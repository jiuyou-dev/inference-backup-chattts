@echo off
chcp 65001 >nul
setlocal

set "PROJECT_ROOT=%~dp0"
set "PYTHON=%PROJECT_ROOT%python\python.exe"

cd /d "%PROJECT_ROOT%ChatTTS"
set "PYTHONPATH=%PROJECT_ROOT%ChatTTS"

echo ============================================================
echo ChatTTS 推理测试
echo ============================================================
echo 项目根目录: %PROJECT_ROOT%
echo Python: %PYTHON%
echo.

%PYTHON% -c "import os; os.environ['PYTHONPATH'] = r'%PROJECT_ROOT%ChatTTS'; import sys; sys.path.insert(0, r'%PROJECT_ROOT%ChatTTS'); exec(open(r'%PROJECT_ROOT%ChatTTS\chattts_infer.py').read())" %1

endlocal
