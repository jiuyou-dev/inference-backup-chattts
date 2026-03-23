import random
from typing import Optional
from time import sleep

import gradio as gr

import sys

sys.path.append("..")
sys.path.append("../..")
from tools.audio import float_to_int16, has_ffmpeg_installed, load_audio
from tools.logger import get_logger

logger = get_logger(" WebUI ")

from tools.seeder import TorchSeedContext
from tools.normalizer import normalizer_en_nemo_text, normalizer_zh_tn

import ChatTTS

chat = ChatTTS.Chat(get_logger("ChatTTS"))

custom_path: Optional[str] = None

has_interrupted = False
is_in_generate = False

seed_min = 1
seed_max = 4294967295

use_mp3 = has_ffmpeg_installed()
if not use_mp3:
    logger.warning("no ffmpeg installed, use wav file output")

# 音色选项：用于预置合适的音色
voices = {
    "默认音色": {"seed": 2},
    "音色1": {"seed": 1111},
    "音色2": {"seed": 2222},
    "音色3": {"seed": 3333},
    "音色4": {"seed": 4444},
    "音色5": {"seed": 5555},
    "音色6": {"seed": 6666},
    "音色7": {"seed": 7777},
    "音色8": {"seed": 8888},
    "音色9": {"seed": 9999},
}


def generate_seed():
    return gr.update(value=random.randint(seed_min, seed_max))


# 返回选择音色对应的seed
def on_voice_change(vocie_selection):
    return voices.get(vocie_selection)["seed"]


def on_audio_seed_change(audio_seed_input):
    with TorchSeedContext(audio_seed_input):
        rand_spk = chat.sample_random_speaker()
    return rand_spk


def export_speaker_to_file(spk_emb_text, filepath="F:/实验文件夹/ChatTTS/参考音频.txt"):
    """将当前音色代码导出到文件（绕过复制粘贴，避免字符损坏）"""
    import json, os
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump({"spk_emb": spk_emb_text}, f, ensure_ascii=False, indent=2)
    return f"✅ 音色已导出到: {filepath}"


def load_inference_params_from_file(filepath):
    """从 JSON 文件加载推理参数，返回所有控件的更新值"""
    import json, os

    # Gradio File 组件可能返回: None、字符串路径、File对象、或直接传内容
    if filepath is None:
        logger.warning("[LoadParams] No file uploaded")
        return [gr.update()] * 15

    # 如果是 File 对象，读取其 name 属性
    actual_path = None
    if hasattr(filepath, 'name'):
        actual_path = filepath.name
    elif isinstance(filepath, str) and os.path.exists(filepath):
        actual_path = filepath
    else:
        # Gradio 6.x 可能直接传文件内容而非路径，尝试直接解析
        try:
            params = json.loads(str(filepath))
            logger.info(f"[LoadParams] Parsed JSON content directly, spk_emb len={len(params.get('spk_emb',''))}")
        except Exception as e:
            logger.warning(f"[LoadParams] Invalid filepath: {filepath}, err={e}")
            return [gr.update()] * 15
        spk_emb_value = params.get('spk_emb', '')
        logger.info(f"[LoadParams] spk_emb prefix: {spk_emb_value[:30] if spk_emb_value else 'EMPTY'}")
        return [
            gr.update(value=params.get('text', '')),
            gr.update(value=params.get('temperature', 0.3)),
            gr.update(value=params.get('top_p', 0.6)),
            gr.update(value=params.get('top_k', 20)),
            gr.update(value=params.get('oral', 2)),
            gr.update(value=params.get('laugh', 0)),
            gr.update(value=params.get('break_val', 4)),
            gr.update(value=params.get('speed', 5)),
            gr.update(value=params.get('refine_text', True)),
            gr.update(value=params.get('audio_seed', 1023)),
            gr.update(value=params.get('text_seed', 42)),
            gr.update(value=params.get('stream_mode', False)),
            gr.update(value=params.get('split_batch', 0)),
            gr.update(value=spk_emb_value),
            gr.update(value=spk_emb_value),
        ]

    # 尝试读取文件
    if not os.path.exists(actual_path):
        logger.warning(f"[LoadParams] File not found: {actual_path}")
        return [gr.update()] * 15

    try:
        with open(actual_path, 'r', encoding='utf-8') as f:
            params = json.load(f)
    except Exception as e:
        logger.error(f"[LoadParams] Failed to read JSON: {e}")
        return [gr.update()] * 15

    spk_emb_value = params.get('spk_emb', '')
    logger.info(f"[LoadParams] Loaded spk_emb length: {len(spk_emb_value)}")

    # 返回值顺序要与 webui.py 中的 outputs 顺序一致
    return [
        gr.update(value=params.get('text', '')),
        gr.update(value=params.get('temperature', 0.3)),
        gr.update(value=params.get('top_p', 0.6)),
        gr.update(value=params.get('top_k', 20)),
        gr.update(value=params.get('oral', 2)),
        gr.update(value=params.get('laugh', 0)),
        gr.update(value=params.get('break_val', 4)),
        gr.update(value=params.get('speed', 5)),
        gr.update(value=params.get('refine_text', True)),
        gr.update(value=params.get('audio_seed', 1023)),
        gr.update(value=params.get('text_seed', 42)),
        gr.update(value=params.get('stream_mode', False)),
        gr.update(value=params.get('split_batch', 0)),
        gr.update(value=spk_emb_value),
        gr.update(value=spk_emb_value),
    ]
def save_inference_params(
    text_input,
    temperature,
    top_p,
    top_k,
    oral,
    laugh,
    break_val,
    speed,
    refine_text_checkbox,
    audio_seed,
    text_seed,
    split_batch,
    stream_mode,
    spk_emb_text,
    output_path="F:/实验文件夹/ChatTTS/params_chattts.json"
):
    """保存当前推理参数到 JSON 文件"""
    import json, os
    params = {
        "text": text_input,
        "refine_text": refine_text_checkbox,
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "oral": oral,
        "laugh": laugh,
        "break_val": break_val,
        "speed": speed,
        "audio_seed": audio_seed,
        "text_seed": text_seed,
        "split_batch": split_batch,
        "stream_mode": stream_mode,
        "spk_emb": spk_emb_text if spk_emb_text and spk_emb_text.startswith("蘁淰") else None,
    }
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(params, f, ensure_ascii=False, indent=2)
    return f"✅ ChatTTS 参数已保存到: {output_path}"



def load_chat(cust_path: Optional[str], coef: Optional[str], enable_cache=True) -> bool:
    if cust_path == None:
        # Use HuggingFace to avoid SSL issues with GitHub Downloads
        ret = chat.load(source="huggingface", coef=coef, enable_cache=enable_cache)
    else:
        logger.info("local model path: %s", cust_path)
        ret = chat.load(
            "custom", custom_path=cust_path, coef=coef, enable_cache=enable_cache
        )
        global custom_path
        custom_path = cust_path
    if ret:
        try:
            chat.normalizer.register("en", normalizer_en_nemo_text())
        except ValueError as e:
            logger.error(e)
        except:
            logger.warning("Package nemo_text_processing not found!")
            logger.warning(
                "Run: conda install -c conda-forge pynini=2.1.5 && pip install nemo_text_processing",
            )
        try:
            chat.normalizer.register("zh", normalizer_zh_tn())
        except ValueError as e:
            logger.error(e)
        except:
            logger.warning("Package WeTextProcessing not found!")
            logger.warning(
                "Run: conda install -c conda-forge pynini=2.1.5 && pip install WeTextProcessing",
            )
    return ret


def reload_chat(coef: Optional[str]) -> str:
    global is_in_generate

    if is_in_generate:
        gr.Warning("Cannot reload when generating!")
        return coef

    chat.unload()
    gr.Info("Model unloaded.")
    if len(coef) != 230:
        gr.Warning("Ignore invalid DVAE coefficient.")
        coef = None
    try:
        global custom_path
        ret = load_chat(custom_path, coef)
    except Exception as e:
        raise gr.Error(str(e))
    if not ret:
        raise gr.Error("Unable to load model.")
    gr.Info("Reload success.")
    return chat.coef


def on_upload_sample_audio(sample_audio_input: Optional[str]) -> str:
    if sample_audio_input is None:
        return ""
    sample_audio = load_audio(sample_audio_input, 24000)
    spk_smp = chat.sample_audio_speaker(sample_audio)
    del sample_audio
    return spk_smp


def _set_generate_buttons(generate_button, interrupt_button, is_reset=False):
    return gr.update(
        value=generate_button, visible=is_reset, interactive=is_reset
    ), gr.update(value=interrupt_button, visible=not is_reset, interactive=not is_reset)


def refine_text(
    text,
    text_seed_input,
    refine_text_flag,
    temperature,
    top_P,
    top_K,
    split_batch,
    oral=2,
    laugh=0,
    break_val=4,
    speed=5,
):
    global chat

    if not refine_text_flag:
        sleep(1)  # to skip fast answer of loading mark
        return text

    # 构建 prompt 控制符
    prompt = f"[oral_{oral}][laugh_{laugh}][break_{break_val}][speed_{speed}]"

    text = chat.infer(
        text,
        skip_refine_text=False,
        refine_text_only=True,
        params_refine_text=ChatTTS.Chat.RefineTextParams(
            temperature=temperature,
            top_P=top_P,
            top_K=top_K,
            prompt=prompt,
            manual_seed=text_seed_input,
        ),
        split_text=split_batch > 0,
    )

    return text[0] if isinstance(text, list) else text


def generate_audio(
    text,
    temperature,
    top_P,
    top_K,
    spk_emb_text: str,
    stream,
    audio_seed_input,
    sample_text_input,
    sample_audio_code_input,
    split_batch,
    oral=2,
    laugh=0,
    break_val=4,
    speed=5,
):
    global chat, has_interrupted

    if not text or has_interrupted or not spk_emb_text.startswith("蘁淰"):
        return None

    # 构建 prompt 控制符
    prompt = f"[oral_{oral}][laugh_{laugh}][break_{break_val}][speed_{speed}]"

    params_infer_code = ChatTTS.Chat.InferCodeParams(
        spk_emb=spk_emb_text,
        temperature=temperature,
        top_P=top_P,
        top_K=top_K,
        prompt=prompt,
        manual_seed=audio_seed_input,
    )

    if sample_text_input and sample_audio_code_input:
        params_infer_code.txt_smp = sample_text_input
        params_infer_code.spk_smp = sample_audio_code_input
        params_infer_code.spk_emb = None

    wav = chat.infer(
        text,
        skip_refine_text=True,
        params_infer_code=params_infer_code,
        stream=stream,
        split_text=split_batch > 0,
        max_split_batch=split_batch,
    )
    if stream:
        for gen in wav:
            audio = gen[0]
            if audio is not None and len(audio) > 0:
                yield 24000, float_to_int16(audio).T
            del audio
    else:
        yield 24000, float_to_int16(wav[0]).T


def interrupt_generate():
    global chat, has_interrupted

    has_interrupted = True
    chat.interrupt()


def set_buttons_before_generate(generate_button, interrupt_button):
    global has_interrupted, is_in_generate

    has_interrupted = False
    is_in_generate = True

    return _set_generate_buttons(
        generate_button,
        interrupt_button,
    )


def set_buttons_after_generate(generate_button, interrupt_button, audio_output):
    global has_interrupted, is_in_generate

    is_in_generate = False

    return _set_generate_buttons(
        generate_button,
        interrupt_button,
        audio_output is not None or has_interrupted,
    )
