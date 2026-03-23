#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RVC 环境检测脚本
检测运行环境是否满足要求

用法:
    python check_env.py
"""

import sys
import shutil
import os

def check_python_version():
    """检查 Python 版本"""
    version = sys.version_info
    print(f"[*] Python 版本: {version.major}.{version.minor}.{version.micro}")
    if version < (3, 9):
        print(f"[ERROR] 需要 Python 3.9+，当前版本 {version.major}.{version.minor} 不满足要求")
        return False
    print(f"[OK] Python 版本满足要求")
    return True

def check_torch():
    """检查 PyTorch"""
    try:
        import torch
        print(f"[*] PyTorch 版本: {torch.__version__}")
        if torch.cuda.is_available():
            print(f"[OK] CUDA 可用: {torch.cuda.get_device_name(0)}")
            return True
        else:
            print(f"[WARN] CUDA 不可用，将使用 CPU 模式")
            return True
    except ImportError:
        print(f"[ERROR] PyTorch 未安装，请运行: pip install torch")
        return False

def check_numpy():
    """检查 NumPy"""
    try:
        import numpy as np
        print(f"[*] NumPy 版本: {np.__version__}")
        if int(np.__version__.split('.')[0]) >= 3:
            print(f"[WARN] NumPy 3.x 可能存在兼容性问题，建议使用 NumPy < 3.0")
        return True
    except ImportError:
        print(f"[ERROR] NumPy 未安装")
        return False

def check_scipy():
    """检查 SciPy"""
    try:
        import scipy
        print(f"[*] SciPy 版本: {scipy.__version__}")
        return True
    except ImportError:
        print(f"[ERROR] SciPy 未安装")
        return False

def check_soundfile():
    """检查 SoundFile"""
    try:
        import soundfile
        print(f"[*] SoundFile 版本: {soundfile.__version__}")
        return True
    except ImportError:
        print(f"[ERROR] SoundFile 未安装")
        return False

def check_fairseq():
    """检查 FairSeq"""
    try:
        import fairseq
        print(f"[*] FairSeq 版本: {fairseq.__version__ if hasattr(fairseq, '__version__') else 'unknown'}")
        return True
    except ImportError:
        print(f"[ERROR] FairSeq 未安装")
        return False

def check_ffmpeg():
    """检查 FFmpeg"""
    if shutil.which("ffmpeg"):
        print(f"[OK] FFmpeg 已安装")
        return True
    else:
        print(f"[WARN] FFmpeg 未安装，音频处理可能失败")
        print(f"     Windows: 下载 https://ffmpeg.org/download.html")
        print(f"     Linux: sudo apt install ffmpeg")
        print(f"     Mac: brew install ffmpeg")
        return False

def check_gpu():
    """检查 GPU 可用性"""
    try:
        import torch
        if torch.cuda.is_available():
            print(f"[OK] GPU: {torch.cuda.get_device_name(0)}")
            print(f"     CUDA: {torch.version.cuda}")
            return True
        else:
            print(f"[INFO] 无 GPU，将使用 CPU 模式（速度较慢）")
            return True
    except:
        print(f"[WARN] 无法检测 GPU 状态")
        return True

def check_assets():
    """检查资源文件"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 项目根目录是脚本所在目录
    project_root = script_dir
    
    assets_dir = os.path.join(project_root, 'assets')
    weights_dir = os.path.join(assets_dir, 'weights')
    
    if not os.path.exists(weights_dir):
        print(f"[ERROR] 缺少 weights 目录: {weights_dir}")
        return False
    
    weights = [f for f in os.listdir(weights_dir) if f.endswith('.pth')]
    if not weights:
        print(f"[ERROR] weights 目录为空，请添加模型文件")
        return False
    
    print(f"[OK] 发现 {len(weights)} 个模型: {', '.join(weights)}")
    
    # 检查 rmvpe
    rmvpe_dir = os.path.join(assets_dir, 'rmvpe')
    rmvpe_file = os.path.join(rmvpe_dir, 'rmvpe.pt')
    if os.path.exists(rmvpe_file):
        print(f"[OK] RMVPE 模型存在")
    else:
        print(f"[WARN] RMVPE 模型不存在")
    
    return True

def main():
    print("=" * 60)
    print("飞书语情感语音生成框架 - 环境检测")
    print("=" * 60)
    print()
    
    checks = [
        ("Python 版本", check_python_version),
        ("PyTorch", check_torch),
        ("NumPy", check_numpy),
        ("SciPy", check_scipy),
        ("SoundFile", check_soundfile),
        ("FairSeq", check_fairseq),
        ("FFmpeg", check_ffmpeg),
        ("GPU", check_gpu),
        ("资源文件", check_assets),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n[{name}]")
        print("-" * 40)
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"[ERROR] 检查失败: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("检测结果汇总")
    print("=" * 60)
    
    all_passed = True
    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"  {status}  {name}")
        if not result:
            all_passed = False
    
    print()
    if all_passed:
        print("[OK] All checks passed! Environment is ready.")
        return 0
    else:
        print("[WARN] Some checks failed. Please install missing dependencies.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
