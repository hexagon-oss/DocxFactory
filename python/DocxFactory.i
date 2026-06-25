%module docxfactory
%{
#include <DocxFactory/WordProcessingCompiler/WordProcessingCompiler.h>
#include <DocxFactory/WordProcessingMerger/WordProcessingMerger.h>
#include <exception>
%}

%include "python/std_string.i"

%rename ("%(undercase)s") "";
%rename (print_doc) print;

%exception {
	try {
		$action
	} catch ( std::exception &_e ) {
		PyErr_SetString( PyExc_Exception, const_cast<char*>( _e.what() ) );
		return NULL;
	}
}

// Include headers to generate Python bindings
%include <DocxFactory/WordProcessingCompiler/WordProcessingCompiler.h>
%include <DocxFactory/WordProcessingMerger/WordProcessingMerger.h>

%pythoncode %{
from datetime	import datetime, date
from sys		import version_info

# Add convenience methods to WordProcessingMerger
def WordProcessingMerger_set_clipboard_value(self, item_name, field_name, val):
  if val is None: return
  if isinstance(val, datetime) or isinstance(val, date): val = str(val)
  return self.setClipboardValue(item_name, field_name, val)

def WordProcessingMerger_set_chart_value(self, item_name, field_name, series, category, val):
  if category is None: return
  if isinstance(category, datetime) or isinstance(category, date): category = str(category)
  if isinstance(val, datetime) or isinstance(val, date): val = str(val)
  # Try different overloads based on argument types
  try:
    # Try string, string, string, string, double
    return self.setChartValue(item_name, field_name, series, category, float(val))
  except:
    try:
      # Try string, string, string, double, double
      return self.setChartValue(item_name, field_name, series, float(category), float(val))
    except:
      # Try string, string, double, double, double
      return self.setChartValue(item_name, field_name, float(series), float(category), float(val))

try:
  # SWIG emits snake_case class names because of the %(undercase)s rename rule.
  # Keep CamelCase aliases for compatibility with existing wrappers/user code.
  WordProcessingCompiler = word_processing_compiler
  WordProcessingMerger = word_processing_merger

  word_processing_merger.set_clipboard_value = WordProcessingMerger_set_clipboard_value
  word_processing_merger.set_chart_value = WordProcessingMerger_set_chart_value

  WordProcessingMerger.set_clipboard_value = WordProcessingMerger_set_clipboard_value
  WordProcessingMerger.set_chart_value = WordProcessingMerger_set_chart_value
except:
  pass
%}
