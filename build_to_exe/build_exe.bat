@echo off
echo 正在打包 Escape From Qin Shi Huang...
echo.

REM 清理之前的建置檔案
if exist "dist" (
    echo 清理舊的建置檔案...
    rmdir /s /q "dist"
)

if exist "build" (
    rmdir /s /q "build"
)

echo 開始使用 PyInstaller 打包...
echo.

REM 使用規格檔案進行打包
pyinstaller --clean build_exe.spec

if %errorlevel% == 0 (
    echo.
    echo 打包完成！
    echo 執行檔位於: dist\EscapeFromQinShiHuang.exe
    echo.
    echo 您可以將整個 dist 資料夾複製到其他電腦執行遊戲。
    pause
) else (
    echo.
    echo 打包過程中發生錯誤！
    echo 請檢查錯誤訊息並嘗試修復。
    pause
)
