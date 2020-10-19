# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 679,370 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        fgSizer1 = wx.FlexGridSizer( 2, 2, 0, 0 )
        fgSizer1.SetFlexibleDirection( wx.BOTH )
        fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.x_speed = wx.Gauge( self, wx.ID_ANY, 255, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.x_speed.SetValue( 0 )
        fgSizer1.Add( self.x_speed, 0, wx.ALL, 5 )

        self.y_speed = wx.Gauge( self, wx.ID_ANY, 255, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.y_speed.SetValue( 0 )
        fgSizer1.Add( self.y_speed, 0, wx.ALL, 5 )

        self.z_speed = wx.Gauge( self, wx.ID_ANY, 255, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.z_speed.SetValue( 0 )
        fgSizer1.Add( self.z_speed, 0, wx.ALL, 5 )

        self.m_checkBox1 = wx.CheckBox( self, wx.ID_ANY, u"Xbox", wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.m_checkBox1, 0, wx.ALL, 5 )


        self.SetSizer( fgSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.m_checkBox1.Bind( wx.EVT_CHECKBOX, self.run_control )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def run_control( self, event ):
        event.Skip()


