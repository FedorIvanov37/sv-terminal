from os import listdir, path, remove, chdir, mkdir
from shutil import rmtree


WORKDIR = "build"
CLEANUP_DIRS = ["common/log", "common/data/spec_backup", "release"]
CLEANUP_FILES = ["common/data/license/license_info.json"]


chdir(WORKDIR)


for directory in CLEANUP_DIRS:
    if not path.isdir(directory):
        mkdir(directory)

    for file in listdir(directory):

        file_path = path.join(directory, file)

        try:
            if path.isfile(file_path):
                remove(file_path)

            if path.isdir(file_path):
                rmtree(file_path)

        except FileNotFoundError:
            mkdir(file_path)


for file_path in CLEANUP_FILES:

    if not path.isfile(file_path):
        continue

    remove(file_path)
