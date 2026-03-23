#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChatTTS 命令行推理脚本
使用 params_chattts.json 作为参数进行推理

用法:
    python chattts_infer.py "输入文本" [-p params_chattts.json]

参数文件默认路径: <script_dir>/params_chattts.json
输出路径: {TTS_OUTPUT_DIR}/ChatTTS/（可通过环境变量 TTS_OUTPUT_DIR 覆盖）

Python 环境自动检测：
    优先使用仓库内嵌 Python: <repo_root>/python/python.exe
    fallback 到系统默认 Python
"""

import os
import sys
import json
import argparse
import soundfile as sf

# ============================================================
# 路径计算（全部相对于脚本位置）
# ============================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # ChatTTS/
CHATTS_DIR = SCRIPT_DIR

# 通过上一级目录找到仓库根目录，然后导入 _python_resolver
# 这样可以复用路径解析逻辑
_repo_root = os.path.dirname(SCRIPT_DIR)  # 仓库根目录
_python_resolver_path = os.path.join(_repo_root, "scripts", "_python_resolver.py")

# 如果 scripts/_python_resolver.py 存在，导入它以复用路径解析
if os.path.exists(_python_resolver_path):
    sys.path.insert(0, os.path.join(_repo_root, "scripts"))
    from _python_resolver import get_output_dir, get_chattts_output_dir

# ============================================================
# 配置（使用相对路径 + 环境变量覆盖）
# ============================================================
# params 文件在脚本同级目录
DEFAULT_PARAMS_FILE = os.path.join(SCRIPT_DIR, "params_chattts.json")

# 输出目录：优先从环境变量读取，默认 E:\tts_output\ChatTTS
_TTS_BASE = os.environ.get("TTS_OUTPUT_DIR", r"E:\tts_output")
OUTPUT_DIR = os.path.join(_TTS_BASE, "ChatTTS")

# ============================================================
# 将仓库根目录加入 sys.path 以便导入 tools 包
# ============================================================
# ChatTTS/ 下有 ChatTTS/ChatTTS/ChatTTS/ 结构
# 脚本在 ChatTTS/chattts_infer.py，需要把 ChatTTS/ 加入 sys.path
sys.path.insert(0, CHATTS_DIR)

from tools.audio import float_to_int16
from tools.logger import get_logger
from tools.seeder import TorchSeedContext
from tools.normalizer import normalizer_en_nemo_text, normalizer_zh_tn

import ChatTTS

# ============================================================
# 初始化 ChatTTS
# ============================================================
logger = get_logger("ChatTTS-Inference")
chat = ChatTTS.Chat(logger)

print("[*] 加载 ChatTTS 模型...")
if not chat.load(source="huggingface"):
    print("[!] ChatTTS 模型加载失败")
    sys.exit(1)

try:
    chat.normalizer.register("en", normalizer_en_nemo_text())
except:
    print("[!] nemo_text_processing 未安装")

try:
    chat.normalizer.register("zh", normalizer_zh_tn())
except:
    print("[!] WeTextProcessing 未安装")

print("[+] ChatTTS 模型加载成功")

# ============================================================
# 辅助函数
# ============================================================
def load_params_json(params_file):
    """加载 params_chattts.json"""
    with open(params_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def float_to_int16_np(wav):
    """将音频转换为 int16"""
    import numpy as np
    import torch
    if isinstance(wav, torch.Tensor):
        t = wav.cpu()
        if t.dim() == 2:
            t = t.squeeze(1)
        t = torch.clamp(t, -1.0, 1.0)
        return (t * 32767.0).short().numpy()
    else:
        wav = np.clip(wav, -1.0, 1.0)
        return (wav * 32767.0).astype(np.int16)

# ============================================================
# 推理主流程
# ============================================================
def run_inference(text, params):
    """
    执行 ChatTTS 推理

    步骤：
    1. 文本优化（可选）
    2. 音频生成
    3. 保存音频文件
    """
    refine_text_flag = params.get('refine_text', True)
    temperature = params.get('temperature', 0.3)
    top_p = params.get('top_p', 0.6)
    top_k = params.get('top_k', 20)
    oral = params.get('oral', 4)
    laugh = params.get('laugh', 0)
    break_val = params.get('break_val', 5)
    speed = params.get('speed', 6)
    audio_seed = params.get('audio_seed', 1023)
    text_seed = params.get('text_seed', 42)
    split_batch = params.get('split_batch', 0)
    stream_mode = params.get('stream_mode', False)
    spk_emb = params.get('spk_emb', '')

    prompt = f"[oral_{oral}][laugh_{laugh}][break_{break_val}][speed_{speed}]"

    print(f"\n{'='*60}")
    print(f"ChatTTS 推理")
    print(f"{'='*60}")
    print(f"  输入文本: {text[:50]}...")
    print(f"  文本优化: {refine_text_flag}")
    print(f"  Temperature: {temperature}")
    print(f"  Top_P: {top_p}, Top_K: {top_k}")
    print(f"  Oral: {oral}, Laugh: {laugh}, Break: {break_val}, Speed: {speed}")
    print(f"  音频种子: {audio_seed}, 文本种子: {text_seed}")
    print(f"  音色: {'params_chattts.json中的spk_emb' if spk_emb and spk_emb.startswith('蘁淰') else '随机采样'}")
    print(f"{'='*60}")

    # 步骤1: 文本优化
    refined_text = text
    if refine_text_flag:
        print(f"\n[Step 1/2] 文本优化...")
        print(f"    Prompt: {prompt}, 文本种子: {text_seed}")

        params_refine = ChatTTS.Chat.RefineTextParams(
            temperature=temperature,
            top_P=top_p,
            top_K=top_k,
            prompt=prompt,
            manual_seed=text_seed,
        )

        refined = chat.infer(
            text,
            skip_refine_text=False,
            refine_text_only=True,
            params_refine_text=params_refine,
            split_text=split_batch > 0,
        )
        refined_text = refined[0] if isinstance(refined, list) else refined
        print(f"    优化后: {refined_text[:50]}...")
    else:
        print(f"\n[Step 1/2] 跳过文本优化")

    # 步骤2: 音频生成
    print(f"\n[Step 2/2] 音频生成...")

    # 处理音色
    if spk_emb and spk_emb.startswith("蘁淰"):
        print(f"    使用 params_chattts.json 中的 spk_emb")
        final_spk_emb = spk_emb
    else:
        print(f"    使用音频种子 {audio_seed} 采样音色")
        with TorchSeedContext(audio_seed):
            final_spk_emb = chat.sample_random_speaker()

    params_infer = ChatTTS.Chat.InferCodeParams(
        spk_emb=final_spk_emb,
        temperature=temperature,
        top_P=top_p,
        top_K=top_k,
        prompt=prompt,
        manual_seed=audio_seed,
    )

    print(f"    音频生成中, 种子: {audio_seed}, stream: {stream_mode}")

    wav = chat.infer(
        refined_text,
        skip_refine_text=True,
        params_infer_code=params_infer,
        stream=stream_mode,
        split_text=split_batch > 0,
        max_split_batch=split_batch,
    )

    if stream_mode:
        last = None
        for gen in wav:
            a = gen[0]
            if a is not None and len(a) > 0:
                last = a
        wav = last
    else:
        wav = wav[0]

    # 转换为 int16 并保存
    audio_data = float_to_int16_np(wav)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    import time
    ts = time.strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(OUTPUT_DIR, f"chattts_raw_{ts}.wav")
    sf.write(output_path, audio_data, 24000)

    duration = len(audio_data) / 24000

    print(f"\n{'='*60}")
    print(f"[OK] ChatTTS 推理完成!")
    print(f"  输出路径: {output_path}")
    print(f"  时长: {duration:.2f}s")
    print(f"  采样率: 24000Hz")
    print(f"{'='*60}")

    return output_path, duration

# ============================================================
# 主入口
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description='ChatTTS 命令行推理脚本 - 使用 params_chattts.json 参数'
    )
    parser.add_argument('text', nargs='?', help='输入文本（可选，不提供则使用 params_chattts.json 中的文本）')
    parser.add_argument(
        '--params', '-p',
        default=DEFAULT_PARAMS_FILE,
        help=f'params_chattts.json 文件路径 (默认: {DEFAULT_PARAMS_FILE})'
    )
    args = parser.parse_args()

    # 加载参数
    print(f"[*] 加载参数文件: {args.params}")
    params = load_params_json(args.params)

    # 获取文本
    if args.text:
        text = args.text
    elif params.get('text'):
        text = params['text']
    else:
        print("[ERROR] 请提供文本或确保 params_chattts.json 中有 text 字段")
        sys.exit(1)

    print(f"[*] 文本: {text[:50]}...")

    # 执行推理
    output_path, duration = run_inference(text, params)

    print(f"\n[完成] {output_path}")
    return output_path

if __name__ == "__main__":
    main()
