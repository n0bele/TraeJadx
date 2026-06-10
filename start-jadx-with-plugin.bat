@echo off
chcp 65001 >nul
echo ==============================================
echo JADX AI MCP - 启动脚本
echo ==============================================
echo.
echo 正在检查 Java 版本...
java -version
echo.
echo.
echo 插件已安装在: %~dp0jadx-1.5.5\plugins\
echo.
echo 正在启动 JADX GUI...
echo.
cd /d "%~dp0jadx-1.5.5\bin"
echo JADX AI MCP 插件将监听端口 8650
echo.
echo 注意: 请在 JADX GUI 中打开一个 APK 文件
echo.
echo 启动中...
start "JADX AI MCP" jadx-gui.bat
echo.
echo JADX GUI 已启动！
echo.
echo 请在 JADX GUI 中打开一个 APK 文件
echo 然后回到 TRAE 开始使用 AI 功能
echo.
pause
