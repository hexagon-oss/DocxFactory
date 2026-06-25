cmake_minimum_required(VERSION 3.21)

project(DocxFactory VERSION 2.0.0 LANGUAGES C CXX)

include(CTest)
include(GNUInstallDirs)

option(DOCXFACTORY_NO_PNG "Define NO_PNG for legacy image pipeline behavior" ON)
option(DOCXFACTORY_BUILD_TOOLS "Build word-processing tools" ON)
option(DOCXFACTORY_ENABLE_UNO "Build UNO/OpenOffice bridge" OFF)
option(DOCXFACTORY_BUILD_PYTHON "Build Python 3 SWIG module" ON)
option(DOCXFACTORY_WITH_IMAGEMAGICK "Enable ImageMagick-based image conversion" OFF)

set(CMAKE_C_STANDARD 99)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

if(MSVC)
  add_compile_options(/permissive- /bigobj)
else()
  add_compile_options(-fpermissive)
endif()

if(DOCXFACTORY_NO_PNG)
  add_compile_definitions(NO_PNG)
endif()

if(DOCXFACTORY_WITH_IMAGEMAGICK)
  add_compile_definitions(DOCXFACTORY_WITH_IMAGEMAGICK=1)
else()
  add_compile_definitions(DOCXFACTORY_WITH_IMAGEMAGICK=0)
endif()

# Conan CMakeDeps / CMakeToolchain dependency resolution.
find_package(Boost REQUIRED CONFIG)
find_package(ICU REQUIRED CONFIG)
find_package(XercesC REQUIRED CONFIG)
find_package(minizip REQUIRED CONFIG)
find_package(Zint REQUIRED CONFIG)
find_package(ZLIB REQUIRED CONFIG)
find_package(RapidJSON REQUIRED CONFIG)

if(DOCXFACTORY_WITH_IMAGEMAGICK)
  find_package(ImageMagick REQUIRED)
endif()

file(GLOB DOCXFACTORY_BARCODE_SOURCES CONFIGURE_DEPENDS src/barcode/*.cpp)
file(GLOB DOCXFACTORY_CONSOLE_CPP_SOURCES CONFIGURE_DEPENDS src/console/*.cpp)
file(GLOB DOCXFACTORY_CONSOLE_C_SOURCES CONFIGURE_DEPENDS src/console/*.c)
file(GLOB DOCXFACTORY_JSON_SOURCES CONFIGURE_DEPENDS src/json/*.cpp)
file(GLOB DOCXFACTORY_LOCALE_SOURCES CONFIGURE_DEPENDS src/locale/*.cpp)
file(GLOB DOCXFACTORY_MATH_SOURCES CONFIGURE_DEPENDS src/math/*.cpp)
file(GLOB DOCXFACTORY_OS_SOURCES CONFIGURE_DEPENDS src/os/*.cpp)
file(GLOB DOCXFACTORY_PARSER_SOURCES CONFIGURE_DEPENDS src/parser/*.cpp)
file(GLOB DOCXFACTORY_STR_SOURCES CONFIGURE_DEPENDS src/str/*.cpp)
file(GLOB DOCXFACTORY_TIME_SOURCES CONFIGURE_DEPENDS src/time/*.cpp)
file(GLOB DOCXFACTORY_UTIL_SOURCES CONFIGURE_DEPENDS src/util/*.cpp)
file(GLOB DOCXFACTORY_XML_SOURCES CONFIGURE_DEPENDS src/xml/*.cpp)
file(GLOB DOCXFACTORY_ZIP_SOURCES CONFIGURE_DEPENDS src/zip/*.cpp)

set(DOCXFACTORY_PLATFORM_SOURCES)
if(WIN32)
  list(APPEND DOCXFACTORY_PLATFORM_SOURCES src/win/WinFunc.cpp)
else()
  list(APPEND DOCXFACTORY_PLATFORM_SOURCES src/unix/UnixFunc.cpp)
endif()

set(DOCXFACTORY_LIB_SOURCES
  ${DOCXFACTORY_BARCODE_SOURCES}
  ${DOCXFACTORY_CONSOLE_CPP_SOURCES}
  ${DOCXFACTORY_CONSOLE_C_SOURCES}
  ${DOCXFACTORY_JSON_SOURCES}
  ${DOCXFACTORY_LOCALE_SOURCES}
  ${DOCXFACTORY_MATH_SOURCES}
  ${DOCXFACTORY_OS_SOURCES}
  ${DOCXFACTORY_PARSER_SOURCES}
  ${DOCXFACTORY_STR_SOURCES}
  ${DOCXFACTORY_TIME_SOURCES}
  ${DOCXFACTORY_UTIL_SOURCES}
  ${DOCXFACTORY_XML_SOURCES}
  ${DOCXFACTORY_ZIP_SOURCES}
  ${DOCXFACTORY_PLATFORM_SOURCES}
)

file(GLOB DOCXFACTORY_WORD_PROCESSING_COMPILER_SOURCES CONFIGURE_DEPENDS src/WordProcessingCompiler/*.cpp)
file(GLOB DOCXFACTORY_WORD_PROCESSING_MERGER_SOURCES CONFIGURE_DEPENDS src/WordProcessingMerger/*.cpp)
file(GLOB DOCXFACTORY_DOCX_COMPILER_SOURCES CONFIGURE_DEPENDS src/DocxCompiler/*.cpp)
file(GLOB DOCXFACTORY_DOCX_MERGER_SOURCES CONFIGURE_DEPENDS src/DocxMerger/*.cpp)
file(GLOB DOCXFACTORY_OPC_SOURCES CONFIGURE_DEPENDS src/opc/*.cpp)

set(DOCXFACTORY_TOOL_MAINS
  src/WordProcessingCompiler/word-processing-compiler.cpp
  src/WordProcessingMerger/word-processing-merger.cpp
)

list(REMOVE_ITEM DOCXFACTORY_WORD_PROCESSING_COMPILER_SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/src/WordProcessingCompiler/word-processing-compiler.cpp)
list(REMOVE_ITEM DOCXFACTORY_WORD_PROCESSING_MERGER_SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/src/WordProcessingMerger/word-processing-merger.cpp)

set(DOCXFACTORY_CONVERTER_SOURCES
  src/ConverterPrinter/ConversionNotSupportedException.cpp
  src/ConverterPrinter/ConverterPrinter.cpp
  src/ConverterPrinter/ConverterPrinterException.cpp
  src/ConverterPrinter/ExportFormatNotSupportedException.cpp
  src/ConverterPrinter/GradeGroup.cpp
  src/ConverterPrinter/OdfConverterUtil.cpp
  src/ConverterPrinter/PrintingNotSupportedException.cpp
  src/ConverterPrinter/UtilFailedException.cpp
  src/ConverterPrinter/UtilNotFoundException.cpp
)

if(WIN32)
  list(APPEND DOCXFACTORY_CONVERTER_SOURCES
    src/ConverterPrinter/OleException.cpp
    src/ConverterPrinter/MsOfficeUtil.cpp
    src/ConverterPrinter/MsWordUtil.cpp
    src/ConverterPrinter/MsExcelUtil.cpp
  )
endif()

if(DOCXFACTORY_ENABLE_UNO)
  add_compile_definitions(DOCXFACTORY_ENABLE_UNO=1)
  list(APPEND DOCXFACTORY_CONVERTER_SOURCES src/ConverterPrinter/OpenOfficeUtil.cpp)

  file(GLOB DOCXFACTORY_UNO_SOURCES CONFIGURE_DEPENDS src/UnoUtil/*.cpp)
  add_library(UnoUtil SHARED ${DOCXFACTORY_UNO_SOURCES})
  target_include_directories(UnoUtil
    PUBLIC
      ${CMAKE_CURRENT_SOURCE_DIR}/include
  )
  target_link_libraries(UnoUtil
    PRIVATE
      ZLIB::ZLIB
      minizip::minizip
      icu::icu
      XercesC::XercesC
      Zint::Zint
  )

  if(DOCXFACTORY_WITH_IMAGEMAGICK)
    target_include_directories(UnoUtil PRIVATE ${ImageMagick_INCLUDE_DIRS})
    target_link_libraries(UnoUtil PRIVATE ${ImageMagick_LIBRARIES})
  endif()

  if(UNIX AND NOT APPLE)
    target_compile_definitions(UnoUtil PRIVATE UNX GCC LINUX CPPU_ENV=gcc3)
  endif()
else()
  add_compile_definitions(DOCXFACTORY_ENABLE_UNO=0)
endif()

add_library(DocxFactoryLib SHARED ${DOCXFACTORY_LIB_SOURCES})
add_library(DocxFactory SHARED
  ${DOCXFACTORY_CONVERTER_SOURCES}
  ${DOCXFACTORY_OPC_SOURCES}
  ${DOCXFACTORY_WORD_PROCESSING_COMPILER_SOURCES}
  ${DOCXFACTORY_WORD_PROCESSING_MERGER_SOURCES}
  ${DOCXFACTORY_DOCX_COMPILER_SOURCES}
  ${DOCXFACTORY_DOCX_MERGER_SOURCES}
)

set_target_properties(DocxFactoryLib PROPERTIES OUTPUT_NAME DocxFactoryLib)
set_target_properties(DocxFactory PROPERTIES OUTPUT_NAME DocxFactory)

target_include_directories(DocxFactoryLib
  PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_include_directories(DocxFactory
  PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}/include/DocxFactory/WordProcessingCompiler
    ${CMAKE_CURRENT_SOURCE_DIR}/include/DocxFactory/WordProcessingMerger
)

target_link_libraries(DocxFactoryLib
  PUBLIC
    boost::boost
    icu::icu
    XercesC::XercesC
    ZLIB::ZLIB
    minizip::minizip
    Zint::Zint
    rapidjson
)

if(DOCXFACTORY_WITH_IMAGEMAGICK)
  target_include_directories(DocxFactoryLib PRIVATE ${ImageMagick_INCLUDE_DIRS})
  target_link_libraries(DocxFactoryLib PUBLIC ${ImageMagick_LIBRARIES})
endif()

target_link_libraries(DocxFactory
  PUBLIC
    DocxFactoryLib
)

if(WIN32)
  target_link_libraries(DocxFactoryLib PUBLIC ole32 oleaut32 shlwapi)
endif()

if(DOCXFACTORY_BUILD_TOOLS)
  add_executable(word-processing-compiler src/WordProcessingCompiler/word-processing-compiler.cpp)
  target_link_libraries(word-processing-compiler PRIVATE DocxFactory DocxFactoryLib)
  target_include_directories(word-processing-compiler PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include)

  add_executable(word-processing-merger src/WordProcessingMerger/word-processing-merger.cpp)
  target_link_libraries(word-processing-merger PRIVATE DocxFactory DocxFactoryLib)
  target_include_directories(word-processing-merger PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include)
endif()

if(DOCXFACTORY_BUILD_PYTHON)
  find_package(SWIG QUIET)
  find_package(Python3 COMPONENTS Interpreter Development.Module QUIET)

  if(SWIG_FOUND AND Python3_FOUND)
    include(UseSWIG)

    set_source_files_properties(
      python/DocxFactory.i
      PROPERTIES
        CPLUSPLUS ON
        SWIG_INCLUDE_DIRECTORIES "${CMAKE_CURRENT_SOURCE_DIR}/include"
        SWIG_FLAGS "-I${CMAKE_CURRENT_SOURCE_DIR}/include"
    )

    swig_add_library(docxfactory_swig
      TYPE MODULE
      LANGUAGE python
      SOURCES python/DocxFactory.i
    )

    set_property(
      TARGET ${SWIG_MODULE_docxfactory_swig_REAL_NAME}
      PROPERTY SWIG_USE_TARGET_INCLUDE_DIRECTORIES TRUE
    )

    target_include_directories(${SWIG_MODULE_docxfactory_swig_REAL_NAME}
      PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/include
        ${Python3_INCLUDE_DIRS}
    )

    target_link_libraries(${SWIG_MODULE_docxfactory_swig_REAL_NAME}
      PRIVATE
        DocxFactory
        DocxFactoryLib
        Python3::Module
    )

    set_target_properties(${SWIG_MODULE_docxfactory_swig_REAL_NAME}
      PROPERTIES
        OUTPUT_NAME docxfactory
        LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/python
    )
  else()
    message(WARNING "DOCXFACTORY_BUILD_PYTHON=ON but SWIG or Python3 dev files were not found. Skipping Python module build.")
  endif()
endif()

install(TARGETS DocxFactoryLib DocxFactory
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)

if(DOCXFACTORY_ENABLE_UNO)
  install(TARGETS UnoUtil
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
  )
endif()

if(DOCXFACTORY_BUILD_TOOLS)
  install(TARGETS word-processing-compiler word-processing-merger
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
  )
endif()

install(
  DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/include/DocxFactory
  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)
