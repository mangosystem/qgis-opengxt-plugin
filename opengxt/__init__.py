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
 This script initializes the plugin, making it known to QGIS.
"""

__author__ = 'Mango System inc.'
__date__ = '2019-10-25'
__copyright__ = '(C) 2019 by Mango System inc.'


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load OpenGXT class from file OpenGXT.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .OpenGXTPlugin import OpenGXTPlugin
    return OpenGXTPlugin()
