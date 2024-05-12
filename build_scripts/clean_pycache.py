from os import listdir, path, chdir
from shutil import rmtree


REMOVE_DIR = "__pycache__"
WORKDIR = "build/release/common/src"


def clean(parent_dir):

    for file in listdir(parent_dir):
        file_path = path.join(parent_dir, file)

        if not path.isdir(file_path):
            continue

        if not file == REMOVE_DIR:
            clean(file_path)
            continue

        rmtree(file_path)


clean(WORKDIR)
