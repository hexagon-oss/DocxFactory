# Python Hello World Example

This example demonstrates simple field substitution with DocxFactory Python bindings.

## What it does

1. Compiles `input_test_template.docx` into `hello_world.dfw`
2. Merges XML payload from `payload.xml`
3. Produces `out/hello_world.docx`

The template fields in `input_test_template.docx` are:

- `{first_name}`
- `{last_name}`

## Prerequisites

- Build DocxFactory with Python enabled (`DOCXFACTORY_BUILD_PYTHON=ON`)
- Ensure one of these build folders exists:
  - `build/macos-release`
  - `build/linux-release`
  - `build/win-vs2022`

## Run

From repository root:

```bash
python3 examples/python/hello_world/run_hello_world.py
```

Optional overrides:

```bash
DOCXFACTORY_BUILD_DIR=build/macos-release \
DOCXFACTORY_TEMPLATE=input_test_template.docx \
python3 examples/python/hello_world/run_hello_world.py
```
