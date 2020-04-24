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
import inspect
import importlib

from PyQt5.QtGui import QIcon
from qgis.PyQt.QtCore import QCoreApplication

from qgis.core import (Qgis,
                       QgsApplication,
                       QgsProcessingAlgorithm,
                       QgsProcessingFeatureBasedAlgorithm,
                       QgsProcessingProvider,
                       QgsMessageLog
                      )
					  
from qgis import processing
from processing.core.ProcessingConfig import Setting, ProcessingConfig
from processing.script import ScriptUtils
from qgis.processing import alg as algfactory

pluginPath = os.path.join(os.path.dirname(__file__), os.pardir)

class OpenGXTProvider(QgsProcessingProvider):
    OPENGXT_ACTIVATED = 'OPENGXT_ACTIVATED'

    def __init__(self):
        """
        Default constructor.
        """
        QgsProcessingProvider.__init__(self)
        
    def load(self):
        ProcessingConfig.settingIcons[self.name()] = self.icon()
        ProcessingConfig.addSetting(Setting(self.name(), self.OPENGXT_ACTIVATED, 'Activate', True))
        ProcessingConfig.readSettings()
        self.refreshAlgorithms()
        return True

    def unload(self):
        """
        Unloads the provider. Any tear-down steps required by the provider
        should be implemented here.
        """
        ProcessingConfig.removeSetting(self.OPENGXT_ACTIVATED)

    def loadAlgorithms(self):
        """
        Loads all algorithms belonging to this provider.
        """
        self.algs = []
        folder = os.path.dirname(__file__)
        
        for entry in [f for f in os.listdir(folder)]:
            if entry.lower().endswith(".py"):
                moduleName = os.path.splitext(os.path.basename(entry))[0]
                filePath = os.path.abspath(os.path.join(folder, entry))
                
                try:
                    spec = importlib.util.spec_from_file_location(moduleName, filePath)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    try:
                        alg = algfactory.instances.pop().createInstance()
                        if alg is not None:
                            self.algs.append(alg)
                    except IndexError as ii:
                        for x in dir(module):
                            obj = getattr(module, x)
                            if inspect.isclass(obj) and issubclass(obj, (QgsProcessingAlgorithm, QgsProcessingFeatureBasedAlgorithm)) and obj.__name__ not in ("QgsProcessingAlgorithm", "QgsProcessingFeatureBasedAlgorithm"):
                                o = obj()
                                self.algs.append(o)
                except ImportError as e:
                    QgsMessageLog.logMessage(QCoreApplication.translate("ScriptUtils", "Could not import script algorithm '{}' from '{}'\n{}").format(moduleName, filePath, str(e)),
                                           QCoreApplication.translate("ScriptUtils", "Processing"),
                                           Qgis.Critical)
        for a in self.algs:
            self.addAlgorithm(a)

    def isActive(self):
        """Return True if the provider is activated and ready to run algorithms"""
        return ProcessingConfig.getSetting(self.OPENGXT_ACTIVATED)

    def setActive(self, active):
        ProcessingConfig.setSettingValue(self.OPENGXT_ACTIVATED, active)

    def id(self):
        """
        Returns the unique provider id, used for identifying the provider. This
        string should be a unique, short, character only string, eg "qgis" or
        "gdal". This string should not be localised.
        """
        return 'opengxt'

    def name(self):
        """
        Returns the provider name, which is used to describe the provider
        within the GUI.

        This string should be short (e.g. "Lastools") and localised.
        """
        return self.tr('OpenGXT - UN GeoAnalysis')

    def icon(self):
        """
        Should return a QIcon which is used for your provider inside
        the Processing toolbox.
        """
        return QIcon(os.path.join(pluginPath, "icons", "icon.png"))

    def longName(self):
        """
        Returns the a longer version of the provider name, which can include
        extra details such as version numbers. E.g. "Lastools LIDAR tools
        (version 2.2.1)". This string should be localised. The default
        implementation returns the same string as name().
        """
        return self.name()
