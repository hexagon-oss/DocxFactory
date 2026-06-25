#!/usr/bin/env python3
"""Minimal DocxFactory Python hello-world sample.

Compiles a DOCX template, merges XML payload, and writes output DOCX.
"""

from pathlib import Path
import os
import sys


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _candidate_build_dirs(root: Path) -> list[Path]:
    env_dir = os.environ.get("DOCXFACTORY_BUILD_DIR", "").strip()
    paths: list[Path] = []

    if env_dir:
        paths.append((root / env_dir).resolve())

    paths.extend(
        [
            (root / "build/macos-release").resolve(),
            (root / "build/linux-release").resolve(),
            (root / "build/win-vs2022").resolve(),
        ]
    )
    return paths


def _find_build_dir(root: Path) -> Path:
    for build_dir in _candidate_build_dirs(root):
        if (build_dir / "docxfactory.py").exists() and (build_dir / "python").exists():
            return build_dir
    raise FileNotFoundError(
        "Could not find DocxFactory Python build output. "
        "Build first, then set DOCXFACTORY_BUILD_DIR if needed."
    )


def main() -> int:
    root = _repo_root()
    example_dir = Path(__file__).resolve().parent
    out_dir = example_dir / "out"
    out_dir.mkdir(parents=True, exist_ok=True)

    build_dir = _find_build_dir(root)
    sys.path.insert(0, str(build_dir))
    sys.path.insert(0, str(build_dir / "python"))

    import docxfactory  # pylint: disable=import-error
    

    template_path = example_dir / "input_test_template.docx"
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    payload_path = example_dir / "payload.xml"
    payload_xml = payload_path.read_text(encoding="utf-8")

    compiled_path = out_dir / "hello_world.dfw"
    output_docx = out_dir / "hello_world.docx"

    compiler = docxfactory.WordProcessingCompiler.get_instance()
    merger = docxfactory.WordProcessingMerger.get_instance()

    try:
        compiler.compile(str(template_path), str(compiled_path))
        merger.load(str(compiled_path))
        merger.merge(payload_xml)
        merger.save(str(output_docx))
    finally:
        merger.close()

    print("DocxFactory hello-world completed successfully")
    print(f"Build dir:   {build_dir}")
    print(f"Template:    {template_path}")
    print(f"Payload XML: {payload_xml}")
    print(f"Payload:     {payload_path}")
    print(f"Output DOCX: {output_docx}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
