#!/usr/bin/env python3.6

##############################################################################
# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
##############################################################################

from utils.arg_parse import getParser, getArgs
from reporters.reporter_base import ReporterBase
from utils.utilities import getDirectory

import json
import os

getParser().add_argument("--local_reporter",
    help="Save the result to a directory specified by this argument.")


class LocalReporter(ReporterBase):
    def __init__(self):
        super(LocalReporter, self).__init__()

    def report(self, content):
        net_name = content[self.META]['net_name']
        netdir = self._getFilename(net_name) + "/"
        platform_name = content[self.META][self.PLATFORM]
        platformdir = self._getFilename(platform_name) + "/"
        ts = float(content[self.META]['time'])
        commit = content[self.META]['commit']
        datedir = getDirectory(commit, ts)
        dirname = platformdir + netdir + datedir
        dirname = getArgs().local_reporter + "/" + dirname
        i = 0
        while os.path.exists(dirname + str(i)):
            i = i+1
        dirname = dirname + str(i) + "/"
        os.makedirs(dirname)
        data = content[self.DATA]
        for d in data:
            filename = dirname + self._getFilename(d) + ".txt"
            content_d = json.dumps(data[d])
            with open(filename, 'w') as file:
                file.write(content_d)
        filename = dirname + self._getFilename(self.META) + ".txt"
        with open(filename, 'w') as file:
            content_meta = json.dumps(content[self.META])
            file.write(content_meta)

    def _getFilename(self, name):
        filename = name.replace(' ', '-').replace('/', '-')
        return "".join([c for c in filename
                        if c.isalpha() or c.isdigit() or
                        c == '_' or c == '.']).rstrip()