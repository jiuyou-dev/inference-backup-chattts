#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 解释器路径模块
仅使用仓库内嵌 Python：<repo_root>/python/python.exe

使用方法：
    from _python_resolver import get_python_exe, get_repo_root

    python_exe = get_python_exe()
    repo_root = get_repo_root()
"""

import os
import sys

# ============================================================
# 路径配置（全部使用相对于本文件的相对路径）
# ============================================================

# 本文件位于 scripts/ 目录下
# 仓库根目录 = scripts/ 的上一级
_SELF_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(_SELF_DIR)  # 仓库根目录

# 内嵌 Python 路径（相对于仓库根目录）
EMBEDDED_PYTHON_REL = os.path.join("python", "python.exe")


def get_repo_root():
    """获取仓库根目录"""
    return REPO_ROOT


def get_python_exe():
    """
    获取 Python 解释器路径

    仅使用仓库内嵌 Python：<repo_root>/python/python.exe
    """
    embedded_py = os.path.join(REPO_ROOT, EMBEDDED_PYTHON_REL)
    if not os.path.exists(embedded_py):
        raise FileNotFoundError(
            f"未找到仓库内嵌 Python：{embedded_py}\n"
            "请确保 <仓库根目录>/python/python.exe 存在。"
        )
    return embedded_py


def get_chattts_dir():
    """获取 ChatTTS 目录路径"""
    return os.path.join(REPO_ROOT, "ChatTTS")


def get_rvc_dir():
    """获取 RVC 目录路径"""
    return os.path.join(REPO_ROOT, "RVC")


def get_output_dir():
    """获取 TTS 输出目录（默认相对于仓库根目录，可通过环境变量 TTS_OUTPUT_DIR 覆盖）"""
    custom = os.environ.get("TTS_OUTPUT_DIR")
    if custom:
        return custom
    return os.path.join(REPO_ROOT, "tts_output")


def get_chattts_output_dir():
    """获取 ChatTTS 音频输出目录"""
    return os.path.join(get_output_dir(), "ChatTTS")


def get_rvc_output_dir():
    """获取 RVC 推理输出目录"""
    return os.path.join(get_output_dir(), "推理")


# ============================================================
# 主入口：测试打印
# ============================================================
if __name__ == "__main__":
    py = get_python_exe()
    root = get_repo_root()
    print(f"仓库根目录: {root}")
    print(f"使用 Python: {py}")
    print(f"ChatTTS 目录: {get_chattts_dir()}")
    print(f"RVC 目录: {get_rvc_dir()}")
    print(f"输出目录: {get_output_dir()}")
