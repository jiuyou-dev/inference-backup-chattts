#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 解释器自动检测模块
自动选择仓库内嵌 Python（推荐）或系统 Python（fallback）

使用方法：
    from _python_resolver import get_python_exe, get_repo_root

    python_exe = get_python_exe()
    repo_root = get_repo_root()

路径优先级：
    1. {repo_root}/python/python.exe          ← 仓库内嵌 Python（推荐）
    2. C:\\Espressif\\tools\\idf-python\\python.exe  ← 九幽工作区兼容
    3. sys.executable                         ← 系统默认 Python
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

# 九幽工作区兼容路径（保持兼容，不推荐新用户使用）
IDF_PYTHON_FALLBACK = r"C:\Espressif\tools\idf-python\python.exe"


def get_repo_root():
    """获取仓库根目录"""
    return REPO_ROOT


def get_python_exe():
    """
    自动选择 Python 解释器

    优先级：
    1. {repo_root}/python/python.exe（仓库内嵌 Python）
    2. C:\\Espressif\\tools\\idf-python\\python.exe（九幽工作区兼容）
    3. sys.executable（系统默认 Python）
    """
    # 方案1：仓库内嵌 Python
    embedded_py = os.path.join(REPO_ROOT, EMBEDDED_PYTHON_REL)
    if os.path.exists(embedded_py):
        return embedded_py

    # 方案2：九幽工作区 Python（兼容旧配置）
    if os.path.exists(IDF_PYTHON_FALLBACK):
        return IDF_PYTHON_FALLBACK

    # 方案3：系统默认
    return sys.executable


def get_chattts_dir():
    """获取 ChatTTS 目录路径"""
    return os.path.join(REPO_ROOT, "ChatTTS")


def get_rvc_dir():
    """获取 RVC 目录路径"""
    return os.path.join(REPO_ROOT, "RVC")


def get_output_dir():
    """获取 TTS 输出目录（默认 E:\\tts_output，可通过环境变量覆盖）"""
    return os.environ.get("TTS_OUTPUT_DIR", r"E:\tts_output")


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
