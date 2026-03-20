# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018  Rickard Lindberg, Roger Lindberg
#
# This file is part of Timeline.
#
# Timeline is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Timeline is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Timeline.  If not, see <http://www.gnu.org/licenses/>.

"""Font helpers used by the embedded GNUmed timeline viewer.

This module intentionally lives outside ``timelinelib.wxgui.components`` so it
can be imported without triggering that package's eager imports of humblewx-
dependent dialogs. The GNUmed timeline plugin only needs the font helpers for
rendering; keeping them here allows the plugin to continue in viewer mode even
when humblewx is unavailable.
"""

import wx


class Font(wx.Font):

    def __init__(self, point_size=12, family=wx.FONTFAMILY_DEFAULT, style=wx.FONTSTYLE_NORMAL,
                 weight=wx.FONTWEIGHT_NORMAL, underlined=False, face_name="", encoding=wx.FONTENCODING_DEFAULT,
                 wxcolor=wx.BLACK):
        self.wxcolor = wxcolor
        wx.Font.__init__(self, point_size, family, style, weight, underlined, face_name, encoding)

    def _get_wxcolor(self):
        return self.wxcolor

    def _set_wxcolor(self, wxcolor):
        self.wxcolor = wxcolor

    WxColor = property(_get_wxcolor, _set_wxcolor)

    def _get_wxfont(self):
        return self

    def _set_wxfont(self, wxfont):
        self.PointSize = wxfont.PointSize
        self.Family = wxfont.Family
        self.Style = wxfont.Style
        self.Weight = wxfont.Weight
        self.SetUnderlined(wxfont.GetUnderlined())
        self.FaceName = wxfont.FaceName
        self.Encoding = wxfont.Encoding

    WxFont = property(_get_wxfont, _set_wxfont)

    def serialize(self):
        return "%s:%s:%s:%s:%s:%s:%s:%s" % (
            self.PointSize,
            self.Family,
            self.Style,
            self.Weight,
            self.GetUnderlined(),
            self.FaceName,
            self.Encoding,
            self.WxColor,
        )

    def increment(self, step=2):
        self.PointSize += step

    def decrement(self, step=2):
        self.PointSize -= step


font_cache = {}


def deserialize_font(serialized_font):
    if serialized_font not in font_cache:
        bool_map = {"True": True, "False": False}
        (
            point_size,
            family,
            style,
            weight,
            underlined,
            facename,
            encoding,
            color,
        ) = serialized_font.split(":")
        color_args = color[1:-1].split(",")
        wxcolor = wx.Colour(
            int(color_args[0]),
            int(color_args[1]),
            int(color_args[2]),
            int(color_args[3])
        )
        font = Font(
            int(point_size),
            int(family),
            int(style),
            int(weight),
            bool_map[underlined],
            facename,
            int(encoding),
            wxcolor
        )
        font_cache[serialized_font] = font
    return font_cache[serialized_font]


def set_minor_strip_text_font(font, dc, force_bold=False, force_normal=False, force_italic=False, force_upright=False):
    set_text_font(font, dc, force_bold, force_normal, force_italic, force_upright)


def set_major_strip_text_font(font, dc, force_bold=False, force_normal=False, force_italic=False, force_upright=False):
    set_text_font(font, dc, force_bold, force_normal, force_italic, force_upright)


def set_balloon_text_font(font, dc, force_bold=False, force_normal=False, force_italic=False, force_upright=False):
    set_text_font(font, dc, force_bold, force_normal, force_italic, force_upright)


def set_legend_text_font(font, dc):
    set_text_font(font, dc)


def set_text_font(selectable_font, dc, force_bold=False, force_normal=False, force_italic=False, force_upright=False):
    font = deserialize_font(selectable_font)
    old_weight = font.Weight
    old_style = font.Style
    if force_bold:
        font.Weight = wx.FONTWEIGHT_BOLD
    elif force_normal:
        font.Weight = wx.FONTWEIGHT_NORMAL
    if force_italic:
        font.Style = wx.FONTSTYLE_ITALIC
    elif force_upright:
        font.Style = wx.FONTSTYLE_NORMAL
    dc.SetFont(font)
    dc.SetTextForeground(font.WxColor)
    font.Style = old_style
    font.Weight = old_weight


def edit_font_data(parent_window, font):
    data = wx.FontData()
    data.SetInitialFont(font)
    data.SetColour(font.WxColor)
    dialog = wx.FontDialog(parent_window, data)
    try:
        if dialog.ShowModal() == wx.ID_OK:
            font_data = dialog.GetFontData()
            font.WxFont = font_data.GetChosenFont()
            font.WxColor = font_data.GetColour()
            return True
        else:
            return False
    finally:
        dialog.Destroy()
