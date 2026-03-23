@echo off
REM RVC 推理启动脚本 (Windows)
REM 用法: run_rvc.bat [参数]

REM 获取脚本所在目录
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM 检查 Python
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python 未安装
    exit /b 1
)

REM 检查环境
echo [*] 检查运行环境...
python check_env.py

REM 运行推理
echo [*] 启动 RVC 推理...
python rvc_infer_json.py %*

exit /b %ERRORLEVEL%
