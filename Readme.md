# Application Manager utility

This is a simple automation tool to check the status of Mbed OS applications, update dependencies, compile and run on hardware platforms.

It uses an interactive CLI interface to perform multiple tasks on top of Mbed CLI.

### Installation

```
git clone https://github.com/MarceloSalazar/aman
cd aman
```

### Setup

1.  Configure application database

    Review `applications.json` (or other json file) and ensure contains relevant information for the applications and targets that you'd like to test.

2. Update local configuration

    The `.env` file is used to store local configuration. Not currently used. Example of paratemers:

    ```
    WIFI_SSID=xxx
    WIFI_PASS=yyy
    ```

### Running

```
python aman.py

Configuration loaded from file dft_cfg.json

Application Manager
===================
(Cmd) help

Documented commands (type help <topic>):
========================================
all  compile  exit  help  install  load  run  save  status  toolchain  update
```

### Using aman

Type `help` and find out details about the commands

In summary:
1. `load` --> loads `applications.json`. If not specified, will use detault configuration (dft_cfg.json), which is being updated when a command finish executing to keep the latest status.
1. `install {app_n}` --> Install an application
1. (Optional) --> Update specific libraries: `update {app_n} {library} {sha/tag}`
1. `compile {app_n}` --> Compile an application
1. `run {app_n}` --> Program target and verify application works as expected
1. `all {app_n}` --> Performs multiple tasks with an application (install, compile, run)
1. `exit`

**Note** `{app_n}` can also be `all`, which means the operation is performed on all applications.


### Planned features/fixes:

- Add ability to publish changes into repository/branch
- Add support for Windows. Currently only OSX is supported.
- Add option to compile using multiple toolchains. Currently either GCC_ARM or ARM is supported.
- Check/Install Python requirements
    - mbed-host-tests --> 1.4.0
- Use connectivity credentials, for example WiFi SSID/PASS
- Option to override default timeout for applications
