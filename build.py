from os import system, environ, chdir
import json
import glob

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
# iterate all refs
for ref in conf["refs"]:
    refPath = "pm3-" + ref
    chdir(environ["GITHUB_WORKSPACE"])
    print("Cloning", refPath, flush=True)
    system(
        "git -c advice.detachedHead=false"
        " clone " + URL + " --depth=1 -b " + ref + " " + refPath
    )
    chdir(refPath)

    # itarate all standalone mode
    for standalone in conf["standaloneList"]:
        print("Building firmware for", standalone, flush=True)
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
        outputPath = "../artifacts/" + ref + "/" + standalone + "/"
        system("mkdir -p " + outputPath)
        system("mv bootrom/obj/bootrom.elf " + outputPath)
        system("mv armsrc/obj/fullimage.elf " + outputPath)
        # collect .s19 file
        if conf["buildS19"]:
            system("mv bootrom/obj/bootrom.s19 " + outputPath)
            system("mv armsrc/obj/fullimage.s19 " + outputPath)
