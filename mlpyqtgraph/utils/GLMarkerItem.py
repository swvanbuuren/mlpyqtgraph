"""
GLMarkerItem - Render various marker types on 3D GL scenes using QPainter.

Supports multiple marker types with configurable properties including size,
stroke width, stroke color, fill color, and transparency.
"""

import math
from enum import Enum
import importlib
from typing import List, Optional, Tuple

from pyqtgraph.opengl import GLGraphicsItem
from pyqtgraph.Qt import QtCore, QtGui, QT_LIB, QtVersion

if int(QtVersion.split(".")[0]) >= 6:
    QtOpenGL = importlib.import_module(f"{QT_LIB}.QtOpenGL")
else:
    QtOpenGL = QtGui


class MarkerType(Enum):
    """Enumeration of supported marker types."""
    POINT = "point"
    CROSS = "cross"
    PLUS = "plus"
    MINUS = "minus"
    PIPE = "pipe"
    ASTERISK = "asterisk"
    CIRCLE = "circle"
    SQUARE = "square"
    DIAMOND = "diamond"
    TRIANGLE_UP = "triangle_up"
    TRIANGLE_DOWN = "triangle_down"
    TRIANGLE_LEFT = "triangle_left"
    TRIANGLE_RIGHT = "triangle_right"
    PENTAGRAM = "pentagram"
    HEXAGRAM = "hexagram"


class GLMarkerItem(GLGraphicsItem.GLGraphicsItem):
    """
    OpenGL item for rendering markers at 3D positions.
    
    Markers are rendered using QPainter on top of the 3D scene, allowing
    for efficient rendering of 2D markers at 3D world positions.
    
    Parameters
    ----------
    **kwds : dict
        Keyword arguments passed to GLGraphicsItem.__init__()
        'glOptions' : str, optional (default='additive')
            GL blending options
    """
    
    def __init__(self, parentItem=None, **kwds):
        super().__init__(parentItem=parentItem)
        glopts = kwds.pop('glOptions', 'translucent')
        self.setGLOptions(glopts)
        
        # List of markers: (position_3d, marker_type, size, stroke_width, stroke_color, fill_color, transparency)
        self.markers: List[dict] = []
        
        # Default marker properties
        self.enable_antialiasing = True
        self.default_size = 10
        self.default_stroke_width = 1.5  # Increased for better antialiasing visibility
        self.default_stroke_color = QtGui.QColor(255, 255, 255, 255)
        self.default_fill_color = QtGui.QColor(255, 255, 255, 255)
        self.default_transparency = 1.0
        self.default_marker_type = MarkerType.CIRCLE

    def compute_projection(self):
        """Compute the projection matrix from 3D world to 2D viewport coordinates."""
        rect = QtCore.QRectF(self.view().rect())
        ndc_to_viewport = QtGui.QMatrix4x4()
        ndc_to_viewport.viewport(rect.left(), rect.bottom(), rect.width(), -rect.height())
        return ndc_to_viewport * self.mvpMatrix()

    def paint(self):
        """Paint method called by OpenGL."""
        self.setupGLState()

        if not (view := self.view()):
            return

        if self.enable_antialiasing:
            self._paint_with_opengl_paintdevice(view)
        else:
            # Direct painting without antialiasing
            painter = QtGui.QPainter(view)
            self.draw(painter)
            painter.end()

    def _paint_with_opengl_paintdevice(self, view):
        """
        Paint using QOpenGLPaintDevice - Qt's standard device for OpenGL painting.
        
        This uses standard Qt functionality to paint directly on the OpenGL context
        with antialiasing enabled, without scaling or blitting.
        """
        # Create OpenGL paint device bound to current context
        device = QtOpenGL.QOpenGLPaintDevice(view.width(), view.height())
        
        # Paint on the OpenGL device
        painter = QtGui.QPainter(device)
        painter.setRenderHints(
            QtGui.QPainter.RenderHint.Antialiasing
            | QtGui.QPainter.RenderHint.SmoothPixmapTransform
        )
        
        self.draw(painter)
        painter.end()

    def draw(self, painter: QtGui.QPainter):
        """
        Draw all markers using the provided QPainter.
        
        Parameters
        ----------
        painter : QtGui.QPainter
            The painter to use for drawing
        """
        project = self.compute_projection()
        
        for marker in self.markers:
            pos_3d = marker['position']
            marker_type = marker['type']
            size = marker['size']
            stroke_width = marker['stroke_width']
            stroke_color = marker['stroke_color']
            fill_color = marker['fill_color']
            transparency = marker['transparency']
            
            # Convert 3D position to 2D viewport position
            vec3 = QtGui.QVector3D(pos_3d[0], pos_3d[1], pos_3d[2])
            pos_2d = project.map(vec3).toPointF()
            
            # Draw the marker
            self._draw_marker(
                painter, pos_2d, marker_type, size,
                stroke_width, stroke_color, fill_color, transparency
            )

    def _draw_marker(
        self,
        painter: QtGui.QPainter,
        pos: QtCore.QPointF,
        marker_type: MarkerType,
        size: float,
        stroke_width: float,
        stroke_color: QtGui.QColor,
        fill_color: QtGui.QColor,
        transparency: float
    ):
        """
        Draw a single marker at the specified 2D position.
        
        Parameters
        ----------
        painter : QtGui.QPainter
            The painter to use
        pos : QtCore.QPointF
            The 2D viewport position to draw at
        marker_type : MarkerType
            The type of marker to draw
        size : float
            The size of the marker
        stroke_width : float
            The stroke width
        stroke_color : QtGui.QColor
            The stroke color
        fill_color : QtGui.QColor
            The fill color
        transparency : float
            The transparency value (0.0-1.0)
        """
        # Apply transparency
        stroke_color.setAlphaF(transparency)
        fill_color.setAlphaF(transparency)
        
        # Set pen and brush with antialiasing-friendly styles
        pen = QtGui.QPen(stroke_color)
        pen.setWidthF(stroke_width) if stroke_width > 0 else pen.setWidth(0)
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(QtCore.Qt.PenJoinStyle.RoundJoin)
        # Set cosmetic pen if very small to ensure antialiasing works
        if stroke_width <= 1.0:
            pen.setCosmetic(True)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(fill_color))
        
        # Draw based on marker type
        if marker_type == MarkerType.POINT:
            self._draw_point(painter, pos, size)
        elif marker_type == MarkerType.CROSS:
            self._draw_cross(painter, pos, size, stroke_width)
        elif marker_type == MarkerType.PLUS:
            self._draw_plus(painter, pos, size, stroke_width)
        elif marker_type == MarkerType.MINUS:
            self._draw_minus(painter, pos, size, stroke_width)
        elif marker_type == MarkerType.PIPE:
            self._draw_pipe(painter, pos, size, stroke_width)
        elif marker_type == MarkerType.ASTERISK:
            self._draw_asterisk(painter, pos, size, stroke_width)
        elif marker_type == MarkerType.CIRCLE:
            self._draw_circle(painter, pos, size)
        elif marker_type == MarkerType.SQUARE:
            self._draw_square(painter, pos, size)
        elif marker_type == MarkerType.DIAMOND:
            self._draw_diamond(painter, pos, size)
        elif marker_type == MarkerType.TRIANGLE_UP:
            self._draw_triangle(painter, pos, size, 0)
        elif marker_type == MarkerType.TRIANGLE_DOWN:
            self._draw_triangle(painter, pos, size, 180)
        elif marker_type == MarkerType.TRIANGLE_LEFT:
            self._draw_triangle(painter, pos, size, 90)
        elif marker_type == MarkerType.TRIANGLE_RIGHT:
            self._draw_triangle(painter, pos, size, -90)
        elif marker_type == MarkerType.PENTAGRAM:
            self._draw_pentagram(painter, pos, size)
        elif marker_type == MarkerType.HEXAGRAM:
            self._draw_hexagram(painter, pos, size)

    @staticmethod
    def _draw_point(painter: QtGui.QPainter, pos: QtCore.QPointF, size: float):
        """Draw a point marker."""
        painter.drawPoint(pos)

    @staticmethod
    def _draw_cross(painter: QtGui.QPainter, pos: QtCore.QPointF, size: float, stroke_width: float):
        """Draw a cross marker (diagonal lines)."""
        half = size / 2
        painter.drawLine(
            QtCore.QPointF(pos.x() - half, pos.y() - half),
            QtCore.QPointF(pos.x() + half, pos.y() + half)
        )
        painter.drawLine(
            QtCore.QPointF(pos.x() - half, pos.y() + half),
            QtCore.QPointF(pos.x() + half, pos.y() - half)
        )

    @staticmethod
    def _draw_plus(painter: QtGui.QPainter, pos: QtCore.QPointF, size: float, stroke_width: float):
        """Draw a plus marker (horizontal and vertical lines)."""
        half = size / 2
        painter.drawLine(
            QtCore.QPointF(pos.x() - half, pos.y()),
            QtCore.QPointF(pos.x() + half, pos.y())
        )
        painter.drawLine(
            QtCore.QPointF(pos.x(), pos.y() - half),
            QtCore.QPointF(pos.x(), pos.y() + half)
        )

    @staticmethod
    def _draw_minus(painter: QtGui.QPainter, pos: QtCore.QPointF, size: float, stroke_width: float):
        """Draw a minus marker (horizontal line)."""
        half = size / 2
        painter.drawLine(
            QtCore.QPointF(pos.x() - half, pos.y()),
            QtCore.QPointF(pos.x() + half, pos.y())
        )

    @staticmethod
    def _draw_pipe(painter: QtGui.QPainter, pos: QtCore.QPointF, size: float, stroke_width: float):
        """Draw a pipe marker (vertical line)."""
        half = size / 2
        painter.drawLine(
            QtCore.QPointF(pos.x(), pos.y() - half),
            QtCore.QPointF(pos.x(), pos.y() + half)
        )

    @staticmethod
    def _draw_asterisk(painter: QtGui.QPainter, pos: QtCore.QPointF, size: float, stroke_width: float):
        """Draw an asterisk marker (six lines at 60 degree angles)."""
        half = size / 2
        angles = [0, 60, 120, 180, 240, 300]
        for angle in angles:
            rad = math.radians(angle)
            x1 = pos.x() + half * math.cos(rad)
            y1 = pos.y() + half * math.sin(rad)
            x2 = pos.x() - half * math.cos(rad)
            y2 = pos.y() - half * math.sin(rad)
            painter.drawLine(QtCore.QPointF(x1, y1), QtCore.QPointF(x2, y2))

    @staticmethod
    def _draw_circle(painter: QtGui.QPainter, pos: QtCore.QPointF, size: float):
        """Draw a circle marker."""
        painter.drawEllipse(pos, size / 2, size / 2)

    @staticmethod
    def _draw_square(painter: QtGui.QPainter, pos: QtCore.QPointF, size: float):
        """Draw a square marker."""
        half = size / 2
        rect = QtCore.QRectF(pos.x() - half, pos.y() - half, size, size)
        painter.drawRect(rect)

    @staticmethod
    def _draw_diamond(painter: QtGui.QPainter, pos: QtCore.QPointF, size: float):
        """Draw a diamond marker (like a playing card diamond, elongated vertically)."""
        half_w = size / 2.5  # Make it narrower
        half_h = size / 2    # Make it taller
        points = [
            QtCore.QPointF(pos.x(), pos.y() - half_h),      # Top
            QtCore.QPointF(pos.x() + half_w, pos.y()),      # Right
            QtCore.QPointF(pos.x(), pos.y() + half_h),      # Bottom
            QtCore.QPointF(pos.x() - half_w, pos.y())       # Left
        ]
        painter.drawPolygon(QtGui.QPolygonF(points))

    @staticmethod
    def _draw_triangle(painter: QtGui.QPainter, pos: QtCore.QPointF, size: float, rotation: float = 0):
        """Draw a triangle marker pointing in the specified direction."""
        half = size / 2
        height = size * math.sqrt(3) / 2
        
        # Define triangle points (pointing up initially)
        points = [
            QtCore.QPointF(0, -height / 2),
            QtCore.QPointF(-half, height / 2),
            QtCore.QPointF(half, height / 2)
        ]
        
        # Rotate points
        rad = math.radians(rotation)
        cos_r = math.cos(rad)
        sin_r = math.sin(rad)
        rotated = []
        for p in points:
            x = p.x() * cos_r - p.y() * sin_r
            y = p.x() * sin_r + p.y() * cos_r
            rotated.append(QtCore.QPointF(pos.x() + x, pos.y() + y))
        
        painter.drawPolygon(QtGui.QPolygonF(rotated))

    @staticmethod
    def _draw_pentagram(painter: QtGui.QPainter, pos: QtCore.QPointF, size: float):
        """Draw a pentagram (5-pointed star) marker."""
        points = []
        for i in range(10):
            angle = i * 36 - 90  # Start at top
            rad = math.radians(angle)
            # Alternate between outer and inner radius
            radius = size / 2 if i % 2 == 0 else size / 4
            x = pos.x() + radius * math.cos(rad)
            y = pos.y() + radius * math.sin(rad)
            points.append(QtCore.QPointF(x, y))
        
        painter.drawPolygon(QtGui.QPolygonF(points))

    @staticmethod
    def _draw_hexagram(painter: QtGui.QPainter, pos: QtCore.QPointF, size: float):
        """Draw a hexagram (6-pointed star / Star of David) marker."""
        points = []
        for i in range(12):
            angle = i * 30 - 90  # Start at top
            rad = math.radians(angle)
            # Alternate between outer and inner radius
            radius = size / 2 if i % 2 == 0 else size / 3
            x = pos.x() + radius * math.cos(rad)
            y = pos.y() + radius * math.sin(rad)
            points.append(QtCore.QPointF(x, y))
        
        painter.drawPolygon(QtGui.QPolygonF(points))

    # Public API methods for adding and managing markers

    def add_marker(
        self,
        position: Tuple[float, float, float],
        marker_type: MarkerType = None,
        size: float = None,
        stroke_width: float = None,
        stroke_color: QtGui.QColor = None,
        fill_color: QtGui.QColor = None,
        transparency: float = None
    ) -> int:
        """
        Add a marker at the specified 3D position.
        
        Parameters
        ----------
        position : tuple of float
            3D position (x, y, z)
        marker_type : MarkerType, optional
            Type of marker (uses default if not specified)
        size : float, optional
            Size of marker (uses default if not specified)
        stroke_width : float, optional
            Stroke width (uses default if not specified)
        stroke_color : QtGui.QColor, optional
            Stroke color (uses default if not specified)
        fill_color : QtGui.QColor, optional
            Fill color (uses default if not specified)
        transparency : float, optional
            Transparency 0.0-1.0 (uses default if not specified)
        
        Returns
        -------
        int
            Index of the added marker
        """
        marker = {
            'position': position,
            'type': marker_type or self.default_marker_type,
            'size': size if size is not None else self.default_size,
            'stroke_width': stroke_width if stroke_width is not None else self.default_stroke_width,
            'stroke_color': stroke_color or QtGui.QColor(self.default_stroke_color),
            'fill_color': fill_color or QtGui.QColor(self.default_fill_color),
            'transparency': transparency if transparency is not None else self.default_transparency
        }
        self.markers.append(marker)
        self.update()
        return len(self.markers) - 1

    def remove_marker(self, index: int):
        """Remove a marker by index."""
        if 0 <= index < len(self.markers):
            self.markers.pop(index)
            self.update()

    def clear_markers(self):
        """Clear all markers."""
        self.markers.clear()
        self.update()

    def update_marker(
        self,
        index: int,
        position: Tuple[float, float, float] = None,
        marker_type: MarkerType = None,
        size: float = None,
        stroke_width: float = None,
        stroke_color: QtGui.QColor = None,
        fill_color: QtGui.QColor = None,
        transparency: float = None
    ):
        """Update properties of an existing marker."""
        if 0 <= index < len(self.markers):
            marker = self.markers[index]
            if position is not None:
                marker['position'] = position
            if marker_type is not None:
                marker['type'] = marker_type
            if size is not None:
                marker['size'] = size
            if stroke_width is not None:
                marker['stroke_width'] = stroke_width
            if stroke_color is not None:
                marker['stroke_color'] = QtGui.QColor(stroke_color)
            if fill_color is not None:
                marker['fill_color'] = QtGui.QColor(fill_color)
            if transparency is not None:
                marker['transparency'] = transparency
            self.update()

    def set_default_properties(
        self,
        marker_type: MarkerType = None,
        size: float = None,
        stroke_width: float = None,
        stroke_color: QtGui.QColor = None,
        fill_color: QtGui.QColor = None,
        transparency: float = None
    ):
        """Set default properties for newly added markers."""
        if marker_type is not None:
            self.default_marker_type = marker_type
        if size is not None:
            self.default_size = size
        if stroke_width is not None:
            self.default_stroke_width = stroke_width
        if stroke_color is not None:
            self.default_stroke_color = QtGui.QColor(stroke_color)
        if fill_color is not None:
            self.default_fill_color = QtGui.QColor(fill_color)
        if transparency is not None:
            self.default_transparency = transparency

    def get_marker_count(self) -> int:
        """Get the number of markers."""
        return len(self.markers)

    def get_marker(self, index: int) -> Optional[dict]:
        """Get marker data by index."""
        if 0 <= index < len(self.markers):
            return self.markers[index].copy()
        return None
