# -*- coding:utf-8 -*-
import os
import re
import sys
import urllib2
from parser_custom import PageParser


class Page(object):
    def __init__(self, url, fp):
        self.url = url
        self.fp = fp
        self.fileRoot = "site" #root file path
        self.siteRoot = "http://" + sys.argv[1]  #root site path

    def save(self): #recursive function
        url = self.url
        #add and update fp if necessary

        self.fp = ""
        url = re.sub("{fp}", self.fp, url)
        last = url.rfind("/")
        self.fp = url[:last]
        filepath = url.split("/")  #prep filepath

        url = self.siteRoot +"/" + url         #final url

        #case for the index page
        if len(filepath) ==1 and not filepath[0]:
            filepath.append("index.html")
        filename = filepath[-1]

        #create filepath to save on disk
        if not filepath[0]:
            filepath = os.path.join(self.fileRoot, *filepath[1:-1])
        else:
            filepath = os.path.join(self.fileRoot, *filepath[:-1])
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        #final write path
        filepath = os.path.join(filepath, filename)

        if os.path.isfile(filepath):
            return

        #write to file
        f = open(filepath, 'w')
        try:
            r = urllib2.urlopen(url)
            if ".html" in filename:
                parser = PageParser()
                parser.feed(r.read())
                html = parser.html.encode('utf-8', 'replace') #utf-8(web) -> ascii(python process) -> utf-8(file)
                # html = parser.html.encode('ascii', 'replace')
                f.write(html)
                f.close()
                for url in parser.urls:
                    nextPage = Page(url, self.fp)
                    nextPage.save()
            else:
                f.write( r.read() )
                f.close()
        except Exception as e:
            print e

if __name__ == '__main__':
    #requirement for utf-8 sytem configuration.
    reload(sys)
    sys.setdefaultencoding('utf-8')
    if len(sys.argv) == 2:
        print
        page = Page("", "")
        page.save()
    else:
        #User usage
        print "Usage: python" , sys.argv[0], "www.example.com"