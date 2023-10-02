import json
from os import environ

confFile = open("config.json")
conf = json.load(confFile)
confFile.close()

with open(environ["GITHUB_OUTPUT"], "a") as f:
    # the keys there matches the keys in jobs->load_conf->outputs of build.yml 
    f.write("refs=" + str(conf["refs"]) + "\n")
    standaloneList = conf["standaloneList"]
    if len(standaloneList) == 0:
        standaloneList = ["empty"]
    f.write("standalones=" + str(standaloneList) + "\n")
