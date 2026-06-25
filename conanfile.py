from conan import ConanFile
from conan.tools.cmake import CMakeDeps, CMakeToolchain, cmake_layout


class DocxFactoryDependenciesConan(ConanFile):
    name = "docxfactory-dependencies"
    version = "1.0"

    settings = "os", "compiler", "build_type", "arch"

    options = {
        "with_uno": [True, False],
        "with_python": [True, False],
        "with_imagemagick": [True, False],
    }
    default_options = {
        "with_uno": False,
        "with_python": True,
        "with_imagemagick": False,
    }

    requires = (
        "boost/1.86.0",
        "icu/76.1",
        "xerces-c/3.2.5",
        "zlib/1.3.1",
        "minizip/1.3.2",
        "zint/2.10.0",
        "rapidjson/1.1.0",
    )

    generators = ()

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()

        tc = CMakeToolchain(self)
        tc.variables["DOCXFACTORY_ENABLE_UNO"] = bool(self.options.with_uno)
        tc.variables["DOCXFACTORY_BUILD_PYTHON"] = bool(self.options.with_python)
        tc.variables["DOCXFACTORY_WITH_IMAGEMAGICK"] = bool(self.options.with_imagemagick)
        tc.generate()
