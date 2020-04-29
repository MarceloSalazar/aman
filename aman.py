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

from pprint import pprint
import cmd
from dotenv import load_dotenv
import os
import sys
sys.path.insert(0, './aman')
from appman import *

app = App_man()

class CLI(cmd.Cmd):
    """Simple command processor example."""

    def do_toolchain(self, toolchain):
        "Defines default toolchain. Usage: toolchain <toolchain>"
        if toolchain:
            print "Toolchain: " + toolchain
            app.config_toolchain(toolchain)
        else:
            print "Error at configuring toolchain"
    
    def do_compile(self, app_n):
        "Check if application compiles OK. Usage: compile <app_n>"

        # TODO: select compiler, or compile for all

        if app_n == "":
            print "Need application number"
        elif app_n == "all":
            print "Compile all applications"
            n = app.get_napps()
            for i in range(0, n):
                app.compile_app(int(i))
        elif not app_n.isdigit():
            print "Not a number: " + app_n
        else:
            print "Compiling application " + app_n
            app.compile_app(int(app_n))

    def do_run(self, app_n):
        "Check if applications runs OK on target. Usage: run <app_n>"

        if app_n == "":
            print "Need application number"
        elif not app_n.isdigit():
            print "Not a number: " + app_n
        else:
            print "Runner application " + app_n
            app.run_app(int(app_n))

        # TODO: select compiler, or run for all

    def do_load(self, file=None):
        "Load configuration file. Usage: load <file.json>"

        if file == "":
            file = "applications.json"
        print "Load file: " + str(file)
        app.load_config(file)

    def do_save(self, file=None):
        "Save current configuration in file. Usage save [file.json] (optional)"
        app.save_config()

    def do_install(self, app_n):
        "Download and install application in current workspace. Usage: install <app_n>"

        if app_n == "":
            print "Need application number"
        elif app_n == "all":
            print "Install all applications"
            n = app.get_napps()
            for i in range(0, n):
                app.install_app(int(i))
        elif not app_n.isdigit():
            print "Not a number: " + app_n
        else:
            print "Installing application " + app_n
            app.install_app(int(app_n))

    def do_update(self, params):
        "Update library in installed application. Usage: update <app_n> <library> <sha/tag>"

        params = params.split(" ")

        if len(params) < 3:
            print "Need params: app_n, library, sha/tag"
            return
        elif params[0] == "":
            print "Need application number"
            return
        elif params[1] == "":
            print "Need library name"
            return
        elif params[2] == "":
            print "Need sha/tag name"
            return
        elif params[0] == "all":
            print "Update all applications"
            n = app.get_napps()
            for i in range(0, n):
                app.update_library(params[1], params[2], int(i))
        else:
            app.update_library(params[1], params[2], int(params[0]))
               

    def do_all(self, app_n):
        "Install, compile, run an application. Usage: all <app_n>"

        if app_n == "":
            print "Need application number"
        elif not app_n.isdigit():
            print "Not a number: " + app_n
        else:
            app.install_app(int(app_n))
            app.compile_app(int(app_n))
            app.run_app(int(app_n))


    def do_status(self, line):
        "Print current status of applications and tests. Usage: status"

        app.print_status()

    def do_exit(self, line):
        "Print current status of applications and tests. Usage: status"
        return True

def main():

    # Load local configuration file
    load_dotenv('.env')

    print "\n"
    print "Application Manager"
    print "==================="

    # Run Command Line interpreter
    CLI().cmdloop()

    return

if __name__ == '__main__':
    main()
