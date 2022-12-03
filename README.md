# PM3 Firmware Builder

Build multiple firmwares of Proxmark3 RRG repo by GitHub Action.  

## Usage
1. Fork this repo
2. Go to `Actions` then enable it.
3. Change the `config.json`
4. Push a commit or click `Run workflow` in `Actions`
5. Check and download the firmwares in `Actions`->the latest workflow run->`Artifacts`

## Examples of `config.json`

### Build the latest firmware of Proxmark3 RDV4 with `LF_SAMYRUN` standalone mode
```
{
    "refs": ["master"],
    "standaloneList": ["LF_SAMYRUN"],
    "PLATFORM": "",
    "PLATFORM_EXTRAS": "",
    "PLATFORM_SIZE": "",
    "extraOptions": [],
    "buildS19": true
}
```

### Build `v4.15864` of Proxmark3 generic firmware with `HF_14ASNIFF` standalone mode
```
{
    "refs": ["v4.15864"],
    "standaloneList": ["HF_14ASNIFF"],
    "PLATFORM": "PM3GENERIC",
    "PLATFORM_EXTRAS": "",
    "PLATFORM_SIZE": "",
    "extraOptions": [],
    "buildS19": true
}
```

### Build 18 sets of firmwares in one run
```
{
    "//": "You will get len(refs) * len(standaloneList) firmwares",
    "refs": [
        "master",
        "v4.15864",
        "v4.13441"
    ],
    "standaloneList": [
        "HF_14ASNIFF",
        "LF_SAMYRUN",
        "LF_EM4100EMUL",
        "LF_EM4100RSWB",
        "LF_EM4100RSWW",
        "LF_EM4100RWC"
    ],
    "PLATFORM": "PM3GENERIC",
    "PLATFORM_EXTRAS": "",
    "PLATFORM_SIZE": "",
    "extraOptions": [],
    "buildS19": true
}
```

### Build firmware for Proxmark3 generic target with 256K RAM
[config described there](https://github.com/RfidResearchGroup/proxmark3/blob/master/doc/md/Use_of_Proxmark/4_Advanced-compilation-parameters.md#256kb-versions)  

(no standalone mode, no hitag, no felica)  
```
{
    "//": "You will get len(refs) * len(standaloneList) firmwares",
    "refs": ["v4.15864"],
    "standaloneList": [""],
    "PLATFORM": "PM3GENERIC",
    "PLATFORM_EXTRAS": "",
    "PLATFORM_SIZE": "256",
    "extraOptions": ["SKIP_HITAG", "SKIP_FELICA"],
    "buildS19": true
}
```