#!/usr/bin/env python

import gtk
import feedparser
import urllib2

class GmailView:

    def __init__(self):

        self.status_icon = gtk.status_icon_new_from_file('no_new.ico')
        self.status_icon.set_tooltip('No new email')
        self.status_icon.set_visible(True)

        self.menu = gtk.Menu()
        self.about_item = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
        self.menu.append(self.about_item)
        self.quit_item = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        self.menu.append(self.quit_item)

    def new_mail(self):
        
        self.status_icon.set_from_file('unread.ico')

    def no_mail(self):
        
        self.status_icon.set_from_file('no_new.ico')

class GmailController:

    def __init__(self):

        self.view = GmailView()
        self.view.quit_item.connect('activate', self.quit)
        self.view.status_icon.connect('popup-menu', self.menu_show)

        self.gmail = GmailChecker('', '')
        
        if self.gmail.unread_count > 0:
            self.view.new_mail()
        else:
            self.view.no_mail()

    def menu_show(self, widget, button, time):

        print self.gmail.unread_count
        if button == 3:
            self.view.menu.show_all()
            self.view.menu.popup(None, None, None, button, time)
            
    def quit(self, widget):
        
        self.view.status_icon.set_visible(False)
        gtk.main_quit()

class GmailChecker:

    feed_realm = 'New mail feed'
    feed_domain = 'mail.google.com'
    feed_url = 'http://mail.google.com/mail/feed/atom'

    def __init__(self, username, password):
        self.username = username
        self.__password = password
        self.login()

    def login(self):
        self.http_auth = urllib2.HTTPDigestAuthHandler()
        self.http_auth.add_password(self.__class__.feed_realm, 
                            self.__class__.feed_domain,
                            self.username, self.__password)

        self.feed = feedparser.parse(self.__class__.feed_url, 
                                        handlers = [self.http_auth])

    def parse(self):
        if self.feed.etag:
            self.feed = feedparser.parse(self.__class__.feed_url,
                                handlers = [self.http_auth],
                                etag = self.feed.etag)
        elif self.feed.modified:
            self.feed = feedparser.parse(self.__class__.feed_url,
                                handlers = [self.http_auth],
                                modified = self.feed.modified)
        else:
            self.feed = feedparser.parse(self.__class__.feed_url,
                                handlers = [self.http_auth])

    def unread_count(self):
        return len(self.feed.entries)

if __name__ == '__main__':
    
    app = GmailController()
    gtk.main()


