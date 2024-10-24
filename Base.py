# -*- coding: utf-8 -*-
"""
/***************************************************************************
 **Nombre del plugin
                                 A QGIS plugin
 **Descripcion
                             -------------------
        begin                : **Fecha
        copyright            : **COPYRIGHT
        email                : **Mail de contacto
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 #   any later version.                                                    *
 *                                                                         *
 ***************************************************************************/
"""
import os.path

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QAction
from qgis.core import *

import LandCoverAI.ui.resources_rc
from LandCoverAI.BaseDialog import BaseDialog


try:
    from pydevd import *
except ImportError:
    None

class Base:
    def __init__(self, iface):
        #settrace()  #Debe estar dentro de la clase que queremos depurar
        self.iface = iface

    def initGui(self):
        self.action = QAction(QIcon(":/myplugin/images/icon.jpg"), u"LandCoverAI", self.iface.mainWindow())
        #self.action.setToolTip("Tree detection")
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&LandCoverAI", self.action)



    def unload(self):
        self.iface.removePluginMenu(u"&LandCoverAI", self.action)
        self.iface.removeToolBarIcon(self.action)
 

    def run(self):
        self.dlg = BaseDialog(self.iface)  
        self.dlg.exec_()


