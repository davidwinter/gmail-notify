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

        self.menu_items = {}

        check_interval = 5 * 60 * 1000
        
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

        self.control.check_mail(self.menu, self.menu_items,
                                self.status_icon)
        
        gobject.timeout_add(check_interval, self.control.check_mail,
                            self.menu, self.menu_items,
                            self.status_icon)


class GmailController:

    def __init__(self):
        self.gmail = GmailChecker()
    
    def check_mail(self, menu, menu_items, icon):
        feed = self.gmail.feed()
        
        if len(feed.entries) > 0:
            list = []

            for entry in feed.entries:
                value = entry.author_detail.name + ': ' + entry.title
                url = entry.link
                email = {'summary': value, 'url': url}
                list.append(email)

            list.reverse()
            
            self.new_mail(list, menu, menu_items, icon)

        else:
            self.no_mail(menu, menu_items, icon)

        return True

    def new_mail(self, list, menu, menu_items, icon):
        print
        menu_url_list = []
        for url in menu_items:
            menu_url_list.append(url)

        feed_url_list = []
        for email in list:
            feed_url_list.append(email['url'])

        menu_set, feed_set = set(menu_url_list), set(feed_url_list)
        to_remove = menu_set - feed_set
        to_add = feed_set - menu_set

        if to_add:
            for email in list:
                if email['url'] in to_add:
                    print email['summary']
                    item = GmailMessageItem(email['summary'], email['url'])
                    item.connect('activate', self.open_email)
                    menu.prepend(item)
                    menu_items[email['url']] = item

        if to_remove:
            for url in to_remove:
                menu.remove(menu_items[url])
                del menu_items[url]

        print "New Mail" + " (" + str(datetime.datetime.now()) + ")"
        icon.set_tooltip('New Mail')
        icon.set_from_file('unread.ico')


    def no_mail(self, menu, menu_items, icon):
        print
        for item in menu_items:
            menu.remove(menu_items[item])

        menu_items = {}

        print "No Mail" + " (" + str(datetime.datetime.now()) + ")"
        icon.set_tooltip('No Mail')
        icon.set_from_file('no_new.ico') 
         
    def on_menu_popup(self, widget, button, time, menu):
        if button == 3:
            menu.show_all()
            menu.popup(None, None, None, button, time)
    
    def open_email(self, item):
        webbrowser.open_new_tab(item.url)

    def go_to_inbox(self, item):
        webbrowser.open_new_tab('http://mail.google.com/mail')


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

