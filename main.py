import pygtk
import time
import threading
import socket
import select
import sys
import json
import gtk
import os
import gobject

class Main(object):
    HOST = "127.0.0.1"
    PORT = 5234
    entry = None

    def write_mes(self, mes):
        end_iter = self.buf.get_end_iter()
        self.buf.insert(end_iter, mes)
        self.save_history(mes)
        self.socket.send(mes)

    def append_text(self, widget, data=None):
        end_iter = self.buf.get_end_iter()
        mes = ""
        if not end_iter.is_start():
            mes = '\n'
        lt = time.localtime()
        mes += "(%i:%i:%i)\n" % (lt.tm_hour, lt.tm_min, lt.tm_sec)
        mes += "%s\n" % self.entry.get_text()
        self.write_mes(mes)

    def save_history(self, mes):
        f = open('history.txt', 'a')
        f.write(mes)
        f.close()
        
    def read_history(self):
        text = ""
        if os.path.exists('history.txt'):
            f = open('history.txt', 'r')
            text = f.read()
            f.close()
        return text

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def delete_event(self, widget, event, data=None):
        self.socket.close()
        print "delete event occurred"
        return False

    def read_sock(self, *args, **kwargs):
        data = self.socket.recv(1024)
        if data:
            self.write_mes(data)

    def __init__(self):
        self.buf = gtk.TextBuffer()
        self.buf.set_text(self.read_history())

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)

        self.vbox = gtk.VBox(False, 0)
        self.vbox.show()

        self.entry = gtk.Entry(max=0)
        self.entry.set_text("1qweqwe")
        self.entry.show()

        self.button = gtk.Button("SEND")
        self.button.connect("clicked", self.append_text, None)
        self.button.set_size_request(100, 50)

        self.textview = gtk.TextView()
        self.textview.show()
        self.textview.set_buffer(self.buf)

        self.vbox.add(self.textview)
        self.vbox.add(self.entry)
        self.vbox.add(self.button)

        self.window.add(self.vbox)
        self.window.set_size_request(400, 400)
        self.button.show()
        self.window.show()

        self.socket = serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.HOST, self.PORT))

        f = self.socket.makefile('r')
        gobject.io_add_watch(f, gobject.IO_IN, self.read_sock, self)

    def main(self):
        gtk.main()

if __name__ == "__main__":
    app = Main()
    app.main()
