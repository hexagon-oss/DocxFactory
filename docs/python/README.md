# DocxFactory Python Documentation

This documentation modernizes the legacy Python tutorial (`docx_factory_install_n_tutorial(Python).pdf`) for the current Conan + CMake workflow in this repository.

## Who this is for

- Python developers generating DOCX files from templates.
- Teams migrating from legacy `/opt/DocxFactory` installs to source builds.
- Users integrating DocxFactory into CI/CD workflows.

## Documentation map

1. [Installation and Build](installation.md)
2. [Hello World Tutorial](tutorial-hello-world.md)
3. [Python API Reference](api-reference.md)
4. [Troubleshooting](troubleshooting.md)

## Quick start

1. Build DocxFactory with Python bindings enabled.
2. Run the hello-world example in [examples/python/hello_world](../../examples/python/hello_world).
3. Adapt the XML payload and DOCX template fields to your own data model.

## Legacy to modern migration

The legacy tutorial described package-style installation and Python module setup under `/opt/DocxFactory`. This repository now uses:

- Conan for C/C++ dependencies.
- CMake for configure/build.
- SWIG for Python wrapper generation.

The Python usage model remains the same: compile template -> load compiled template -> merge XML -> save DOCX.
