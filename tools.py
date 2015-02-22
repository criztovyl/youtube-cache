#!/usr/bin/python
#    This is a program to cache YouTube videos
#    Copyright (C) 2015 Christoph "criztovyl" Schulz
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os
import logging
import json as JSON
from threading import Thread
class Path:
    def __init__(self, filepath, sep = os.sep):
        self.path = filepath
        self.sep = sep
    def append(self, filename):
        return Path(self.path + self.sep + filename, self.sep)
    def open(self, mode="r"):
        return open(self.path, mode)
    def mkdirs(self):
        if not os.path.exists(self.path):
            os.mkdirs(self.path)
    def touch(self):
        print self.pardir()
        if not os.path.exists(self.pardir()):
            os.makedirs(self.pardir())
        open(self.path, "w")
    def pardir(self):
        return os.path.dirname(os.path.abspath(self.path))
    def touchIfNotExists(self):
        if not os.path.exists(self.path):
            self.touch()
    def basename(self):
        return os.path.basename(self.path)
    def suffix(self, suffix):
        return Path(self.path + "." + suffix, self.sep)

class LoggerEnvironment:
    def __init__(self):
        logging.basicConfig(format="%(asctime)s %(levelname)s %(filename)s %(name)s: %(message)s", datefmt="%H:%M:%S", level=logging.INFO)
    @staticmethod
    def getLogger(clazz):
        return logging.getLogger(clazz.__class__.__name__)

class JSONFile:
    #fjle => file
    def __init__(self, filename):
        LoggerEnvironment()
        self.filePath = Path(filename)
        self.filePath.touchIfNotExists()
        self.logger = LoggerEnvironment.getLogger(self)
    def data(self, obj):
        self.obj = obj
        return self
    def save(self):
        self.logger.info("Saving %s..." % self.filePath.basename())
        JSON.dump(self.obj, self.filePath.open("w"))
        self.logger.info("Saved %s." %self.filePath.basename())
        return self
    def saveAsync(self):
        self.thread = Thread(name=self.filePath.path, target=self.save)
        self.thread.start()
        return self
    def load(self):
        try:
            return JSON.load(self.filePath.open())
        except:
            return None
