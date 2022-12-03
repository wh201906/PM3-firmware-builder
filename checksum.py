from os import system, environ, chdir
import glob

# show checksum
chdir(environ["GITHUB_WORKSPACE"])
files = glob.glob("artifacts/**/*.*", recursive=True)
for file in files:
    system("sha1sum " + file + ">>checksum.txt")

print("Checksum:", flush=True)
system("cat checksum.txt")
