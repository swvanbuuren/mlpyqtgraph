""" GLTextItem module with advanced text alignment """

import OpenGL.GL as gl  # noqa
import numpy as np
import pyqtgraph.functions as fn
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.opengl import items

__all__ = ['GLTextItem']


class GLTextItem(items.GLTextItem.GLTextItem):
    """ GLTextItem extended with advanced text alignment """

    def __init__(self, parentItem=None, **kwds):
        """All keyword arguments are passed to setData()"""
        super().__init__(parentItem=parentItem)
        self.alignment = QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom
        self.setData(**kwds)

    def setData(self, **kwds):
        """
        Update the data displayed by this item. All arguments are optional;
        for example it is allowed to update text while leaving colors unchanged, etc.

        ====================  ==================================================
        **Arguments:**
        ------------------------------------------------------------------------
        pos                   (3,) array of floats specifying text location.
        color                 QColor or array of ints [R,G,B] or [R,G,B,A]. (Default: Qt.white)
        text                  String to display.
        font                  QFont (Default: QFont('Helvetica', 16))
        alignment             QtCore.Qt.AlignmentFlag (Default: QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        ====================  ==================================================
        """
        args = ['pos', 'color', 'text', 'font', 'alignment']
        for k in kwds.keys():
            if k not in args:
                raise ValueError('Invalid keyword argument: %s (allowed arguments are %s)' % (k, str(args)))
        for arg in args:
            if arg in kwds:
                value = kwds[arg]
                if arg == 'pos':
                    if isinstance(value, np.ndarray):
                        if value.shape != (3,):
                            raise ValueError('"pos.shape" must be (3,).')
                    elif isinstance(value, (tuple, list)):
                        if len(value) != 3:
                            raise ValueError('"len(pos)" must be 3.')
                elif arg == 'color':
                    value = fn.mkColor(value)
                elif arg == 'font':
                    if isinstance(value, QtGui.QFont) is False:
                        raise TypeError('"font" must be QFont.')
                setattr(self, arg, value)
        self.update()

    def align_text(self, pos):
        """
        Aligns the text at the given position according to the given alignment.
        """
        font_metrics = QtGui.QFontMetrics(self.font)
        rect = font_metrics.tightBoundingRect(self.text)
        width = rect.width()
        height = rect.height()
        dx = dy = 0.0
        if self.alignment & QtCore.Qt.AlignRight:
            dx = width
        if self.alignment & QtCore.Qt.AlignHCenter:
            dx = width / 2.0
        if self.alignment & QtCore.Qt.AlignTop:
            dy = height
        if self.alignment & QtCore.Qt.AlignVCenter:
            dy = height / 2.0
        pos.setX(pos.x() - dx)
        pos.setY(pos.y() - dy)

    def __project(self, obj_pos, modelview, projection, viewport):
        text_pos = super().__project(obj_pos, modelview, projection, viewport)
        self.align_text(text_pos)
        return text_pos
