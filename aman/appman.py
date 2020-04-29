#!/usr/bin/env python

# Copyright (c) 2016 ARM Limited, All Rights Reserved
# SPDX-License-Identifier: Apache-2.0

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied.

import argparse
import os
import shutil
import subprocess
import datetime
import time
import threading
from datetime import datetime
from prettytable import PrettyTable
import json
from datetime import datetime
import mbed_lstools

# Common default settings
dft_temp_dir = "tmp/"
dft_cfg_file =  "dft_cfg.json"
dft_polling_timeout = 120
dft_log_file = "util/default.log"


def get_timestamp():
    yr = datetime.now().year
    mo = datetime.now().month
    day = datetime.now().day
    hr = datetime.now().hour
    min = datetime.now().minute
    return str(yr) + str(mo) + str(day) + str(hr) + str(min)


# Application manager
class App_man:

    def __init__(self):
        self.apps = []
        self.load_config(dft_cfg_file)
        self.dft_toolchain = "GCC_ARM"

        return 

    def get_napps(self):
        return len(self.apps)

    def save_config(self, config_file=None):

        if config_file==None:
            config_file = dft_cfg_file

        try:
            with open(config_file, 'w') as json_file:
                json_str = json.dumps(self.apps)
                json_file.write(json_str)
                json_file.close()

        except Exception, e:
            print "Error at saving " + config_file + " file, " + str(e)
            print "Configuration not saved"
            return

    def remove_app(self, app_n):

        if not isinstance(app_n,int):
            print "Not a number: " + str(app_n)
            return

        try:
            if "local_dir" in self.apps[app_n] and self.apps[app_n]["local_dir"] != False:
                shutil.rmtree(dft_temp_dir + self.apps[app_n]["local_dir"])
        except Exception, e:
            print "Warning: 'local_dir' not found: " + str(self.apps[app_n]["local_dir"])

        self.apps[app_n]["local_dir"] = False
        self.apps[app_n]["status"] = "NEW"
        self.apps[app_n]["compile"] = ""
        self.apps[app_n]["credentials"] = ""
        self.save_config()

    def load_config(self, config_file):

        if config_file == "":
            print "Need to specify file, " + config_file
            return

        try:
            with open(config_file) as json_file:
                self.apps = json.load(json_file)
        except Exception, e:
            print "Error at opening " + config_file + " file, " + str(e)
            print "Configuration not loaded. Use 'load <config.json>"
            return

        print "Configuration loaded from file " + config_file

        for i in range(len(self.apps)):

            self.apps[i]["name"].replace(" ", "_")
            self.apps[i]["vendor"].replace(" ", "_")

            if "status" not in self.apps[i]:
                self.apps[i]["status"] = "NEW"

            if "local_dir" not in self.apps[i] or self.apps[i]["local_dir"] == False:
                self.remove_app(i)
            
            if self.apps[i]["local_dir"]:
                if os.path.isdir(dft_temp_dir + self.apps[i]["local_dir"]) == False:
                    print "Application not found in folder. Removing."
                    self.remove_app(i)

            if "compile" not in self.apps[i]:
                self.apps[i]["compile"] = [""]

            if "run" not in self.apps[i]:
                self.apps[i]["run"] = [""]

        self.save_config()

    def install_app(self, app_n):

        # TODO: check parameters
        if not isinstance(app_n,int):
            print "Not a number (install): " + str(app_n)
            return

        if self.apps[app_n]["local_dir"]:
            print "Application exists. Deleting and installing new one."

            try:
                shutil.rmtree(dft_temp_dir + self.apps[app_n]["local_dir"])
                print "Done"
            except Exception, e:
                print "Error at deleting " + self.apps[app_n]["local_dir"] + " folder"
    
        # Get app name
        app_name = self.apps[app_n]["app_url"]
        if app_name[-1:] == '/': 
            app_name = app_name[:-1] # Remove last character
        app_name = app_name.split("/")[-1]
      
        self.apps[app_n]["local_dir"] = get_timestamp() + "_" + \
                                        self.apps[app_n]["vendor"] + "_" + app_name
                                            
        print "Temp location: " + self.apps[app_n]["local_dir"]

        if "branch" in self.apps[app_n]:
            # TODO: test branch feature
            branch = self.apps[app_n]["branch"]
            command = "mbed import " + \
                  self.apps[app_n]["app_url"] + "#" + branch + " " + \
                  dft_temp_dir + self.apps[app_n]["local_dir"]
        else:
            command = "mbed import " + \
                  self.apps[app_n]["app_url"] + " " + \
                  dft_temp_dir + self.apps[app_n]["local_dir"]

        print("Command: " + command)

        try:
            output = subprocess.check_call(command , shell=True, stderr=subprocess.STDOUT)
        except Exception, e:
            print "Error: " + str(e.output)

        self.apps[app_n]["status"] = "INSTALLED"
        self.apps[app_n]["credentials"] = ""
        self.apps[app_n]["compile"] = ""
        self.apps[app_n]["run"] = ""
        self.save_config()
        
    def config_toolchain(self, toolchain):

        # TODO: check parameters
        if toolchain:
            self.dft_toolchain = toolchain
            # TODO: clean build and run status for targets
            return

    def print_status(self, app_n=None):

        table = PrettyTable(['#', 'Name', 'Targets', 'Status', 'Compile', 'Run'])
        table.align['Targets'] = 'l'
        
        print "Toolchain: " + self.dft_toolchain

        for i in range(len(self.apps)):

            table.add_row([i, \
                           self.apps[i]["name"], \
                          ",\n".join(map(str, self.apps[i]["targets"])), \
                           self.apps[i]["status"], \
                           ",\n".join(map(str, self.apps[i]["compile"])), \
                           ",\n".join(map(str, self.apps[i]["run"])) ])
        print table


    def update_app_library(self, library, sha_tag, app_n):

        if not isinstance(app_n,int):
            print "Not a number (update): " + str(app_n)
            return
        if not self.apps[app_n]["local_dir"]:
            print "Application not installed locally: " + str(app_n)
            return

        # TODO: check parameters

        top_path = os.getcwd()

        # Change to library folder before updating
        temp = top_path + '/tmp/' + self.apps[app_n]["local_dir"] + '/' + library
        os.chdir(temp)

        command = "mbed update " + sha_tag
        print "\n"
        print("command: " + command)

        try:
            output = subprocess.check_call(command , shell=True, stderr=subprocess.STDOUT)
        except Exception, e:
            output = str(e.output)
        print output

        # Return to top path
        os.chdir(top_path)

    def update_library(self, library, sha_tag, app_n=None):

        # TODO: check parameters

        print "Updating library " + library + " to " + sha_tag

        if app_n == None:
            print "Update: " + str(app_n)
            for i in range(len(self.apps)):
                self.update_app_library(library, sha_tag, i)
        else:
            print "Update: " + str(app_n)
            self.update_app_library(library, sha_tag, app_n)

    def compile_app(self, app_n):

        if not isinstance(app_n,int):
            print "Not a number (update): " + str(app_n)
            return
        if (not self.apps[app_n]["local_dir"]):
            print "Application not installed locally: " + str(app_n)
            return

        # Save current path        
        top_path = os.getcwd()

        # Change to library folder before compiling
        temp = top_path + '/' + dft_temp_dir + self.apps[app_n]["local_dir"] + '/'
        os.chdir(temp)

        # TODO: Needed config for specific apps, such WiFi credentials

        compile_options = " -c"

        compile_target = []
        for target in self.apps[app_n]["targets"]:
            command = "mbed compile -t " + self.dft_toolchain + \
                      " -m " + target + \
                      compile_options
                      
            print("command: " + command)

            try:
                output = subprocess.check_call(command , shell=True, stderr=subprocess.STDOUT)
                compile_target.append(target + "_" + self.dft_toolchain + "_OK")

            except Exception, e:
                output = str(e.output)
                compile_target.append(target + "_" + self.dft_toolchain + "_Error")

        # Return to top path
        os.chdir(top_path)

        self.apps[app_n]["compile"] = compile_target
        self.save_config()

    def run_app(self, app_n):

        if not isinstance(app_n,int):
            print "Not a number (run): " + str(app_n)
            return

        # TODO:
        # Check if compile was successful for target we're going to run
        # depends on identifying if combination of target + toolchain was succesfull

        # Detect platform
        mbeds = mbed_lstools.create()
        muts = mbeds.list_mbeds(filter_function=None, unique_names=True, read_details_txt=False)

        print "Detected devices:"
        detected_devices = dict()
        for mut in muts:
            detected_devices[mut["platform_name"]] = {"mount": mut["mount_point"], "serial":mut["serial_port"]}
            print "   " + mut["platform_name"]
            
        if detected_devices == dict():
            print "   None"
         
        run_target=[]
        for target in self.apps[app_n]["targets"]:
            # Detect devices and continue to flash them

            if target not in detected_devices:
                run_target.append(target + "_Error")
                print "Target " + target + " not detected"
                continue
            else:
                print "Target " + target + " detected"

            binary_path = dft_temp_dir + self.apps[app_n]["local_dir"] + \
                          '/' + 'BUILD/' + \
                          target + '/' + self.dft_toolchain + '/' + \
                          self.apps[app_n]["local_dir"] + '.bin'

            # Program specific device and check output
            command = "mbedhtrun" + \
                      " -d " + detected_devices[target]['mount'] + \
                      " -p " + detected_devices[target]['serial'] + ":115200" + \
                      " -m " + target + \
                      " -f " + binary_path + \
                      " --sync=0" + \
                      " --compare-log " + str(dft_log_file) + \
                      " --polling-timeout " + str(dft_polling_timeout)
                      # TODO: A different log file could be specified for other applications

            print("Command: " + command)

            try:
                output = subprocess.check_call(command , shell=True, stderr=subprocess.STDOUT)
                run_target.append(target + "_" + self.dft_toolchain + "_OK")
            except Exception, e:
                output = str(e.output)
                run_target.append(target + "_" + self.dft_toolchain + "_Error")

        self.apps[app_n]["run"] = run_target
        self.save_config()
