# PM3 Firmware Builder

Build multiple firmwares of [Proxmark3 RRG repo](https://github.com/RfidResearchGroup/proxmark3) in parallel by GitHub Action.  

## Usage
1. Fork this repo  
2. Go to `Actions` then enable it.  
(If you don't want to affect your contribution chart, you can create a new branch then do the following steps)  
3. Change the `config.json`  
(You can also build the firmware based on your own RRG repo, just change the `URL` to your repo URL)  
4. Push a commit to this repo or click `Run workflow` in `Actions`  
5. Check and download the firmwares in `Actions`->the latest workflow run->`Artifacts`  

## Examples of `config.json`

### Build the latest firmware of Proxmark3 RDV4 with `LF_SAMYRUN` standalone mode

<details>
<summary>config.json</summary>


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

</details>

### Build `v4.15864` of Proxmark3 generic firmware with `HF_14ASNIFF` standalone mode

<details>
<summary>config.json</summary>

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

</details>

### Build 18 sets of firmwares in one run

<details>
<summary>config.json</summary>

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

</details>

### Build firmware for Proxmark3 generic target with 256KB flash memory(AT91SAM7S256)
[config described there](https://github.com/RfidResearchGroup/proxmark3/blob/master/doc/md/Use_of_Proxmark/4_Advanced-compilation-parameters.md#256kb-versions)  

(no standalone mode, no hitag, no felica)  

<details>
<summary>config.json</summary>

```
{
    "//": "You will get len(refs) * len(standaloneList) firmwares",
    "refs": ["v4.13441"],
    "standaloneList": [""],
    "PLATFORM": "PM3GENERIC",
    "PLATFORM_EXTRAS": "",
    "PLATFORM_SIZE": "256",
    "extraOptions": ["SKIP_HITAG", "SKIP_FELICA"],
    "buildS19": true
}
```

</details>

<details>
<summary>config.json</summary>

```
{
    "refs": ["v4.17140", "v4.16717", "v4.15864"],
    "standaloneList": ["", "HF_14ASNIFF"],
    "PLATFORM": "PM3GENERIC",
    "PLATFORM_EXTRAS": "",
    "PLATFORM_SIZE": "256",
    "extraOptions": [
        "SKIP_HITAG",
        "SKIP_ICLASS",
        "SKIP_FELICA",
        "SKIP_LEGICRF",
        "SKIP_ISO14443b",
        "SKIP_EM4x50",
        "SKIP_NFCBARCODE"
    ],
    "extraLines": [],
    "buildS19": true,
    "URL": ""
}
```

</details>

### Build firmware for Proxmark3 generic target with external flash memory

<details>
<summary>config.json</summary>

```
{
    "refs": ["master"],
    "standaloneList": ["HF_14ASNIFF", "HF_MFCSIM"],
    "PLATFORM": "PM3GENERIC",
    "PLATFORM_EXTRAS": "",
    "PLATFORM_SIZE": "",
    "extraOptions": [],
    "extraLines": [
        "PLATFORM_DEFS=-DWITH_FLASH"
    ],
    "buildS19": true
}
```

</details>
