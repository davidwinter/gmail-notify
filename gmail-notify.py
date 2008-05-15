#!/usr/bin/env python

import gtk
import feedparser
import urllib
import sys
import getpass
import webbrowser

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

    def new_mail_menu_item(self, label, url):
        
        return GmailMessageItem(label, url)
        
    

class GmailController:

    def __init__(self):

        self.view = GmailView()
        self.view.quit_item.connect('activate', self.quit)
        self.view.status_icon.connect('popup-menu', self.menu_show)

        self.gmail = GmailChecker()
        
        print self.gmail.unread_count()
        print self.gmail.feed.entries[0].author_detail.name
        print self.gmail.feed.entries[0].link
        #entry = self.gmail.feed.entries[0]
        #label = entry.author_detail.name + ' ' + entry['title']
        #url = entry.link
        #new_item = GmailMessageItem(label, url)
        #new_item.connect('activate', self.open_message)
        #self.view.menu.prepend(new_item)

        self.check_mail()
        
    def open_message(self, widget):
        webbrowser.open_new_tab(widget.url)
    
    def check_mail(self):
        self.gmail.parse()

        if self.gmail.unread_count() > 0:
            message_builder = GmailMessageBuilder()
            emails = message_builder.build_label_url_dict(self.gmail.feed)
            for email in emails:
                new_item = GmailMessageItem(emails[email], email)
                new_item.connect('activate', self.open_message)
                self.view.menu.prepend(new_item)
            

            self.view.new_mail()
        else:
            self.view.no_mail()

    def menu_show(self, widget, button, time):

        if button == 3:
            self.view.menu.show_all()
            self.view.menu.popup(None, None, None, button, time)
            
    def quit(self, widget):
        
        self.view.status_icon.set_visible(False)
        gtk.main_quit()

class GmailMessageBuilder:

    def build_label_url_dict(self, feed):
        dict = {}
        for entry in feed.entries:
            value = entry.author_detail.name + ': ' + entry.title
            dict[entry.link] = value

        return dict

class GmailChecker:

    feed_realm = 'New mail feed'
    feed_domain = 'mail.google.com'
    feed_url = 'http://mail.google.com/mail/feed/atom'

    def __init__(self):
        self.parse()

    def parse(self):
        opener = GmailURLOpener()
        f = opener.open(self.__class__.feed_url)
        self.feed_src = f.read()
        self.feed = feedparser.parse(self.feed_src)

    def unread_count(self):
        return len(self.feed.entries)

class GmailURLOpener(urllib.FancyURLopener):

    def prompt_user_passwd(self, host, realm):
        username = open('username').read().strip()
        password = open('password').read().strip()
        return (username, password)

class GmailMessageItem(gtk.MenuItem):
    
    def __init__(self, label, url):
        gtk.MenuItem.__init__(self, label)
        self.url = url

if __name__ == '__main__':
    
    app = GmailController()
    gtk.main()


