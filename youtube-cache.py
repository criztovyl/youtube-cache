from rssparser import RSSParser
rss = RSSParser("http://gdata.youtube.com/feeds/base/users/songstowearpantsto/uploads?format=5")
rss.update()
while len(rss.urls) > 0:
    print rss.urls.pop()
rss.update()
