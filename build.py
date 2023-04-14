from os import system, environ, chdir, path
import sys
import json
import glob
from subprocess import run, PIPE


# load config file
confFile = open("config.json")
conf = json.load(confFile)
confFile.close()


def validKey(name: str):
    if name in conf.keys() and len(conf[name]) > 0:
        return True
    else:
        return False


URL = "https://github.com/RfidResearchGroup/proxmark3.git"

if validKey("URL"):
    URL = environ["URL"]

# `system("cd")` doesn't work there
ref = environ["MATRIX_REF"]
refPath = "pm3-" + ref
chdir(environ["GITHUB_WORKSPACE"])
print("Cloning", refPath, flush=True)
system(
    "git -c advice.detachedHead=false"
    " clone " + URL + " --depth=1 -b " + ref + " " + refPath
)
if not path.exists("./" + refPath):  # failed to clone the branch
    system("git clone " + URL + " " + refPath)
    chdir(refPath)
    system("git -c advice.detachedHead=false checkout " + ref)
else:
    chdir(refPath)

# save commit SHA1
sha1 = run("git rev-parse HEAD", shell=True, stdout=PIPE).stdout
sha1 = sha1.decode("utf-8").strip()
print(sha1, flush=True)
system("mkdir -p ../artifacts/" + ref)
system("touch ../artifacts/" + sha1 + ".txt")

standalone = environ["MATRIX_STANDALONE"]
modeName = standalone if len(standalone) != 0 else "empty"
print("Building firmware for standalone mode:", modeName, flush=True)

# detect using PLATFORM=PM3GENERIC or PLATFORM=PM3OTHER
oldVersion = True
with open("Makefile.platform.sample", "r") as sample:
    text = sample.readline()
    while text:
        if "PM3GENERIC" in text:
            oldVersion = False
            break
        text = sample.readline()

# generate Makefile.platform
with open("Makefile.platform", "w+") as mp:
    mp.write("STANDALONE=" + standalone + "\n")
    if validKey("PLATFORM"):
        platform = conf["PLATFORM"]
        if oldVersion and platform == "PM3GENERIC":
            platform = "PM3OTHER"
        mp.write("PLATFORM=" + platform + "\n")
    if validKey("PLATFORM_EXTRAS"):
        mp.write("PLATFORM_EXTRAS=" + conf["PLATFORM_EXTRAS"] + "\n")
    if validKey("PLATFORM_SIZE"):
        mp.write("PLATFORM_SIZE=" + conf["PLATFORM_SIZE"] + "\n")
    if validKey("extraOptions"):
        for option in conf["extraOptions"]:
            mp.write(option + "=1\n")
    if validKey("extraLines"):
        for line in conf["extraLines"]:
            mp.write(line + "\n")

# clean
system("make clean -j 1> /dev/null")

# build
system("make -j bootrom fullimage")

# check the build result
checkPath = "./bootrom/obj/bootrom.elf"
if not path.exists(checkPath):
    print(checkPath + " doesn't exist, Exiting...", flush=True)
    sys.exit(-1)

# collect generated files
outputPath = "../artifacts/"
system("mkdir -p " + outputPath)
system("mv bootrom/obj/bootrom.elf " + outputPath)
system("mv armsrc/obj/fullimage.elf " + outputPath)

# collect .s19 files
if conf["buildS19"]:
    system("mv bootrom/obj/bootrom.s19 " + outputPath)
    system("mv armsrc/obj/fullimage.s19 " + outputPath)

# collect Makefile.platform
system("mv ./Makefile.platform " + outputPath)
