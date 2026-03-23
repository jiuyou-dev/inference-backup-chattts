#!/bin/bash
# RVC 推理启动脚本 (Linux/Mac)
# 用法: ./run_rvc.sh [参数]

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 未安装"
    exit 1
fi

# 检查环境
echo "[*] 检查运行环境..."
python3 check_env.py
if [ $? -ne 0 ]; then
    echo "[WARN] 环境检测有问题，但继续尝试运行..."
fi

# 运行推理
echo "[*] 启动 RVC 推理..."
python3 rvc_infer_json.py "$@"

exit $?
