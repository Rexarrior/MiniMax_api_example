@echo off
REM build.bat — Build script for roguelike (Windows)
setlocal enabledelayedexpansion

set "VCPKG_ROOT=%VCPKG_ROOT%S:\programming\my\vcpkg"
set "CMAKE_EXE=%VCPKG_ROOT%\downloads\tools\cmake-3.31.10-windows\cmake-3.31.10-windows-x86_64\bin\cmake.exe"
set "BUILD_DIR=%~dp0build"

echo === Roguelike Build Script ===
echo vcpkg:   %VCPKG_ROOT%
echo Build:   %BUILD_DIR%

REM Check vcpkg
if not exist "%VCPKG_ROOT%\scripts\buildsystems\vcpkg.cmake" (
    echo ERROR: vcpkg not found at %VCPKG_ROOT%
    echo Set VCPKG_ROOT env var or install vcpkg
    exit /b 1
)

REM Configure
echo.
echo --- Configuring CMake ---
"%CMAKE_EXE%" -B "%BUILD_DIR%" -S "%~dp0." -DCMAKE_TOOLCHAIN_FILE="%VCPKG_ROOT%\scripts\buildsystems\vcpkg.cmake"
if errorlevel 1 exit /b 1

REM Build
echo.
echo --- Building ---
"%CMAKE_EXE%" --build "%BUILD_DIR%" --config Release
if errorlevel 1 exit /b 1

REM Copy DLLs
echo.
echo --- Copying DLLs ---
if exist "%VCPKG_ROOT%\installed\x64-windows\bin\raylib.dll" (
    copy /Y "%VCPKG_ROOT%\installed\x64-windows\bin\raylib.dll" "%BUILD_DIR%\Release\"
)
if exist "%VCPKG_ROOT%\installed\x64-windows\bin\glfw3.dll" (
    copy /Y "%VCPKG_ROOT%\installed\x64-windows\bin\glfw3.dll" "%BUILD_DIR%\Release\"
)

REM Run tests
echo.
echo --- Running tests ---
if exist "%BUILD_DIR%\Release\roguelike_tests.exe" (
    "%BUILD_DIR%\Release\roguelike_tests.exe" --gtest_brief=1
)

echo.
echo === Build complete ===
echo Executable: %BUILD_DIR%\Release\roguelike.exe
echo Run: "%BUILD_DIR%\Release\roguelike.exe"
