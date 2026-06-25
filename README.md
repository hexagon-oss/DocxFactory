DocxFactory Project
===================

Description
-----------

[DocxFactory](http://docxfactory.com) is a free, cross platform C/C++ library with C#, Java, Python, Progress 4GL wrappers
and command line tools for generating ([Microsoft Word .DOCX](https://de.wikipedia.org/wiki/Office_Open_XML)) files (also called Open XML).

**DocxFactory Features:** [http://docxfactory.com](http://docxfactory.com)

**DocxFactory Tutorials (PDF):** [http://docxfactory.com/tutorial](http://docxfactory.com/tutorial)

**Download the binaries for your operating system:** [http://docxfactory.com/free-download](http://docxfactory.com/free-download)

**Installation:** For information on how to install DocxFactory on your operating system, see the Installation chapter included in all of the tutorials.

Compiling DocxFactory and high-level language wrappers
------------------------------------------------------

Read the [compilation instructions](https://github.com/DocxFactory/DocxFactory/blob/master/COMPILING.md)


Python SWIG Quick Start
-----------------------

Build with Conan + CMake (macOS example):

```bash
conan profile detect --force
conan install . -of build/macos-release -s build_type=Release -o '&:with_uno=False' -o '&:with_imagemagick=False' --build=missing

cmake -S . -B build/macos-release \
	-DCMAKE_TOOLCHAIN_FILE=build/macos-release/build/Release/generators/conan_toolchain.cmake \
	-DCMAKE_BUILD_TYPE=Release \
	-DDOCXFACTORY_BUILD_PYTHON=ON

cmake --build build/macos-release --config Release -j
```

Linux variant:

```bash
conan profile detect --force
conan install . -of build/linux-release -s build_type=Release -o '&:with_uno=False' -o '&:with_imagemagick=False' --build=missing

cmake -S . -B build/linux-release \
	-DCMAKE_TOOLCHAIN_FILE=build/linux-release/build/Release/generators/conan_toolchain.cmake \
	-DCMAKE_BUILD_TYPE=Release \
	-DDOCXFACTORY_BUILD_PYTHON=ON

cmake --build build/linux-release --config Release -j
```

Python import/use example:

```python
import sys

sys.path.insert(0, "build/macos-release")
sys.path.insert(0, "build/macos-release/python")

import docxfactory

compiler = docxfactory.WordProcessingCompiler.get_instance()
compiler.compile("input_template.docx", "compiled_template.dfw")

merger = docxfactory.WordProcessingMerger.get_instance()
merger.load("compiled_template.dfw")
merger.merge("<root><name>Example</name></root>")
merger.save("output.docx")
merger.close()
```

For Linux builds, replace `build/macos-release` with `build/linux-release` in the two `sys.path.insert(...)` lines above.

Notes:

- Generated artifacts are `build/<cfg>/docxfactory.py` and `build/<cfg>/python/_docxfactory.so`.
- The API is singleton-style and uses `get_instance()`.
- Snake case names are also available (`word_processing_compiler`, `word_processing_merger`).

Python Documentation and Examples
---------------------------------

- In-depth Python docs: [docs/python/README.md](docs/python/README.md)
- Hello-world executable example: [examples/python/hello_world/README.md](examples/python/hello_world/README.md)


History
-------

Read the [changelog](https://github.com/DocxFactory/DocxFactory/blob/master/CHANGELOG.md)


Author and License
------------------

DocxFactory is copyrighted by [Alon Blich](mailto:alonb@docxfactory.com) and licensed under the
[Apache 2.0 license.](https://www.apache.org/licenses/LICENSE-2.0)


Third Party / Licenses Acknowledgement
--------------------------------------

Microsoft Office and Word are registered trademarks of Microsoft Corporation.

DocxFactory only includes third party components that have a permissive free license.

Please see the [third party / licenses acknowledgement.](https://github.com/DocxFactory/DocxFactory/blob/master/LICENSE-3RD-PARTY.md)
