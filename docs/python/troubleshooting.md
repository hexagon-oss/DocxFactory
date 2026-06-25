# Python Troubleshooting

## CMake cannot find Boost

Symptom:

- `Could not find a package configuration file provided by "Boost"`

Fix:

1. Run `conan install` for the same build folder.
2. Use `-DCMAKE_TOOLCHAIN_FILE=.../conan_toolchain.cmake` in CMake configure.
3. Do not use placeholder paths like `build/...`.

## `argument -o/--options: expected one argument`

Root cause:

- Shell interpreted unquoted `&` in Conan options.

Fix:

- Quote options: `-o '&:with_uno=False'`

## Python import fails (`No module named docxfactory`)

Fix:

1. Ensure build finished with `DOCXFACTORY_BUILD_PYTHON=ON`.
2. Add both paths to `sys.path`:
   - `build/<cfg>`
   - `build/<cfg>/python`
3. Confirm generated files exist.

## SWIG not found

Fix:

- Install SWIG and ensure it is in `PATH`.
- macOS: `brew install swig`
- Linux: `apt install swig`

## CTest says "No tests were found!!!"

This is informational in current repository state and does not mean build failure.

## Build folder deleted accidentally

If `build/<cfg>` is removed, regenerate Conan files:

```bash
conan install . -of build/<cfg> -s build_type=Release -o '&:with_uno=False' -o '&:with_python=True' -o '&:with_imagemagick=False' --build=missing
```
