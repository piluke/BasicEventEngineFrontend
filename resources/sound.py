# Copyright (c) 2017 Luke Montalvo <lukemontalvo@gmail.com>
#
# This file is part of BEE.
# BEE is free software and comes with ABSOLUTELY NO WARANTY.
# See LICENSE for more details.

try:
	import wx
except ImportError:
	raise ImportError("The wxPython module is required to run this program")

import wx.adv

import copy
import os
import shutil

from resources.base import BEEFBaseResource

class BEEFSound(BEEFBaseResource):
	def __init__(self, top, name):
		BEEFBaseResource.__init__(self, top, name)
		self.path = "/resources/sounds/"
		self.type = 1
		self.sound = None
		self.properties = {
			"path": "",
			"volume": 100,
			"pan": 0
		}

	def initPageSpecific(self):
		self.gbs = wx.GridBagSizer(12, 2)

		self.pageAddStatictext("Name:", (0,0))
		self.pageAddTextctrl("tc_name", self.name, (1,0), (1,2))
		self.pageAddButton("bt_edit", "Edit Sound", (2,0))
		self.pageAddButton("bt_import", "Import", (2,1))

		self.pageAddStatictext("Volume:", (3,0))
		self.pageAddSlider("sl_volume", self.properties["volume"], (4,0))

		if self.properties["path"]:
			self.sound = wx.adv.Sound(self.top.tmpDir+self.properties["path"])

		playsizer = wx.BoxSizer()
		bt_play = self.pageMakeBmpbutton("bt_play", "images/sound/play.png", tooltip="Play Sound")
		playsizer.Add(bt_play, 1, wx.ALL | wx.EXPAND, 0)
		bt_loop = self.pageMakeBmpbutton("bt_loop", "images/sound/loop.png", tooltip="Loop Sound")
		playsizer.Add(bt_loop, 1, wx.ALL | wx.EXPAND, 0)
		bt_stop = self.pageMakeBmpbutton("bt_stop", "images/sound/stop.png", tooltip="Stop Sound")
		playsizer.Add(bt_stop, 1, wx.ALL | wx.EXPAND, 0)
		self.gbs.Add(playsizer, (4,1), (1,1))

		path = self.properties["path"]
		self.pageAddStatictext("Path: {}".format(path), (5,0), name="st_path")

		self.pageAddButton("bt_ok", "OK", (6,0))

		self.sizer = wx.BoxSizer()
		self.sizer.Add(self.gbs, 1, wx.ALL | wx.EXPAND, 20)
		self.page.SetSizer(self.sizer)

	def onTextSpecific(self, event):
		return True
	def onCheckBoxSpecific(self, event):
		pass
	def onButtonSpecific(self, event):
		bt = event.GetEventObject()
		if bt == self.inputs["bt_ok"]:
			self.destroyPage()
		elif bt == self.inputs["bt_edit"]:
			return self.top.editResource(self)
		elif bt == self.inputs["bt_import"]:
			wildcards = (
				"WAV Sound (*.wav)|*.wav|"
				"All files (*)|*"
			)

			d = self.top.tmpDir+os.path.dirname(self.properties["path"])
			f = os.path.basename(self.properties["path"])
			if not self.properties["path"]:
				d = os.getcwd()
				f = ""

			dialog = wx.FileDialog(
				self.top, message="Import Sound",
				defaultDir=d,
				defaultFile=f,
				wildcard=wildcards,
				style=wx.FD_OPEN
			)

			if dialog.ShowModal() == wx.ID_OK:
				path = dialog.GetPath()
				ext = os.path.splitext(path)[1]

				self.properties["path"] = self.path+self.name+ext
				shutil.copyfile(path, self.top.tmpDir+self.properties["path"])

				self.update()
			else:
				dialog.Destroy()
				return False

			dialog.Destroy()
		elif bt == self.inputs["bt_play"]:
			if self.sound and self.sound.IsOk():
				self.sound.Play(wx.adv.SOUND_ASYNC)
			return False
		elif bt == self.inputs["bt_loop"]:
			if self.sound and self.sound.IsOk():
				self.sound.Play(wx.adv.SOUND_ASYNC | wx.adv.SOUND_LOOP)
			return False
		elif bt == self.inputs["bt_stop"]:
			if self.sound and self.sound.IsOk():
				self.sound.Stop()
			return False

		return True
	def onSliderSpecific(self, event):
		return True
	def onSpinCtrlSpecific(self, event):
		pass
	def onListEditSpecific(self, event):
		pass

	def update(self):
		self.inputs["st_path"].SetLabel("Path: {}".format(self.properties["path"]))

	def commitPage(self):
		if self.page:
			tc_name = self.inputs["tc_name"]
			if tc_name.GetValue() != self.name:
				self.rename(tc_name.GetValue())

			sl_volume = self.inputs["sl_volume"]
			self.properties["volume"] = sl_volume.GetValue()
	def moveTo(self, name, newfile):
		ext = os.path.splitext(self.properties["path"])[1]
		os.rename(self.top.tmpDir+self.properties["path"], newfile+ext)
		self.properties["path"] = self.path+name+ext
		self.inputs["st_path"].SetLabel("Path: {}".format(self.properties["path"]))

	def MenuDuplicate(self, event):
		r = BEEFSound(self.top, None)
		r.properties = copy.deepcopy(self.properties)
		self.top.addSound(self.name, r)