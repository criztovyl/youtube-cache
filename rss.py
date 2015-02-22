#!/bin/env python
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
import feedparser
from appdirs import user_data_dir
import hashlib
import os
import json as JSON
class RSSParser:
    def __init__(self, url):

        #Init var
        self.url = url
        self.items = []
        self.urls = []

        #Set data path and safe name
        appdir = user_data_dir("rssparser", "criztovyl")
        self.safe_name = appdir + os.sep + hashlib.sha256(self.url).hexdigest()

        #Create data dir
        if not os.path.exists(appdir):
            os.makedirs(appdir)

        #Open safe file (once for writing that the file is created if not exists)
        if not os.path.exists(self.safe_name + ".json"):
            f = open(self.safe_name + ".json", "w")
            f.close()
        safe_file = open(self.safe_name + ".json", "r")

        #Write mapping file only if not exists
        mab_path = self.safe_name + ".map"
        if not os.path.exists(mab_path):
            with open(mab_path, "w") as mab:
                mab.write(self.url)

        #Load urls and items from json
        try:
            json = JSON.load(safe_file)
            if "urls" in json.keys():
                self.urls = JSON.loads(json["urls"])
            if "items" in json.keys():
                self.items = JSON.loads(json["items"])
        except ValueError, e:
            pass

        safe_file.close()


    #Update feed
    def update(self):
        #Load Feed
        feed = feedparser.parse(self.url);
        #Iterate items
        for item in feed["items"]:
            if item["id"] not in self.items:
                self.items.append(item["id"])
                self.urls.append(item["link"].replace("&feature=youtube_gdata", ""))
        #Dump updated urls and items
        JSON.dump({
                "urls" : JSON.dumps(self.urls),
                "items" : JSON.dumps(self.items)
                }, open(self.safe_name + ".json", "w"))
