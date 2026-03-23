#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RVC 命令行推理脚本
使用 params_rvc.json 作为参数进行推理

用法:
    python rvc_infer_json.py "input_audio.wav" [params_rvc.json]

参数文件默认路径: <script_dir>/params_rvc.json
输出路径: 自动生成，保存到 {TTS_OUTPUT_DIR}/推理/（默认 <repo_root>/tts_output/推理/）
"""

import os
import sys
import json
import shutil
import argparse
import soundfile as sf

# ============================================================
# 路径计算（全部相对于脚本位置）
# ============================================================
RVC_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # RVC/
RVC_PROJECT_DIR = RVC_SCRIPT_DIR  # 推理脚本所在目录即项目根目录

# 通过上一级目录找到仓库根目录，导入路径解析模块
_repo_root = os.path.dirname(RVC_SCRIPT_DIR)  # 仓库根目录
_python_resolver_path = os.path.join(_repo_root, "scripts", "_python_resolver.py")
if os.path.exists(_python_resolver_path):
    sys.path.insert(0, os.path.join(_repo_root, "scripts"))
    from _python_resolver import get_output_dir, get_rvc_output_dir

# 保存原始 argv，防止 Config 的 argparse 干扰脚本参数解析
_real_argv = sys.argv[:]
sys.argv = ['']

# ============================================================
# 环境检测
# ============================================================
import torch

def check_environment():
    """检测运行环境"""
    print("[*] 检测运行环境...")
    
    # Python 版本
    if sys.version_info < (3, 9):
        print(f"[WARN] Python {sys.version_info.major}.{sys.version_info.minor} 可能存在兼容性问题，建议使用 Python 3.9+")
    
    # PyTorch
    print(f"[*] PyTorch 版本: {torch.__version__}")
    
    # GPU/CPU
    if torch.cuda.is_available():
        print(f"[OK] GPU: {torch.cuda.get_device_name(0)}")
    else:
        print(f"[INFO] 无 GPU 或 CUDA 不可用，将使用 CPU 模式")
    
    # FFmpeg
    import shutil
    if shutil.which("ffmpeg"):
        print(f"[OK] FFmpeg 已安装")
    else:
        print(f"[WARN] FFmpeg 未安装，音频处理可能失败")

check_environment()

# ============================================================
# 环境变量
# ============================================================
os.environ.setdefault('weight_root', os.path.join(RVC_PROJECT_DIR, 'assets', 'weights'))
os.environ.setdefault('weight_uvr5_root', os.path.join(RVC_PROJECT_DIR, 'assets', 'uvr5_weights'))
os.environ.setdefault('index_root', os.path.join(RVC_PROJECT_DIR, 'logs'))
os.environ.setdefault('outside_index_root', os.path.join(RVC_PROJECT_DIR, 'assets', 'indices'))
os.environ.setdefault('rmvpe_root', os.path.join(RVC_PROJECT_DIR, 'assets', 'rmvpe'))

# ============================================================
# 路径处理：中文路径 -> ASCII 临时路径
# ============================================================
# 索引临时目录：放在仓库根目录下，避免 C:\ 权限问题
INDEX_TEMP_DIR = os.path.join(_repo_root, "temp_index")

def copy_to_ascii(src_path):
    """将中文路径的文件复制到 ASCII 临时目录"""
    if not src_path or not os.path.exists(src_path):
        return src_path
    os.makedirs(INDEX_TEMP_DIR, exist_ok=True)
    dst = os.path.join(INDEX_TEMP_DIR, os.path.basename(src_path))
    if not os.path.exists(dst):
        shutil.copy2(src_path, dst)
        print(f"    [*] ASCII path: {dst}")
    return dst

# ============================================================
# 核心推理模块导入
# ============================================================
sys.path.insert(0, RVC_PROJECT_DIR)

from configs.config import Config
from infer.modules.vc.modules import VC

# ============================================================
# 初始化
# ============================================================
config = Config()
vc = VC(config)

# ============================================================
# 辅助函数
# ============================================================
def get_model_list():
    """获取可用模型列表"""
    weight_root = os.environ['weight_root']
    try:
        return [f for f in os.listdir(weight_root) if f.endswith('.pth')]
    except Exception:
        return []

def load_params_json(params_file):
    """加载 params_rvc.json"""
    with open(params_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def validate_params(params):
    """验证参数完整性"""
    required = ['model', 'pitch', 'f0_method']
    for key in required:
        if key not in params:
            raise ValueError(f"缺少必需参数: {key}")
    # 填充默认值
    params.setdefault('sid', 0)
    params.setdefault('index_rate', 0)
    params.setdefault('filter_radius', 3)
    params.setdefault('resample_sr', 0)
    params.setdefault('rms_mix_rate', 1.0)
    params.setdefault('protect', 0.33)
    params.setdefault('file_index', '')
    return params

# ============================================================
# 推理主流程
# ============================================================
def run_inference(input_audio, params):
    """
    执行 RVC 推理

    步骤：
    1. 校验输入音频
    2. 处理 file_index 路径（中文 -> ASCII）
    3. 加载模型 (vc.get_vc)
    4. 执行推理 (vc.vc_single)
    5. 保存输出音频
    """
    model_name = params['model']
    sid = params['sid']
    pitch = params['pitch']
    f0_method = params['f0_method']
    file_index = params.get('file_index', '')
    index_rate = params.get('index_rate', 0)
    filter_radius = params.get('filter_radius', 3)
    resample_sr = params.get('resample_sr', 0)
    rms_mix_rate = params.get('rms_mix_rate', 1.0)
    protect = params.get('protect', 0.33)

    # 步骤1: 检查输入音频
    if not os.path.exists(input_audio):
        raise FileNotFoundError(f"输入音频不存在: {input_audio}")

    audio_info = sf.info(input_audio)
    print(f"\n{'='*60}")
    print(f"RVC 推理")
    print(f"{'='*60}")
    print(f"  输入音频: {input_audio}")
    print(f"  音频信息: {audio_info.samplerate}Hz, {audio_info.duration:.2f}s, {audio_info.channels}ch")
    print(f"  模型: {model_name}")
    print(f"  音调: {pitch} 半音")
    print(f"  F0方法: {f0_method}")
    print(f"  索引率: {index_rate}")
    print(f"  滤波半径: {filter_radius}")
    print(f"  RMS混合率: {rms_mix_rate}")
    print(f"  保护参数: {protect}")

    # 步骤2: 处理 file_index 路径（中文路径 -> ASCII 临时路径）
    if file_index and os.path.exists(file_index):
        print(f"  索引文件(原): {file_index}")
        # FAISS 无法处理中文路径，复制到 ASCII 临时目录
        ascii_index = copy_to_ascii(file_index)
        file_index = ascii_index
        print(f"  索引文件(ASCII): {file_index}")
    elif file_index:
        print(f"  [!] 索引文件不存在: {file_index}")
        file_index = ''  # 找不到则不使用索引

    # 步骤3: 加载模型
    print(f"\n[Step 1/2] 加载模型: {model_name}")
    ret = vc.get_vc(model_name)
    print(f"    [OK] 模型加载完成")

    # 步骤4: 执行推理
    print(f"\n[Step 2/2] 开始推理...")
    result = vc.vc_single(
        sid=sid,
        input_audio_path=input_audio,
        f0_up_key=pitch,
        f0_file=None,
        f0_method=f0_method,
        file_index=file_index or '',
        file_index2='',
        index_rate=index_rate,
        filter_radius=filter_radius,
        resample_sr=resample_sr,
        rms_mix_rate=rms_mix_rate,
        protect=protect,
    )

    msg, audio_data = result[0], result[1]

    if audio_data is None or audio_data == (None, None):
        raise RuntimeError(f"推理失败: {msg}")

    sr, audio = audio_data

    # 步骤5: 保存输出
    # 输出目录：优先从环境变量 TTS_OUTPUT_DIR 读取，默认相对于仓库根目录
    _rvc_out_dir = os.environ.get("TTS_OUTPUT_DIR")
    if _rvc_out_dir:
        _rvc_out = os.path.join(_rvc_out_dir, "推理")
    else:
        _rvc_out = os.path.join(_repo_root, "tts_output", "推理")
    os.makedirs(_rvc_out, exist_ok=True)
    ts = input_audio.replace('\\', '/').split('/')[-1].rsplit('.', 1)[0]
    output_path = os.path.join(_rvc_out, f"{ts}_to_{model_name}_p{pitch}_{f0_method}.wav")
    sf.write(output_path, audio, sr)

    duration = len(audio) / sr
    print(f"\n{'='*60}")
    print(f"[OK] 推理完成!")
    print(f"  输出路径: {output_path}")
    print(f"  时长: {duration:.2f}s")
    print(f"  采样率: {sr}Hz")
    print(f"{'='*60}")

    return output_path, duration, sr

# ============================================================
# 主入口
# ============================================================
def main():
    # 恢复原始 argv
    sys.argv = _real_argv

    parser = argparse.ArgumentParser(
        description='RVC 命令行推理脚本 - 使用 params_rvc.json 参数'
    )
    parser.add_argument('input', nargs='?', help='输入音频文件路径')
    parser.add_argument(
        '--params', '-p',
        default=os.path.join(RVC_PROJECT_DIR, 'params_rvc.json'),
        help='params_rvc.json 文件路径 (默认: <project_root>/params_rvc.json)'
    )
    parser.add_argument(
        '--model', '-m',
        help='覆盖 params_rvc.json 中的模型名称'
    )
    parser.add_argument(
        '--pitch', '-pt',
        type=int,
        help='覆盖 params_rvc.json 中的音调参数'
    )
    parser.add_argument(
        '--output', '-o',
        help='指定输出文件路径'
    )
    args = parser.parse_args()

    # 如果没有提供输入参数，尝试从命令行获取
    if not args.input:
        print("用法: python rvc_infer_json.py <input_audio.wav> [--params params_rvc.json] [--model xxx.pth] [--pitch N]")
        sys.exit(1)

    input_audio = args.input

    # 加载参数
    print(f"[*] 加载参数文件: {args.params}")
    params = load_params_json(args.params)
    params = validate_params(params)
    print(f"    模型: {params['model']}")
    print(f"    音调: {params['pitch']}")
    print(f"    F0方法: {params['f0_method']}")

    # 命令行覆盖参数
    if args.model:
        params['model'] = args.model
    if args.pitch is not None:
        params['pitch'] = args.pitch

    # 执行推理
    output_path, duration, sr = run_inference(input_audio, params)

    print(f"\n[完成] {output_path}")

if __name__ == "__main__":
    main()
