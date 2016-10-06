# -*- coding:utf-8 -*-
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

class PageParser(HTMLParser):
    """ class to parse an html page
        html: parsed html ready to save to file
        urls: urls to use for recursive search
    """

    def __init__(self, *args, **kwargs):
        HTMLParser.__init__(self)
        self.html = ""
        self.urls = []
    #both side type start tag handle ( overring function from HTMLParser )
    def handle_starttag(self, tag, attrs):
        self.html += "<" + tag + " "
        for attr in attrs:
            #format urls for recursion
            if attr[0] == 'href':
                if attr[1] == '/':
                    print "this is home link"
                    pass
                #relative to root
                elif attr[1].startswith(".."):
                    self.urls.append(attr[1][3:])
                #outbound links
                elif attr[1].find("google") != int(-1):
                    pass
                elif attr[1].startswith("http"):
                    print "start with http"
                    pass
                elif attr[1].startswith("https"):
                    print "start with https"
                    pass
                #links going deeper
                elif attr[1].startswith("/"):
                    self.urls.append("{fp}" + attr[1])
                #same directory as current link
                else:
                    self.urls.append("{fp}/" + attr[1])
            elif attr[0] == 'src':
                if attr[1].startswith(".."):
                    for_root_dir_check_variable = attr[1][3:]
                    if for_root_dir_check_variable == '/':
                        pass
                    else:
                        self.urls.append(for_root_dir_check_variable)
                else:
                    if attr[1] == '/':
                        pass
                    elif attr[1].startswith("http"):
                        print "start with http"
                        pass
                    elif attr[1].startswith("https"):
                        print "start with https"
                        pass
                    else:
                        self.urls.append(attr[1])

            try:
                if attr[1] == None:
                    self.html += attr[0] + "=\"" + "\" "
                else:
                    self.html += attr[0] + "=\"" +  attr[1].decode('utf-8').encode('utf-8') + "\" "
                    # self.html += attr[0] + "=\"" + attr[1] + "\" "
            except Exception as e:
                print e
        self.html += ">"

    #both side type end tag handle ( overring function from HTMLParser )
    def handle_endtag(self, tag):
        self.html += "</" + tag + ">"

    #one side type s tag handle ( overring function from HTMLParser )
    def handle_startendtag(self, tag, attrs):
        self.html += "<" + tag + " "
        for attr in attrs:
            if attr[0] == 'href':
                #relative to root
                if attr[1] == '/':
                    print "this is home link"
                elif attr[1].startswith(".."):
                    self.urls.append(attr[1][3:])
                elif attr[1].find("google") != int(-1):
                    print "the link have a google keyword"
                    pass
                #outbound links
                elif attr[1].startswith("http"):
                    print "start with http"
                    pass
                elif attr[1].startswith("https"):
                    print "start with https"
                    pass
                #links going deeper
                elif attr[1].startswith("/"):
                    self.urls.append("{fp}" + attr[1])
                #same directory as current link
                else:
                    self.urls.append("{fp}/" + attr[1])
            elif attr[0] == 'src':
                if attr[1].startswith(".."):
                    for_root_dir_check_variable = attr[1][3:]
                    if for_root_dir_check_variable == '/':
                        pass
                    else:
                        self.urls.append(for_root_dir_check_variable)
                else:
                    if attr[1] == '/':
                        pass
                    elif attr[1].startswith("http"):
                        print "start with http"
                        pass
                    elif attr[1].startswith("https"):
                        print "start with https"
                        pass
                    else:
                        self.urls.append(attr[1])

            self.html += attr[0] + "=\"" +  attr[1].decode('utf-8').encode('utf-8') + "\" "
            # self.html += attr[0] + "=\"" + attr[1] + "\" "
        self.html += "/>"

    #data handle in frontend page -> html() ( overring function from HTMLParser )
    def handle_data(self, data):
        self.html += data.decode('utf-8').encode('utf-8')

    #commnet handle ( overring function from HTMLParser )
    def handle_comment(self, data):
        self.html += "<!--" + data + "-->"

    #entity_ref handle ( overring function from HTMLParser )
    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        self.html += c

    #char_ref tag handle ( overring function from HTMLParser )
    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        self.html += c

    #decl handle ( overring function from HTMLParser )
    def handle_decl(self, data):
        self.html += "<!" + data + ">"

    #NOT USE - pi handle ( overring function from HTMLParser )
    def handle_pi(self, data):
        pass
