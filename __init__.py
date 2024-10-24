# -*- coding: utf-8 -*-
import sys

try:
    sys.path.append(
        "C:/Users/Enrique/Desktop/eclipse/plugins/org.python.pydev.core_12.2.0.202409031913/pysrc"
    )
    from pydevd import *
except ImportError:
    None


def classFactory(iface):
    from .Base import Base
    return Base(iface)
