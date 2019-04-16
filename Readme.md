# Application Manager utility

### Running the application

`python main.py`

### Commands

Type `help` and find out details about the commands

In summary:
1. `load` --> loads `applications.json`. If not specified, will use detault configuration (dft_cfg.json), which is being updated when multiple commands finish.
1. `install {app_n}` --> Install an application
1. `credentials {app_n}` --> Install credentials for an application
1. (Optional) `update {app_n} {library} {sha/tag}`
1. `compile {app_n}` --> Compile an application
1. `run {app_n}` --> Program target and verify application works as expected
1. `all {app_n}` --> Performs multiple tasks with an application (install, credentials, compile, run)
1. `exit`

**Note** `{app_n}` can also be `all`, which means the operation is performed on all applications.

### Installation

```
git clone https://github.com/ARMmbed/aman
cd aman
python setup.py install
```

### Environment setup

1. Generate `mbed_cloud_dev_credentials.c` and copy to the config folder

2. Review `applications.json` and ensure contains relevant information

#### Update local configuration

The `.env` file is used to store local configuration. Example of paratemers:

```
PELION_CREDENTIALS_FILE=util/mbed_cloud_dev_credentials.c
API_KEY=15439862444196150789
WIFI_SSID=xxx
WIFI_PASS=yyy
```

### Current limitations and pending tasks:

Important:
- Use WiFi credentials on WiFi applications
- Add ability to publish changes into repository/branch
- Add support for Windows. Currently only OSX is supported.
- Add Arm Compiler and IAR. Currently only GCC_ARM is supported.

Future/minor:
- Check R/W to device from Pelion
- Download credentials from Pelion, using API keys
- Check/Install Python requirements
    - mbed-host-tests --> 1.4.0
    - Cloud Python SDK
Optional:
- Option to override default timeout for applications