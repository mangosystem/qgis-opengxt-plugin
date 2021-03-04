# -*- coding: utf-8 -*-

"""
/***************************************************************************
Name                 : OpenGXT for Processing Toolbox
Description          : OpenGXT for Processing Toolbox
Date                 : 2019-10-25
copyright            : (C) 2019 by Mango System inc.
email                : mapplus@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = 'Mango System inc.'
__date__ = '2019-10-25'
__copyright__ = '(C) 2019 by Mango System inc.'
__revision__ = '$Format:%H$'

import os
import sys
import inspect
import webbrowser

from qgis.PyQt.QtCore import (QCoreApplication, 
                              QTranslator,
                              QSettings)
                              
from qgis.core import (QgsProcessingAlgorithm, 
                       QgsApplication)
                       
from .processing.OpenGXTProvider import OpenGXTProvider

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


class OpenGXTPlugin(object):

    def __init__(self):
        self.provider = None
        
        self.plugin_dir = os.path.dirname(__file__)
        locale = QSettings().value("locale/userLocale")[0:2]
        locale_path = os.path.join(self.plugin_dir, "i18n", "opengxt_{}.qm".format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

    def initProcessing(self):
        """Init Processing provider for QGIS >= 3.8."""
        self.provider = OpenGXTProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        self.initProcessing()

    def unload(self):
        QgsApplication.processingRegistry().removeProvider(self.provider)

    def showHelp(self):
        webbrowser.open("https://github.com/mangosystem/oepngxt")
