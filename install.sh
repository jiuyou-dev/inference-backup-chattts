#!/bin/bash
# ============================================================
# 飞书语情感语音生成框架 - 环境安装脚本 (Linux/macOS)
# ============================================================

set -e

echo "============================================================"
echo "飞书语情感语音生成框架 - 环境安装脚本"
echo "============================================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到 Python3，请先安装 Python 3.9+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "[检测] Python 版本: $PYTHON_VERSION"

# 检查 CUDA
python3 -c "import torch; print(f'[GPU] {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"CPU\"}')" 2>/dev/null || echo "[GPU] CPU"

echo ""
echo "============================================================"
echo "开始安装依赖..."
echo "============================================================"

# 安装 PyTorch (CUDA 12.1)
echo "[1/3] 安装 PyTorch (CUDA 12.1)..."
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 安装核心依赖
echo "[2/3] 安装核心依赖..."
pip3 install 'numpy<3.0.0' scipy soundfile tqdm

# 安装 ChatTTS 特定依赖
echo "[3/3] 安装 ChatTTS/RVC 特定依赖..."
pip3 install vector-quantize-pytorch transformers vocos fairseq

echo ""
echo "============================================================"
echo "安装完成！"
echo "============================================================"
echo ""
echo "用法:"
echo "  ChatTTS: python3 ChatTTS/chattts_infer.py \"文本\""
echo "  RVC:     python3 RVC/rvc_infer_json.py input.wav"
echo ""
