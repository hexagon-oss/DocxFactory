DocxFactory compilation instructions
====================================

This project now supports a Conan + CMake workflow for cross-platform C++ builds.

Build goals covered by this setup:

- Linux with GCC + CMake
- Windows with Visual Studio + CMake
- macOS with Clang/GCC + CMake (best effort, depends on dependency availability)
- Python 3 SWIG binding (optional, enabled by default when toolchain is available)


Prerequisites
-------------

Install these tools first:

- CMake 3.21+
- Conan 2.x
- A C++ compiler toolchain for your OS
- SWIG 4.x (optional, for Python binding)
- Python 3 development headers (optional, for Python binding)


Conan dependency management
---------------------------

Dependencies are managed through `conanfile.py`.

Typical setup:

1. Detect/create a Conan profile:

	 ```bash
	 conan profile detect --force
	 ```

2. Install dependencies and generate CMake toolchain files:

	 ```bash
	 conan install . \
		 -of build/<cfg> \
		 -s build_type=<Release|Debug> \
		 -o '&:with_uno=False' \
		 -o '&:with_python=True' \
		 -o '&:with_imagemagick=False' \
		 --build=missing
	 ```

Notes:

- UNO is disabled by default (`with_uno=False`) because it requires LibreOffice SDK headers and runtime.
- Python binding remains optional (`with_python=True` by default in Conan recipe).
- ImageMagick support is optional (`with_imagemagick=False` by default in Conan recipe).


Linux (GCC + CMake)
-------------------

```bash
conan profile detect --force
conan install . -of build/linux-release -s build_type=Release -o '&:with_uno=False' -o '&:with_imagemagick=False' --build=missing

cmake -S . -B build/linux-release \
	-DCMAKE_TOOLCHAIN_FILE=build/linux-release/build/Release/generators/conan_toolchain.cmake \
	-DCMAKE_BUILD_TYPE=Release

cmake --build build/linux-release --config Release -j
# Optional: no CTest tests are currently registered in this repository.
# Running ctest will print "No tests were found!!!" unless tests are added.
ctest --test-dir build/linux-release --output-on-failure || true
```

**Important:** If you delete the `build/` folder for a clean rebuild, you MUST re-run `conan install` first to regenerate the toolchain file, or cmake will fail with "Could not find Boost".


Windows (Visual Studio + CMake)
-------------------------------

Example for Visual Studio 2022 and x64:

```powershell
conan profile detect --force
conan install . -of build/win-vs2022 -s build_type=Release -s compiler="msvc" -s compiler.version=193 -s arch=x86_64 -o '&:with_uno=False' -o '&:with_imagemagick=False' --build=missing

cmake -S . -B build/win-vs2022 -G "Visual Studio 17 2022" -A x64 `
	-DCMAKE_TOOLCHAIN_FILE=build/win-vs2022/build/Release/generators/conan_toolchain.cmake

cmake --build build/win-vs2022 --config Release
# Optional: no CTest tests are currently registered in this repository.
# Running ctest will print "No tests were found!!!" unless tests are added.
ctest --test-dir build/win-vs2022 -C Release --output-on-failure
```

**Important:** If you delete the `build/` folder for a clean rebuild, you MUST re-run `conan install` first to regenerate the toolchain file, or cmake will fail with "Could not find Boost".


macOS (CMake + Apple Clang/GCC)
-------------------------------

```bash
conan profile detect --force
conan install . -of build/macos-release -s build_type=Release -o '&:with_uno=False' -o '&:with_imagemagick=False' --build=missing

cmake -S . -B build/macos-release \
	-DCMAKE_TOOLCHAIN_FILE=build/macos-release/build/Release/generators/conan_toolchain.cmake \
	-DCMAKE_BUILD_TYPE=Release

cmake --build build/macos-release --config Release -j
# Optional: no CTest tests are currently registered in this repository.
# Running ctest will print "No tests were found!!!" unless tests are added.
ctest --test-dir build/macos-release --output-on-failure || true
```

**Important:** If you delete the `build/` folder for a clean rebuild, you MUST re-run `conan install` first to regenerate the toolchain file, or cmake will fail with "Could not find Boost".

Alternative (CMake 3.23+): Use Conan's generated preset instead of explicit toolchain path:

```bash
cmake --preset conan-release
cmake --build build/macos-release --config Release -j
```

If a dependency is not available for your macOS architecture/profile, Conan will report it during `conan install`.


Python 3 binding (optional)
---------------------------

The Python SWIG module can be enabled via `DOCXFACTORY_BUILD_PYTHON=ON`.

Requirements:

- `swig` in `PATH`
- Python 3 interpreter + development headers

Control it from CMake:

```bash
cmake -S . -B build/macos-release \
	-DCMAKE_TOOLCHAIN_FILE=build/macos-release/build/Release/generators/conan_toolchain.cmake \
	-DCMAKE_BUILD_TYPE=Release \
	-DDOCXFACTORY_BUILD_PYTHON=ON
```

If Python/SWIG is missing, the C++ build continues and CMake prints a warning.

Additional Python docs and runnable examples:

- `docs/python/README.md`
- `examples/python/hello_world/README.md`

**Status**: Python SWIG bindings are working with the CMake build on macOS and produce:

- `build/<cfg>/python/_docxfactory.so`
- `build/<cfg>/docxfactory.py`

### Python usage example

This project exposes singleton-style APIs from C++, so use `get_instance()` instead of constructors.

```python
import sys

# Adjust for your build directory (linux-release, macos-release, win-vs2022, etc.)
sys.path.insert(0, "build/macos-release")
sys.path.insert(0, "build/macos-release/python")

import docxfactory

# Both names are available:
# - docxfactory.word_processing_compiler / word_processing_merger
# - docxfactory.WordProcessingCompiler / WordProcessingMerger (compatibility aliases)

compiler = docxfactory.WordProcessingCompiler.get_instance()
compiler.compile("input_template.docx", "compiled_template.dfw")

merger = docxfactory.WordProcessingMerger.get_instance()
merger.load("compiled_template.dfw")
merger.merge("<root><name>Example</name></root>")
merger.save("output.docx")
merger.close()
```


Build options
-------------

Main CMake options:

- `DOCXFACTORY_NO_PNG` (default `ON`)
- `DOCXFACTORY_BUILD_TOOLS` (default `ON`)
- `DOCXFACTORY_ENABLE_UNO` (default `OFF`)
- `DOCXFACTORY_BUILD_PYTHON` (default `ON`)
- `DOCXFACTORY_WITH_IMAGEMAGICK` (default `OFF`)


Platform-specific considerations
---------------------------------

### macOS (Apple Clang)

The codebase has been adapted for macOS through the following fixes:

- **Unix function support**: UnixFunc module is compiled on macOS (extended `__unix__` macro to include `__APPLE__`)
- **ICU C++17 compatibility**: C++17 standard required for modern ICU namespace handling (`using namespace icu;`)
- **Pointer serialization**: 64-bit safe pointer-to-uint32 casting via `DOCXFACTORY_PTR_TO_UINT32` macro for legacy serialized data
- **Minizip headers**: Fallback include chain accommodates different header locations across platforms
- **RapidJSON iterators**: Updated to use modern MemberIterator API with dereferencing syntax `(*iterator).member`
- **DLL macro guards**: Word processing tools use empty DLL macro on Unix-like systems instead of `__declspec` attributes

### Linux (GCC/Clang)

Standard build supported with no special considerations beyond dependency availability.

### Windows (MSVC)

Standard build supported. Note that getopt exception specifications are only applied on MSVC to avoid conflicts with BSD headers on Unix-like systems.


Known limitations and workarounds
---------------------------------

### ImageMagick support

ImageMagick integration is disabled by default (`with_imagemagick=False`) due to licensing concerns and dependency complexity. To enable:

```bash
conan install . -of build/... -o '&:with_imagemagick=True' --build=missing
```

### Python binding on macOS

Python SWIG binding is supported. If import/build issues occur, verify your Python setup:

```bash
python3 --version
python3-config --includes
```

### UNO (LibreOffice) support

LibreOffice SDK integration is disabled by default. Requires LibreOffice development files. To enable:

```bash
conan install . -of build/... -o '&:with_uno=True' --build=missing
```

Note: UNO support may not be available on all platforms/architectures.


Troubleshooting
---------------

**Error: "Dependency not available for your profile"**

- Check Conan profile: `conan profile show default`
- Force profile detection: `conan profile detect --force`
- Enable missing dependencies to build from source: `--build=missing`

**Conan warnings about deprecated Conan 1.X fields (`cpp_info.names`, `env_info`, etc.)**

- Root cause: some upstream ConanCenter recipes still expose legacy metadata for backward compatibility.
- Impact: warning-only; does not indicate a broken build in Conan 2.x.
- Action: safe to proceed; warnings will disappear as upstream recipes are modernized.

**Error: "Could not find Conan toolchain file"**

- Ensure `conan install` completed successfully before `cmake`
- Check toolchain path matches CMake `-DCMAKE_TOOLCHAIN_FILE` parameter
- Typical location: `build/<config>/build/Release/generators/conan_toolchain.cmake`

**Error: "argument -o/--options: expected one argument"**

- Root cause: your shell (especially zsh) interprets unquoted `&` in Conan package options.
- Fix: quote each option value, for example: `-o '&:with_uno=False'`

**CTest output: "No tests were found!!!"**

- Root cause: the CMake project includes CTest support but currently defines no tests with `add_test(...)`.
- Impact: informational; it does not mean compilation failed.

**macOS: "command not found: conan"**

- Install Conan: `pip3 install conan`
- Or via Homebrew: `brew install conan`

**Python binding not working**

- Check SWIG is available: `which swig`
- Install SWIG: `brew install swig` (macOS) or `apt install swig` (Linux)
- Verify Python headers: `python3 -m pip show python3-dev` or `apt install python3-dev`

**Build errors on architecture mismatch**

- Create architecture-specific Conan profile:
  ```bash
  conan profile detect --force
  conan install . -s arch=arm64 -s compiler.libcxx=libc++ ...  # for Apple Silicon
  ```

**Linker warnings about duplicate libraries**

- These warnings from Conan linking multiple libc++ copies are harmless and can be safely ignored
- Set `CMAKE_C_VISIBILITY_PRESET=hidden` if warnings become problematic


Legacy GNU Make build
---------------------

The historical `gmake/Makefile` is kept for reference.
The recommended build path for new work is Conan + CMake.
