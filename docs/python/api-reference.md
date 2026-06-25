# Python API Reference (Core)

DocxFactory's Python binding is generated through SWIG and exposes singleton-style classes.

## Imports

```python
import docxfactory
```

Both naming styles are available:

- CamelCase: `WordProcessingCompiler`, `WordProcessingMerger`
- snake_case: `word_processing_compiler`, `word_processing_merger`

## WordProcessingCompiler

### get_instance()

Returns the compiler singleton.

```python
compiler = docxfactory.WordProcessingCompiler.get_instance()
```

### compile(src_docx, dst_dfw)

Compiles a DOCX template into DocxFactory's compiled format.

```python
compiler.compile("template.docx", "template.dfw")
```

## WordProcessingMerger

### get_instance()

Returns the merger singleton.

```python
merger = docxfactory.WordProcessingMerger.get_instance()
```

### load(dfw_path)

Loads a compiled template.

```python
merger.load("template.dfw")
```

### merge(xml_payload)

Merges XML payload into the loaded template.

```python
merger.merge("<root><name>Alice</name></root>")
```

### save(output_docx[, optional_flags...])

Writes merged content into a DOCX file.

```python
merger.save("output.docx")
```

### close()

Closes and resets merger state.

```python
merger.close()
```

### Additional convenience methods

Depending on template usage, the wrapper also exposes methods such as:

- `set_clipboard_value(...)`
- `set_chart_value(...)`
- `paste(...)`

These are useful for advanced templates using clipboard regions or chart data.

## Error model

C++ exceptions are converted into Python `Exception` objects. Wrap compile/merge/save logic in try/except.

```python
try:
    compiler.compile("template.docx", "template.dfw")
except Exception as exc:
    print(f"DocxFactory error: {exc}")
```
