from os import system, environ, chdir
from os.path import isfile
import glob

# show checksum
chdir(environ["GITHUB_WORKSPACE"])
files = glob.glob("artifacts/**/*.*", recursive=True)
for file in files:
    if not isfile(file):
        continue
    system("sha1sum " + file + ">>checksum.txt")

print("Checksum:", flush=True)
system("cat checksum.txt")
system("mv checksum.txt artifacts/")