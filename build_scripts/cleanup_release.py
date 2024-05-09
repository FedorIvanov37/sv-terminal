from os import chdir, listdir, unlink

WORKDIR = "build"

chdir(WORKDIR)

for file in listdir('.'):
    if file == "messages":
        unlink(file)
