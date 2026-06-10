@echo off
chcp 65001 >nul
echo ========================================
echo Jadx-AI 脚本运行工具
echo ========================================
echo.
echo 可用脚本:
echo   1. check_connection     - 检查 JADX 插件连接
echo   2. simple_test          - 简单 API 测试
echo   3. test_api             - API 端点测试
echo   4. debug_api            - API 调试
echo   5. list_resources       - 列出资源文件
echo   6. analyze_security     - 安全分析
echo   7. deep_security        - 深度安全分析
echo   8. final_analyze        - 最终分析
echo.
echo 目录说明:
echo   scripts/   - Python 脚本目录
echo   tmp/       - 临时文件目录
echo   result/    - 结果输出目录
echo.
set /p choice="请输入脚本编号 (1-8) 或直接输入脚本名称: "

if "%choice%"=="1" set script=check_connection.py
if "%choice%"=="2" set script=simple_test.py
if "%choice%"=="3" set script=test_api.py
if "%choice%"=="4" set script=debug_api.py
if "%choice%"=="5" set script=list_resources.py
if "%choice%"=="6" set script=analyze_security.py
if "%choice%"=="7" set script=deep_security_analyze.py
if "%choice%"=="8" set script=final_analyze.py

if "%script%"=="" set script=%choice%

if not exist "scripts\%script%" (
    echo.
    echo 错误: 找不到脚本 "%script%"
    pause
    exit /b 1
)

echo.
echo 正在运行: %script%
echo ========================================
cd /d "%~dp0scripts"
python "%script%"
cd ..
echo.
echo ========================================
echo 脚本执行完成
echo ========================================
pause
