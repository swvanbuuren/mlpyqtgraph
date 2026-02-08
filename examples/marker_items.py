"""
Example demonstrating GLMarkerItem for rendering various markers on a 3D GL scene,
with a GLSurfacePlotItem surface background.
"""

import numpy as np
import pyqtgraph as pg
from pyqtgraph.opengl import GLAxisItem, GLGridItem, GLViewWidget
from pyqtgraph.Qt import QtCore, QtGui

from mlpyqtgraph.utils.GLMarkerItem import GLMarkerItem, MarkerType
from mlpyqtgraph.utils.GLSurfacePlotItem import GLSurfacePlotItem


def main():
    """Create a 3D scene with various marker types."""
    # Create application and view
    pg.mkQApp("GLMarkerItem Example")
    pg.setConfigOption('background', 'k')  # Set black background
    pg.setConfigOption('foreground', 'w')  # Set white foreground for better visibility
    
    # Configure surface format for MSAA (hardware antialiasing)
    fmt = QtGui.QSurfaceFormat()
    fmt.setSamples(4)  # Request 4x MSAA
    fmt.setVersion(3, 3)  # Use OpenGL 3.3
    fmt.setProfile(QtGui.QSurfaceFormat.CoreProfile)
    QtGui.QSurfaceFormat.setDefaultFormat(fmt)
    
    glv = GLViewWidget()
    glv.show()
    glv.setWindowTitle('GLMarkerItem Example - Various Marker Types')
    glv.setCameraPosition(distance=50, elevation=45, azimuth=45)

    # Add grid and axis items
    griditem = GLGridItem()
    griditem.setSize(40, 40)
    griditem.setSpacing(5, 5)
    glv.addItem(griditem)

    axisitem = GLAxisItem()
    axisitem.setSize(20, 20, 20)
    glv.addItem(axisitem)

    # Create surface plot background
    x = np.linspace(-20, 20, 50)
    y = np.linspace(-20, 20, 50)
    xx, yy = np.meshgrid(x, y)
    # Create a simple wavy surface
    zz = 5 * np.sin(np.sqrt(xx**2 + yy**2) / 5)
    
    # Create surface colors (grayscale based on z value)
    colors = np.zeros((*zz.shape, 4))
    colors[:, :, 0] = (zz - zz.min()) / (zz.max() - zz.min()) * 0.7  # Red channel
    colors[:, :, 1] = (zz - zz.min()) / (zz.max() - zz.min()) * 0.7  # Green channel
    colors[:, :, 2] = (zz - zz.min()) / (zz.max() - zz.min()) * 0.9  # Blue channel
    colors[:, :, 3] = 1.0  # Alpha (fully opaque)
    
    surface = GLSurfacePlotItem(x=xx, y=yy, z=zz, colors=colors, shader='normalColor', smooth=True,
                                showGrid=True, lineColor=(0.5, 0.5, 0.5, 1.0), lineWidth=0.5)
    glv.addItem(surface)

    # Create marker item
    markers = GLMarkerItem()
    glv.addItem(markers)

    # Define marker types and their display positions
    marker_types = [
        (MarkerType.POINT, "POINT", -15, 20),
        (MarkerType.CROSS, "CROSS", -5, 20),
        (MarkerType.PLUS, "PLUS", 5, 20),
        (MarkerType.MINUS, "MINUS", 15, 20),
        
        (MarkerType.PIPE, "PIPE", -15, 10),
        (MarkerType.ASTERISK, "ASTERISK", -5, 10),
        (MarkerType.CIRCLE, "CIRCLE", 5, 10),
        (MarkerType.SQUARE, "SQUARE", 15, 10),
        
        (MarkerType.TRIANGLE_UP, "TRIANGLE_UP", -15, 0),
        (MarkerType.TRIANGLE_DOWN, "TRIANGLE_DOWN", -5, 0),
        (MarkerType.TRIANGLE_LEFT, "TRIANGLE_LEFT", 5, 0),
        (MarkerType.TRIANGLE_RIGHT, "TRIANGLE_RIGHT", 15, 0),
        
        (MarkerType.DIAMOND, "DIAMOND", -15, -10),
        (MarkerType.PENTAGRAM, "PENTAGRAM", -5, -10),
        (MarkerType.HEXAGRAM, "HEXAGRAM", 5, -10),
    ]

    # Add markers with different configurations
    for marker_type, name, x, y in marker_types:
        # Set default properties for this marker
        markers.set_default_properties(
            marker_type=marker_type,
            size=8,
            stroke_width=1.5,
            stroke_color=QtGui.QColor(255, 255, 255, 255),
            fill_color=QtGui.QColor(100, 150, 255, 255),
            transparency=1.0
        )
        # Add the marker
        markers.add_marker((x, y, 0))

    # Add some additional markers with different colors
    # Red markers in a diagonal
    markers.set_default_properties(
        marker_type=MarkerType.CIRCLE,
        size=6,
        stroke_width=1.0,
        stroke_color=QtGui.QColor(255, 0, 0),
        fill_color=QtGui.QColor(255, 100, 100)
    )
    for i in range(-2, 3):
        markers.add_marker((i * 3, i * 3, i))

    # Green markers
    markers.set_default_properties(
        marker_type=MarkerType.SQUARE,
        size=6,
        stroke_color=QtGui.QColor(0, 255, 0),
        fill_color=QtGui.QColor(100, 255, 100)
    )
    for i in range(-2, 3):
        markers.add_marker((-i * 3, i * 3, -i))

    if __name__ == '__main__':
        pg.exec()


if __name__ == '__main__':
    main()
