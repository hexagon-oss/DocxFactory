# Hello World Tutorial (Field Substitution)

This tutorial demonstrates the core DocxFactory pipeline using Python:

1. Compile a DOCX template into `.dfw`
2. Merge XML data
3. Save a final DOCX

The provided executable sample is in [examples/python/hello_world](../../examples/python/hello_world).

## Template used in this repo

The example uses `input_test_template.docx` from the repository root. That template contains these fields:

- `{first_name}`
- `{last_name}`

## XML payload

Use this structure:

```xml
<root>
  <first_name>John</first_name>
  <last_name>Smith</operatfirst_name>
</root>
```

## Run the example

From repository root:

```bash
python3 examples/python/hello_world/run_hello_world.py
```

Default output:

- `examples/python/hello_world/out/hello_world.docx`

## How the code works

- `WordProcessingCompiler.get_instance()` compiles the DOCX template once into `.dfw`.
- `WordProcessingMerger.get_instance()` loads `.dfw`, merges XML, and saves output.
- `merger.close()` releases resources.

## Production best practices

- Compile templates during deployment or startup, not on every request.
- Keep template files versioned and immutable.
- Validate incoming XML against expected schema/shape.
- Always call `close()` in `finally` blocks in long-running services.
- Use absolute paths in server processes.
- Generate outputs in per-request temp directories to avoid collisions.

## Customizing for your own template

1. Create a DOCX with your own placeholders (for example `{customer_name}`).
2. Change template path in the example script.
3. Update payload XML to include matching element names.
4. Re-run script and inspect generated DOCX.
