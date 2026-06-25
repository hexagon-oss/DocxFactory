
#ifndef __DOCXFACTORY_FILE_INFO_H__
#define __DOCXFACTORY_FILE_INFO_H__

#if defined(__has_include)
  #if __has_include("zlib/zip.h")
    #include "zlib/zip.h"
    #include "zlib/unzip.h"
  #elif __has_include("minizip/zip.h")
    #include "minizip/zip.h"
    #include "minizip/unzip.h"
  #else
    #include "zip.h"
    #include "unzip.h"
  #endif
#else
  #include "zlib/zip.h"
  #include "zlib/unzip.h"
#endif



namespace DocxFactory
{
	using namespace std;

	class FileInfo
	{
	public:
		FileInfo( unz_file_info p_unzFileInfo );
		virtual ~FileInfo();

		const unz_file_info* getUnzFileInfo()	const;
		const zip_fileinfo* getZipFileInfo()	const;

	protected:

	private:
		FileInfo( const FileInfo& p_other );
		FileInfo operator = ( const FileInfo& p_other );

		unz_file_info	m_unzFileInfo;
		zip_fileinfo	m_zipFileInfo;
	};
};

#endif
