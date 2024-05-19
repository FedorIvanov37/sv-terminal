from os import chdir, getcwd

print(getcwd())

from common.lib.enums.ReleaseDefinition import ReleaseDefinition

WORKDIR = "build"
OUTPUT_FILE = "version_info.rc"
VERSION_INFO = f"""
1 VERSIONINFO
FILEVERSION 0,0,0,{ReleaseDefinition.VERSION_NUMBER}
PRODUCTVERSION 0,0,0,{ReleaseDefinition.VERSION_NUMBER}
FILEOS 0x40004
FILETYPE 0x1
{{
BLOCK "StringFileInfo"
{{
	BLOCK "040904B0"
	{{
		VALUE "FileDescription", "Signal executable file"
		VALUE "InternalName", "{ReleaseDefinition.NAME}.exe"
		VALUE "OriginalFilename", "{ReleaseDefinition.NAME}.exe"
		VALUE "CompanyName", ""
		VALUE "LegalCopyright", "{r'\xA9'} Developed by Fedor Ivanov"
		VALUE "ProductName", "{ReleaseDefinition.NAME.upper()}"
		VALUE "FileVersion", "{ReleaseDefinition.VERSION}"
		VALUE "ProductVersion", "{ReleaseDefinition.VERSION}"
	}}
}}

BLOCK "VarFileInfo"
{{
	VALUE "Translation", 0x0409 0x04B0  
}}
}}   
"""

chdir(WORKDIR)

with open(OUTPUT_FILE, 'w') as output_file:
    output_file.write(VERSION_INFO)
