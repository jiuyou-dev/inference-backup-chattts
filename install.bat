@echo off
chcp 65001 >nul
echo ============================================================
echo 飞书语情感语音生成框架 - 环境安装脚本
echo ============================================================
echo.

REM 检查 Python 版本
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.9+
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [检测] Python 版本: %PYTHON_VERSION%

REM 检查 CUDA
python -c "import torch; print(f'[GPU] {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"CPU\"}')" 2>nul

echo.
echo ============================================================
echo 开始安装依赖...
echo ============================================================

REM 安装 PyTorch (CUDA 12.1)
echo [1/3] 安装 PyTorch (CUDA 12.1)...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

REM 安装核心依赖
echo [2/3] 安装核心依赖...
pip install numpy<3.0.0 scipy soundfile tqdm

REM 安装 ChatTTS 特定依赖
echo [3/3] 安装 ChatTTS/RVC 特定依赖...
pip install vector-quantize-pytorch transformers vocos fairseq

echo.
echo ============================================================
echo 安装完成！
echo ============================================================
echo.
echo 用法:
echo   ChatTTS: python ChatTTS\chattts_infer.py "文本"
echo   RVC:     python RVC\rvc_infer_json.py input.wav
echo.
pause
