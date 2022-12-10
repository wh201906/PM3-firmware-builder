from os import system, environ, chdir
import json
import glob
from subprocess import run, PIPE

URL = "https://github.com/RfidResearchGroup/proxmark3.git"

# load config file
confFile = open("config.json")
conf = json.load(confFile)
confFile.close()


def validKey(name: str):
    if name in conf.keys() and len(conf[name]) > 0:
        return True
    else:
        return False


# `system(cd)` doesn't work there
ref = environ["MATRIX_REF"]
refPath = "pm3-" + ref
chdir(environ["GITHUB_WORKSPACE"])
print("Cloning", refPath, flush=True)
system(
    "git -c advice.detachedHead=false"
    " clone " + URL + " --depth=1 -b " + ref + " " + refPath
)
chdir(refPath)

# save commit SHA1
sha1 = run("git rev-parse HEAD", shell=True, stdout=PIPE).stdout
sha1 = sha1.decode("utf-8").strip()
print(sha1, flush=True)
system("mkdir -p ../artifacts/" + ref)
system("touch ../artifacts/" + ref + "/" + sha1 + ".txt")

standalone = environ["MATRIX_STANDALONE"]
modeName = standalone if len(standalone) != 0 else "empty"
print("Building firmware for standalone mode:", modeName, flush=True)

# clean
system("make clean 1> /dev/null")

# build
buildCmd = "make -j"
buildCmd += " STANDALONE=" + standalone

if validKey("PLATFORM"):
    buildCmd += " PLATFORM=" + conf["PLATFORM"]
if validKey("PLATFORM_EXTRAS"):
    buildCmd += " PLATFORM_EXTRAS=" + conf["PLATFORM_EXTRAS"]
if validKey("PLATFORM_SIZE"):
    buildCmd += " PLATFORM_SIZE=" + conf["PLATFORM_SIZE"]
for option in conf["extraOptions"]:
    buildCmd += " " + option + "=1"

buildCmd += " bootrom fullimage"
system(buildCmd)

# collect generated files
outputPath = "../artifacts/" + ref + "/" + modeName + "/"
system("mkdir -p " + outputPath)
system("mv bootrom/obj/bootrom.elf " + outputPath)
system("mv armsrc/obj/fullimage.elf " + outputPath)

# collect .s19 files
if conf["buildS19"]:
    system("mv bootrom/obj/bootrom.s19 " + outputPath)
    system("mv armsrc/obj/fullimage.s19 " + outputPath)
