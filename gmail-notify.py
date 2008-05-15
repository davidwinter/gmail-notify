#!/usr/bin/env python

import gtk
import feedparser

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

    def menu_show(self, widget, button, time):

        if button == 3:
            item = gtk.MenuItem('test')
            self.view.menu.insert(item, 0)

            self.view.menu.show_all()
            self.view.menu.popup(None, None, None, button, time)
            

    def quit(self, widget):
        self.view.status_icon.set_visible(False)
        gtk.main_quit()

if __name__ == '__main__':
    app = GmailController()
    gtk.main()


