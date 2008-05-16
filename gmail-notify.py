#!/usr/bin/env python

import gtk
import gobject
import webbrowser

import urllib 
import feedparser

import datetime


class GmailView:
    
    def __init__(self, control):
        self.control = control

        self.mail_items = []
        
        """Set-up Menu"""
        self.menu = gtk.Menu()
        self.menu.append(gtk.SeparatorMenuItem())
        self.about_item = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
        self.menu.append(self.about_item)
        self.quit_item = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        self.menu.append(self.quit_item)

        self.quit_item.connect('activate', gtk.main_quit)

        """Set-up Status Icon"""
        self.status_icon = gtk.status_icon_new_from_file('no_new.ico')
        self.status_icon.set_visible(True)
        
        self.status_icon.connect(   'popup-menu', 
                                    self.control.on_menu_popup,
                                    self.menu)

        self.status_icon.connect('activate', self.control.go_to_inbox)

        self.control.check_mail(self)
        
        gobject.timeout_add(5 * 60 * 1000, self.control.check_mail, self)

    """Set icon, and take dictionary to build menu items."""
    def new_mail(self, list):
        list.reverse()
        for email in list:
            item = GmailMessageItem(email['summary'], email['url'])
            item.connect('activate', self.control.open_email)
            self.menu.prepend(item)
            self.mail_items.append(item)

        print "New Mail" + " (" + str(datetime.datetime.now()) + ")"
        self.status_icon.set_tooltip('New Mail')
        self.status_icon.set_from_file('unread.ico')

    """Set icon, and remove all menu items besides About and Quit."""
    def no_mail(self):
        for item in self.mail_items:
            self.menu.remove(item)

        print "No Mail" + " (" + str(datetime.datetime.now()) + ")"
        self.status_icon.set_tooltip('No Mail')
        self.status_icon.set_from_file('no_new.ico') 


class GmailController:

    def __init__(self):
        self.gmail = GmailChecker()
    
    def check_mail(self, view):
        feed = self.gmail.feed()
        
        if len(feed.entries) > 0:
            list = []

            """Reversing list so that when added to menu they are in
            correct order."""
            for entry in feed.entries:
                value = entry.author_detail.name + ': ' + entry.title
                url = entry.link
                email = {'summary': value, 'url': url}
                list.append(email)
            
            view.new_mail(list)

        else:
            view.no_mail()
         
    def on_menu_popup(self, widget, button, time, menu):
        if button == 3:
            menu.show_all()
            menu.popup(None, None, None, button, time)
    
    def open_email(self, item):
        webbrowser.open_new_tab(item.url)

    def go_to_inbox(self, item):
        webbrowser.open_new_tab('http://mail.google.com/mail')


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

    def feed(self):
        opener = GmailURLOpener()
        f = opener.open(self.__class__.feed_url)
        feed_src = f.read()
        return feedparser.parse(feed_src)


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
    
    app = GmailView(GmailController())
    gtk.main()

