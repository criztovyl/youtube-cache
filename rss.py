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
import hashlib
import os
import json as JSON
from tools import JSONFile
from appdirs import user_data_dir
class RSSParser:
    def __init__(self, url):

        #Init var
        self.url = url
        self.items = []
        self.urls = []

        #Set data path and safe name
        appdirPath = Path(user_data_dir("rssparser", "criztovyl"))
        appdirPath.mkdirs()
        self.safePath = appdirPath.append(hashlib.sha256(self.url).hexdigest())
        self.safe = JSONFile(safePath.path)

        #Write mapping file only if not exists
        self.safePath.suffix("map").touchIfNotExists()

        #Load urls and items from json
        try:
            json = safe.load()
            if "urls" in json.keys():
                self.urls = JSON.loads(json["urls"])
            if "items" in json.keys():
                self.items = JSON.loads(json["items"])
        except ValueError, e:
            pass

    #Update feed
    def update(self):
        #Load Feed
        feed = feedparser.parse(self.url);
        #Iterate items
        newitems = []
        for item in feed["items"]:
            if item["id"] not in self.items:
                self.items.append(item["id"])
                link = item["link"].replace("&feature=youtube_gdata", "")
                self.urls.append(link)
                newitems.append(link)
        self.save()
        return newitems;

    def save(self):
        #Dump updated urls and items
        self.safe.data({
                "urls" : JSON.dumps(self.urls),
                "items" : JSON.dumps(self.items)
                }).save()
    def saveAsync(self):
        Thread(target=self.save).start()
