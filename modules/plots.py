import os

from datetime import datetime
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

from modules.ui_plot import Ui_PlotWindow

from functools import partial
from config.functions import *
from config.defs import *
from functions import * # messageBox

from functools import partial

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from random import randint

pg.setConfigOptions(antialias=True)
pg.setConfigOption('foreground', '#000000')


class PlotWindow(QMainWindow):
    def __init__(self, plot_parameters, enable):
        #super().__init__()
        QMainWindow.__init__(self)
        global p2
        self.ui = Ui_PlotWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui
        self.widgets = widgets
        self.plot_error = False
        self.plot_parameters = plot_parameters
        try:
            parameters_obligatory = ["x","y1","y2","titles","name"] # y2 could be blank [] but must exists
            for param in parameters_obligatory:
                if param not in plot_parameters:
                    self.plot_error = True
                    retval = messageBox(self,"Problem initializing class Plot","Plot graph parameter not sended ('"+param+"')","error")                
                    break
        except:
            self.plot_parameters = ""
            self.plot_error = True
            retval = messageBox(self,"Problem initializing class Plot","Plot graph not initialized","error")  

        boolean_values = [True,False]

        def updateViews():
            global p2
            ## view has resized; update auxiliary views to match
            p2.setGeometry(p.getViewBox().sceneBoundingRect())
            
            ## need to re-update linked axes since this was called
            ## incorrectly while views had different shapes.
            ## (probably this should be handled in ViewBox.resizeEvent)
            p2.linkedViewChanged(p.getViewBox(), p2.XAxis)

        windowTitle = "Plot window - " + plot_parameters["name"]


        if not self.plot_error:
            
    
            p = widgets.plot_widget
            #widgets.plot_widget.setBackground('#ffffff') # default white
            
            p.setWindowTitle(windowTitle)

            # ------------------------------------------
            # Configure optional parameters plot window
            # ------------------------------------------
            # -----------
            # background
            # -----------
            if "foreground" in plot_parameters:
                pg.setConfigOption('foreground',plot_parameters["foreground"]) # option available in second graph! (global configuration)
            # -----------
            # background
            # -----------
            if "background" in plot_parameters:
                p.setBackground(plot_parameters["background"])
            else:
                p.setBackground('#ffffff')
            # --------
            # margins
            # --------
            if "margins" in plot_parameters:
                if len(plot_parameters["margins"])==4:
                    p.setContentsMargins(plot_parameters["margins"][0], plot_parameters["margins"][1], plot_parameters["margins"][2], plot_parameters["margins"][3])
            

            # ----------
            # showgrid
            # ----------
            if "showgrid" in plot_parameters:
                if "x" in plot_parameters["showgrid"] and "y1" in plot_parameters["showgrid"]:
                    if plot_parameters["showgrid"]["x"] in boolean_values and plot_parameters["showgrid"]["y1"] in boolean_values:
                        p.showGrid(x=plot_parameters["showgrid"]["x"],y=plot_parameters["showgrid"]["y1"])

            # --------
            # xrange
            # --------
            if "xrange" in plot_parameters:
                if "min" in plot_parameters["xrange"] and "max" in plot_parameters["xrange"]:
                    p.setXRange(plot_parameters["xrange"]["min"],plot_parameters["xrange"]["max"],padding=0)
            # --------
            # yrange
            # --------
            if "yrange" in plot_parameters:
                if "min" in plot_parameters["yrange"] and "max" in plot_parameters["yrange"]:
                    p.setYRange(plot_parameters["yrange"]["min"],plot_parameters["yrange"]["max"],padding=0)
            
            # --------
            # multiaxis
            # --------
            if "multiaxis" not in plot_parameters:
                plot_parameters["multiaxis"] = True

            # -----------------------------------------------------
            # -----------------------------------------------------

            # default styles
            label_style_title = {"color": "#000000", "font-size": "14pt"} # title
            label_style_top = label_style_bottom = label_style_left = label_style_right = {"color": "#DDDDDD", "font-size": "12pt"} # axis x, y & y2
            if "styles_titles" in plot_parameters:
                if len(plot_parameters["styles_titles"]==5):
                    label_style_title = plot_parameters["styles_titles"]["title"]
                    label_style_top = plot_parameters["styles_titles"]["top"]
                    label_style_bottom = plot_parameters["styles_titles"]["bottom"]
                    label_style_left = plot_parameters["styles_titles"]["left"]
                    label_style_right = plot_parameters["styles_titles"]["right"]

            # ---------
            # printing
            # ---------
            # Default values

            if plot_parameters["multiaxis"]:
                # only 2 colors, symbols
                colors_default = ["r","g"]
                symbols_default = ["+","o"]
            else:
                if "y5" in plot_parameters:
                    # until 100
                    colors_default = []
                    for i in range(100):
                        # random color
                        colors_default.append('#%06X' % randint(0, 0xFFFFFF))
                else:
                    # only four colours (for ex. solarmems test)
                    colors_default = ["r","g","y","b"]
                    symbols_default = ["o","o","o","o"]   

            style_default = Qt.SolidLine
            width_default = 2
            antialias_default = True
            # ----------
            colors_y = []
            colors_y.append(colors_default[0])
            styles_y = []
            styles_y.append(style_default)
            widths_y = []
            widths_y.append(width_default)
            symbols_y = []
            symbols_y.append(symbols_default)
            names_y = []
            
            if not plot_parameters["multiaxis"]:
                names_y.append(plot_parameters["titles"]["left"] + "_1")
            else:
                names_y.append(plot_parameters["titles"]["left"])

            antialias_y = []
            antialias_y.append(antialias_default)

            # ------------------------
            for i in range(1,101):
                y_axis_name = "y" + str(i+1)
                if y_axis_name in plot_parameters:
                    colors_y.append(colors_default[i])
                    styles_y.append(style_default)
                    widths_y.append(width_default)
                    symbols_y.append(symbols_default)
                    antialias_y.append(antialias_default)
                    if plot_parameters["multiaxis"]:
                        name_y = "plot" + str(i+1)
                        if "right" in plot_parameters["titles"]:
                            name_y = plot_parameters["titles"]["right"]
                    else:
                        name_y = plot_parameters["titles"]["left"] + "_" + str(i+1)
                    names_y.append(name_y)
                    
                else:
                    break

            # getting style from plot_parameters
            if "styles_graphs" in plot_parameters:
                for i in range(1,101):
                    y_axis_name = "y" + str(i)
                    if y_axis_name in plot_parameters["styles_graph"]:
                        if "color" in plot_parameters["styles_graph"][y_axis_name]:
                            colors_y[i-1] = plot_parameters["styles_graph"][y_axis_name]["color"]
                        if "style" in plot_parameters["styles_graph"][y_axis_name]:
                            styles_y[i-1] = plot_parameters["styles_graph"][y_axis_name]["style"]
                        if "width" in plot_parameters["styles_graph"][y_axis_name]:
                            widths_y[i-1] = plot_parameters["styles_graph"][y_axis_name]["width"]
                        if "symbol" in plot_parameters["styles_graph"][y_axis_name]:
                            symbols_y[i-1] = plot_parameters["styles_graph"][y_axis_name]["symbol"]
                        if "name" in plot_parameters["styles_graph"][y_axis_name]:
                            name_y = plot_parameters["styles_graph"][y_axis_name]["name"]
                        if "antialias" in plot_parameters["styles_graph"][y_axis_name]:
                            antialias_y[i-1] = plot_parameters["styles_graph"][y_axis_name]["antialias"]
                    else:
                        break
            
            # -----------
            # units
            # -----------
            units_bottom = ""
            units_left = ""
            units_right = ""

            if "units" in plot_parameters:
                if len(plot_parameters["units"])==3 and plot_parameters["multiaxis"] and "bottom" in plot_parameters["units"] and "left" in plot_parameters["units"] and "right" in plot_parameters["units"]:
                    units_bottom = plot_parameters["units"]["bottom"]
                    units_left = plot_parameters["units"]["left"]
                    units_right = plot_parameters["units"]["right"]
                if len(plot_parameters["units"])==2 and not plot_parameters["multiaxis"] and "bottom" in plot_parameters["units"] and "left" in plot_parameters["units"]:
                    units_bottom = plot_parameters["units"]["bottom"]
                    units_left = plot_parameters["units"]["left"]
            
            # ----------
            # legend
            # ----------
            if "legend" in plot_parameters:
                if plot_parameters["legend"] in boolean_values:
                    if plot_parameters["legend"]:
                        p.addLegend()
            # bottom
            
            p.setLabel('bottom', plot_parameters["titles"]["bottom"], units=units_bottom, **label_style_bottom)    
            p.getAxis('bottom').setPen(pg.mkPen(color='#000000', width=3))
            # left
            p.setLabel('left', plot_parameters["titles"]["left"], units=units_left, **label_style_left)
            pen_y = pg.mkPen(color = colors_y[0], width = widths_y[0])
            #p.getAxis('left').setPen(pg.mkPen(color='#c4380d', width=3))
            p.getAxis('left').setPen(pen_y)

            # set curve empty
            curve = p.plot(x=[], y=[], pen=pg.mkPen(color=colors_y[0], width=widths_y[0], style = styles_y[0]), symbol=symbols_y[0], name=names_y[0], antialias = antialias_y[0])
            # **Supported symbols:**

            # * 'o'  circle (default)
            # * 's'  square
            # * 't'  triangle
            # * 'd'  diamond
            # * '+'  plus
            # * 't1' triangle pointing upwards
            # * 't2'  triangle pointing right side
            # * 't3'  triangle pointing left side
            # * 'p'  pentagon
            # * 'h'  hexagon
            # * 'star'
            # * 'x'  cross
            # * 'arrow_up'
            # * 'arrow_right'
            # * 'arrow_down'
            # * 'arrow_left'
            # * 'crosshair'
            # * any QPainterPath to specify custom symbol shapes.

            

            if len(plot_parameters["y2"])==len(plot_parameters["x"]): # check if exists y2
                if plot_parameters["multiaxis"]:
                    # if multiaxis only 2 curves in plot
                    # right
                    p.showAxis('right')
                    p.setLabel('right', plot_parameters["titles"]["right"], units=units_right, **label_style_right)
                    pen_y2 = pg.mkPen(color = colors_y[1], width = widths_y[1])
                    p.getAxis('right').setPen(pen_y2)
                    # p2
                    p2 = pg.ViewBox()
                    p.scene().addItem(p2)
                    p.getAxis('right').linkToView(p2)
                    p2.setXLink(p)
                    
                    curve2 = pg.PlotDataItem(pen=pg.mkPen(color=colors_y[1], width=widths_y[1], style = styles_y[1]))  
                    p2.addItem(curve2)

                #p.plot(plot_parameters["x"], plot_parameters["y"], pen = pg.mkPen(color = color_y, style = style_y, width = width_y), symbol=symbol_y, name=name_y, antialias = antialias_y)

                    updateViews()
                    p.getViewBox().sigResized.connect(updateViews)
                    curve2.setData(np.array(plot_parameters["x"],dtype=float),np.array(plot_parameters["y2"],dtype=float), symbol=symbols_y[1], name=names_y[1], antialias = antialias_y[1])

                    

                else:
                    # if not add all curves to plot (max. 100 curves)
                    for i in range(1,101):
                        y_axis_name = "y" + str(i+1)
                        curve_name = "curve" + y_axis_name
                        myVars = vars()
                        if (y_axis_name in plot_parameters) and len(plot_parameters[y_axis_name])==len(plot_parameters["x"]):
                            myVars[curve_name] = p.plot(x=[], y=[], pen=pg.mkPen(color=colors_y[i], width=widths_y[i], style = styles_y[i]), symbol=symbols_y[0], name=names_y[i], antialias = antialias_y[i])
                            myVars[curve_name].setData(np.array(plot_parameters["x"],dtype=float),np.array(plot_parameters[y_axis_name],dtype=float))
                        else:
                            break
            # add curve 1
            curve.setData(np.array(plot_parameters["x"],dtype=float),np.array(plot_parameters["y1"],dtype=float))
            
                        



    

        self.setWindowTitle(windowTitle)
        # Hide buttons right
        self.setMinimumWidth(740)
        self.setMaximumWidth(740)




