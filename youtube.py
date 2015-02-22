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
from rss import RSSParser
from tools import Path
from tools import JSONFile
from appdirs import AppDirs
class YouTubeCache:
    def __init__(self):
        #Init vars
        self.appdir = Path(AppDirs("YouTubeCache", "criztovyl").user_data_dir)
        self.channels_jf = JSONFile(self.appdir.append("channels.json").path)
        self.cached_jf = JSONFile(self.appdir.append("chached.json").path)
        self.rsss = []
        self.cached = self.cached_jf.load() or []
        self.channels = self.channels_jf.load() or []
        for channel in self.channels:
            self.rsss.append(RSSParser())
        for rss in self.rsss:
            print rss.url
        self.save()
    def cache(self):
        for rss in self.rsss:
            rss.update()
        return self
    def add(self, channels):
        for channel in channels:
            self.channels.append(channel)
            self.rsss.append(RSSParser(self.rssurl(channel)))
        return self
    def save(self):
        self.channels_jf.data(self.channels).saveAsync()
        self.cached_jf.data(self.cached).saveAsync()
    @staticmethod
    def rssurl(channel):
        return 'http://gdata.youtube.com/feeds/base/users/%(c)s/uploads?format=5' % {"c" : channel }
