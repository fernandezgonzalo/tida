#!/usr/bin/env python

import os
from gi.repository import Gtk
from gi.repository import Vte
from gi.repository import GLib
from gi.repository import Keybinder
from gi.repository import Gdk


class Tida(Gtk.Window):
	"""A micro-drop-down terminal like TILDA"""
	def __init__(self, config=None):
		Gtk.Window.__init__(self)
		self.init_config(config)
		self.init_icon()
		self.init_terminal()
		Gtk.main()
		
	def init_config(self, config=None):
		"""Initialise the program with config if exists, else set default values"""
		if config != None:
			self.set_default_size(config['width'], config['heigth'])
			self.set_decorated(config['decorated'])
			self.set_skip_taskbar_hint(config['skip_taskbar_hint'])
			self.set_keep_above(config['keep_above'])
			self.set_skip_pager_hint(config['skip_pager_hint'])
			self.set_modal(config['modal'])
						
			s = Gdk.Screen.get_default()
			c = (s.get_width() - self.get_size()[0]) / 2.
			self.move(int(c), 0)
		else:
			self.set_decorated(False)
			self.set_skip_taskbar_hint(True)
			self.set_keep_above(True)
			self.set_skip_pager_hint(False)
			self.set_modal(False)
			self.set_default_size(720, 300)
			self.move(323, 0)
		self.init_keybinder(config)
		
	def init_icon(self):
		"""Initialise status icon"""
		self.status_icon = Gtk.StatusIcon()
		abs_file_name = os.path.join(os.path.dirname(__file__), "terminal.png")
		self.status_icon.set_from_file(abs_file_name)
		self.status_icon.set_title("StatusIcon TIDA")
		self.status_icon.set_tooltip_text("TIDA :>")
		
	def init_terminal(self):
		"""Initialise and add new Vte Terminal to Window"""
		self.term = Vte.Terminal()
		self.term.set_scrollback_lines(-1)
		self.term.connect('child-exited', Gtk.main_quit)
		self.term.fork_command_full(Vte.PtyFlags.DEFAULT, os.environ['HOME'], ['/usr/bin/bash'], [], GLib.SpawnFlags.DO_NOT_REAP_CHILD, None, None)
		
		self.add(self.term)
		self.connect('delete-event', Gtk.main_quit)
		
		
	def init_keybinder(self, config):
		"""Initialise keybinder and bind some keys (toggle, copy, paste)"""
		Keybinder.init()
		Keybinder.set_use_cooked_accelerators(False)
		self.bind_all_key(config['key_toggle_visibility'],
							config['key_copy_to_clipboard'],
							config['key_paste_from_clipboard'])

		
	def bind_all_key(self, key_toggle, key_copy, key_paste):
		"""Bind all keys used with tida"""
		Keybinder.bind(key_toggle, self.callback_toggle_visibility, "asd")
		Keybinder.bind(key_copy, self.callback_copy, "asd")
		Keybinder.bind(key_paste, self.callback_paste, "asd")

	
	def callback_copy(self, key, asd):
		"""Callback function used when press the shortcut for copy to clipboard"""
		if self.is_visible():
			self.term.copy_clipboard()
			return True
		return False
	
	def callback_paste(self, key, asd):
		"""Callback function used when press the shortcut for paste from clipboard"""
		if self.is_visible():
			self.term.paste_clipboard()
			return True
		return False
			
	def callback_toggle_visibility(self, key, asd):
		"""Callback function used when press the shortcut for toggle visibility of tida"""
		if self.is_visible():
			self.hide()
		else:
			self.show_all()

