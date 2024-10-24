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
import os
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout
from qgis.core import *
from qgis.gui import *
from PyQt5 import uic
from LandCoverAI.utils import *
from PyQt5.QtGui import QImage, QPixmap


try:
    from pydevd import *
except ImportError:
    None

#Compila el archivo 
#Se genera en memoria y no se ve
Ui_BaseDialog, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui/ui_BaseDialog.ui'),
    from_imports=True,
    import_from="LandCoverAI.ui")


class BaseDialog(QDialog, Ui_BaseDialog):
    def __init__(self, iface):
        QDialog.__init__(self)
        self.setupUi(self)
        self.iface = iface
        self.plugin_dir = os.path.dirname(os.path.abspath(__file__))
        self.new_dialog = None
        self.rectangleBounds = ""
        self.map_canvas = ""
        self.imagepath_previsualize = ""
        
        
    def selectionRectangle(self):
        project = QgsProject.instance()
        
        self.new_dialog = QDialog()
        self.new_dialog.setWindowTitle("LandCoverAI")
        self.new_dialog.setWindowModality(Qt.ApplicationModal)  
        self.new_dialog.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)  
        self.new_dialog.resize(800,600)
        
        
        map_canvas = QgsMapCanvas(self.new_dialog)
        map_canvas.setMinimumSize(800,600)
        
        layers = project.mapLayers()
        map_canvas_layer_list = [I for I in layers.values()]
        map_canvas.setLayers(map_canvas_layer_list)
        map_canvas.setExtent(self.iface.mapCanvas().extent())    
        
        rect_tool = RectangleMapTool(map_canvas, self.new_dialog)  # Instantiate your tool
        map_canvas.setMapTool(rect_tool)  # Activate the tool
        self.map_canvas = map_canvas
        self.new_dialog.show()
        self.new_dialog.raise_() 
        self.new_dialog.activateWindow() 
        
        def onDialogClosed():
                
            rect = rect_tool.rectangle()
            print("Coordenadas del área:", rect)
            self.rectangleBounds = rect
             
            
            if rect is None:
                warning_dialog_no_rectangle = QDialog()
                warning_dialog_no_rectangle.setMinimumSize(200,100)
                warning_dialog_no_rectangle.setWindowTitle("Warning")
                layout = QVBoxLayout()
                warning_message = QLabel("No se seleccionó ningún área")
                layout.addWidget(warning_message)
                warning_dialog_no_rectangle.setLayout(layout)
                warning_dialog_no_rectangle.exec_()
                self.imagePreview.clear()
                self.rectangleLabel.clear()
            
            else:
                self.printRectangleCoords()
                self.exportMap()
                self.displayImageLabel()
                

                
        
       
        self.new_dialog.finished.connect(onDialogClosed)
        

        
    def printRectangleCoords(self):
        
        rect_str = f"Min X: {self.rectangleBounds.xMinimum():.3f}, Min Y: {self.rectangleBounds.yMinimum():.3f}, Max X: {self.rectangleBounds.xMaximum():.3f}, Max Y: {self.rectangleBounds.yMaximum():.3f}"
        self.rectangleLabel.setText(rect_str)
        
    
    
    def exportMap(self):
        """
        Esta función solo sirve para previsualizar la imagen de una forma rápida y 
        el área que deseamos que posteriormente sea inferida.
        """
        
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(plugin_dir, "exportedImages")
        
   
        file_name = "previsualizeImage.png"    
        self.imagepath_previsualize = os.path.normpath(os.path.join(folder_path, file_name))
    
       
        map_settings = self.map_canvas.mapSettings()
        map_settings.setExtent(self.rectangleBounds)  
        
        
        exporter = QgsMapRendererParallelJob(map_settings)
        exporter.start()
        exporter.waitForFinished()
    
       
        image = exporter.renderedImage()
        
        # Guarda la imagen
        if image.save(self.imagepath_previsualize, 'PNG'):
            print(f"Map image successfully saved to {self.imagepath_previsualize}")
        else:
            print("Failed to save the image.")
            
  
    def displayImageLabel(self):
        
        pixmap = QPixmap(self.imagepath_previsualize)  
        self.imagePreview.setPixmap(pixmap)  
        self.imagePreview.setScaledContents(True)  
    
    
        
            