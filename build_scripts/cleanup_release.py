from os import listdir, path, remove, chdir
from shutil import rmtree


WORKDIR = "build"
CLEANUP_DIRS = ["common/log", "common/data/spec_backup"]
CLEANUP_FILES = ["common/data/license/license_info.json"]


chdir(WORKDIR)


for directory in CLEANUP_DIRS:
    for file in listdir(directory):
        file_path = path.join(directory, file)

        if path.isfile(file_path):
            remove(file_path)

        if path.isdir(file_path):
            rmtree(file_path)


for file_path in CLEANUP_FILES:

    if not path.isfile(file_path):
        continue

    remove(file_path)
