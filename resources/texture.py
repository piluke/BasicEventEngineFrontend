# Copyright (c) 2017-18 Luke Montalvo <lukemontalvo@gmail.com>
#
# This file is part of BEEF.
# BEEF is free software and comes with ABSOLUTELY NO WARANTY.
# See LICENSE for more details.

try:
	import wx
except ImportError:
	raise ImportError("The wxPython module is required to run this program")

import copy
import os
import shutil

from resources.base import BEEFBaseResource
from resources.enum import EResource

class BEEFTexture(BEEFBaseResource):
	def __init__(self, top, name):
		BEEFBaseResource.__init__(self, top, name)
		self.path = "/resources/textures/"
		self.type = EResource.TEXTURE
		self.properties = {
			"path": "",
			"width": 0,
			"height": 0,
			"subimage_amount": 1,
			"speed": 1.0
		}

	def getInit(self):
		init = ""
		if self.properties["subimage_amount"] > 1:
			init += "\n\t\t\t{name}->set_subimage_amount({si_amount}, {si_width});".format(name=self.name, si_amount=self.properties["subimage_amount"], si_width=self.properties["width"]//self.properties["subimage_amount"])
			#if self.properties["speed"] != 1.0:
			init += "\n\t\t\t{name}->set_speed({speed});".format(name=self.name, speed=self.properties["speed"])
		init += "\n\t\t\t{name}->load();".format(name=self.name)
		return init

	def initPageSpecific(self):
		self.gbs = wx.GridBagSizer(12, 2)

		self.pageAddStatictext("Name:", (0,0))
		self.pageAddTextctrl("tc_name", self.name, (1,0), (1,2))
		self.pageAddButton("bt_edit", "Edit Image", (2,0))
		self.pageAddButton("bt_import", "Import", (2,1))

		self.pageAddStatictext("Subimage amount:", (3,0))
		self.pageAddTextctrl("tc_subimage_amount", str(self.properties["subimage_amount"]), (3,1))

		self.pageAddStatictext("Animation speed:", (4,0))
		self.pageAddTextctrl("tc_speed", str(self.properties["speed"]), (4,1))

		path = self.properties["path"]
		imgpath = self.top.rootDir+path

		w = self.properties["width"] // self.properties["subimage_amount"]
		h = self.properties["height"]
		self.pageAddBitmap("bmp_texture", imgpath, (5,0), imgsize=self.getBmpSize((w, h), (128,128)))
		self.cropBmp(self.properties["subimage_amount"])

		self.pageAddStatictext("Dimensions: {}px by {}px".format(w, h), (6,0), name="st_dimensions")

		self.pageAddStatictext("Path: {}".format(path), (7,0), name="st_path")

		self.pageAddButton("bt_ok", "OK", (8,0))

		self.sizer = wx.BoxSizer()
		self.sizer.Add(self.gbs, 1, wx.ALL | wx.EXPAND, 20)
		self.page.SetSizer(self.sizer)

	def getBmpSize(self, size, maxSize):
		width, height = size
		maxW, maxH = maxSize

		w = maxW
		h = maxW*max(height,1)/max(width,1)

		if h > maxH:
			h = maxH
			w = maxH*w/h

		return (w,h)
	def cropBmp(self, subimage_amount):
		w = self.properties["width"] // subimage_amount
		h = self.properties["height"]

		path = self.top.rootDir + self.properties["path"]
		if os.path.isfile(path):
			self.inputs["bmp_texture"].SetBitmap(wx.Bitmap(wx.Image(path)).GetSubBitmap(wx.Rect(
				0, 0,
				w, h
			)))

	def onTextSpecific(self, event):
		tc = event.GetEventObject()
		if tc == self.inputs["tc_subimage_amount"] and tc.GetValue():
			self.cropBmp(int(tc.GetValue()))

		return True
	def onButtonSpecific(self, event):
		bt = event.GetEventObject()
		if bt == self.inputs["bt_ok"]:
			self.destroyPage()
		elif bt == self.inputs["bt_edit"]:
			return self.top.editResource(self)
		elif bt == self.inputs["bt_import"]:
			wildcards = (
				"PNG Image (*.png)|*.png|"
				"All files (*)|*"
			)

			d = self.top.rootDir+os.path.dirname(self.properties["path"])
			f = os.path.basename(self.properties["path"])
			if not self.properties["path"]:
				d = os.getcwd()
				f = ""

			dialog = wx.FileDialog(
				self.top, message="Import Texture",
				defaultDir=d,
				defaultFile=f,
				wildcard=wildcards,
				style=wx.FD_OPEN
			)

			if dialog.ShowModal() == wx.ID_OK:
				path = dialog.GetPath()
				ext = os.path.splitext(path)[1]

				self.properties["path"] = self.path+self.name+ext
				shutil.copyfile(path, self.top.rootDir+self.properties["path"])

				self.update()
			else:
				dialog.Destroy()
				return False

			dialog.Destroy()

		return True

	def update(self):
		self.inputs["st_path"].SetLabel("Path: {}".format(self.properties["path"]))

		img = wx.Image(self.top.rootDir+self.properties["path"])
		w = img.GetWidth()
		h = img.GetHeight()
		self.properties["width"] = w
		self.properties["height"] = h

		img.Rescale(*self.getBmpSize((w, h), (128,128)))
		self.inputs["bmp_texture"].SetBitmap(wx.Bitmap(img))

		self.inputs["st_dimensions"].SetLabel("Dimensions: {}px by {}px".format(w, h))

	def commitPage(self):
		if self.page:
			tc_name = self.inputs["tc_name"]
			if tc_name.GetValue() != self.name:
				self.rename(tc_name.GetValue())

			self.properties["subimage_amount"] = int(self.inputs["tc_subimage_amount"].GetValue())
			self.properties["speed"] = float(self.inputs["tc_speed"].GetValue())
	def moveTo(self, name, newfile):
		if self.properties["path"]:
			ext = os.path.splitext(self.properties["path"])[1]
			os.rename(self.top.rootDir+self.properties["path"], newfile+ext)
			self.properties["path"] = self.path+name+ext
			self.inputs["st_path"].SetLabel("Path: {}".format(self.properties["path"]))

	def MenuDuplicate(self, event):
		r = BEEFTexture(self.top, None)
		r.properties = copy.deepcopy(self.properties)
		self.top.addTexture(self.name, r)
