#!/bin/bash
# build.sh — Build script for roguelike (Linux/macOS)
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="${SCRIPT_DIR}/build"
VCPKG_ROOT="${VCPKG_ROOT:-$HOME/vcpkg}"

echo "=== Roguelike Build Script ==="
echo "Source:  ${SCRIPT_DIR}"
echo "Build:   ${BUILD_DIR}"
echo "vcpkg:   ${VCPKG_ROOT}"

# Check vcpkg
if [ ! -f "${VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake" ]; then
    echo "ERROR: vcpkg not found at ${VCPKG_ROOT}"
    echo "Set VCPKG_ROOT env var or install vcpkg"
    exit 1
fi

# Configure
echo ""
echo "--- Configuring CMake ---"
cmake -B "${BUILD_DIR}" -S "${SCRIPT_DIR}" \
    -DCMAKE_TOOLCHAIN_FILE="${VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake" \
    -DCMAKE_BUILD_TYPE=Release

# Build
echo ""
echo "--- Building ---"
cmake --build "${BUILD_DIR}" --config Release -j$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)

# Copy shared libs (Linux/macOS)
echo ""
echo "--- Copying shared libraries ---"
if [ -f "${BUILD_DIR}/vcpkg_installed/x64-linux/lib/libraylib.so" ]; then
    cp "${BUILD_DIR}/vcpkg_installed/x64-linux/lib/libraylib.so" "${BUILD_DIR}/"
fi
if [ -f "${BUILD_DIR}/vcpkg_installed/x64-linux/lib/libglfw.so.3" ]; then
    cp "${BUILD_DIR}/vcpkg_installed/x64-linux/lib/libglfw.so.3" "${BUILD_DIR}/"
fi

# Run tests
echo ""
echo "--- Running tests ---"
if [ -f "${BUILD_DIR}/roguelike_tests" ]; then
    "${BUILD_DIR}/roguelike_tests"
fi

echo ""
echo "=== Build complete ==="
echo "Executable: ${BUILD_DIR}/roguelike"
echo "Run: ${BUILD_DIR}/roguelike"
