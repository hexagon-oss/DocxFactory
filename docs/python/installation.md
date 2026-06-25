# Installation and Build (Python)

This section replaces the legacy package install flow with the repository's current source-based workflow.

## Prerequisites

- CMake 3.21+
- Conan 2.x
- C++ toolchain for your platform
- Python 3
- SWIG 4.x

## 1. Detect Conan profile

```bash
conan profile detect --force
```

## 2. Install dependencies

macOS example:

```bash
conan install . -of build/macos-release -s build_type=Release -o '&:with_uno=False' -o '&:with_python=True' -o '&:with_imagemagick=False' --build=missing
```

Linux example:

```bash
conan install . -of build/linux-release -s build_type=Release -o '&:with_uno=False' -o '&:with_python=True' -o '&:with_imagemagick=False' --build=missing
```

Windows example:

```powershell
conan install . -of build/win-vs2022 -s build_type=Release -s compiler="msvc" -s compiler.version=193 -s arch=x86_64 -o '&:with_uno=False' -o '&:with_python=True' -o '&:with_imagemagick=False' --build=missing
```

## 3. Configure CMake with Python binding enabled

macOS example:

```bash
cmake -S . -B build/macos-release \
  -DCMAKE_TOOLCHAIN_FILE=build/macos-release/build/Release/generators/conan_toolchain.cmake \
  -DCMAKE_BUILD_TYPE=Release \
  -DDOCXFACTORY_BUILD_PYTHON=ON
```

## 4. Build

```bash
cmake --build build/macos-release --config Release -j
```

## 5. Verify generated Python artifacts

Expected files:

- `build/<cfg>/docxfactory.py`
- `build/<cfg>/python/_docxfactory.so` (or platform equivalent extension)

## 6. Verify import

```python
import sys
sys.path.insert(0, "build/macos-release")
sys.path.insert(0, "build/macos-release/python")
import docxfactory
print("DocxFactory import OK")
```

## Important clean-build rule

If you delete `build/<cfg>`, run `conan install` again before running CMake. The Conan toolchain and dependency config files are generated into the build folder.
