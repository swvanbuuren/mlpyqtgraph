# GLMarkerItem Documentation

## Overview

`GLMarkerItem` is an OpenGL item for rendering various types of markers on 3D GL scenes. It uses QPainter to efficiently draw 2D markers at 3D world positions, following the same pattern as the PyQtGraph `GLPainterItem` example.

## Features

- **14 Marker Types**: point, cross, plus, minus, pipe, asterisk, circle, square, triangle (4 directions), pentagram, hexagram
- **Fully Configurable**: Control size, stroke width, stroke color, fill color, and transparency for each marker
- **Efficient Rendering**: All markers are drawn in a single pass using QPainter
- **Easy API**: Simple methods to add, remove, and update markers

## Supported Marker Types

The `MarkerType` enum includes:

| Type | Description |
|------|-------------|
| `POINT` | Single pixel point |
| `CROSS` | Diagonal crossing lines (X) |
| `PLUS` | Horizontal and vertical lines (+) |
| `MINUS` | Horizontal line only |
| `PIPE` | Vertical line only |
| `ASTERISK` | Six lines at 60° angles |
| `CIRCLE` | Filled/unfilled circle |
| `SQUARE` | Filled/unfilled square |
| `TRIANGLE_UP` | Triangle pointing upward |
| `TRIANGLE_DOWN` | Triangle pointing downward |
| `TRIANGLE_LEFT` | Triangle pointing left |
| `TRIANGLE_RIGHT` | Triangle pointing right |
| `PENTAGRAM` | Five-pointed star |
| `HEXAGRAM` | Six-pointed star (Star of David) |

## Installation

The `GLMarkerItem` class is located in the `mlpyqtgraph.utils` module:

```python
from mlpyqtgraph.utils import GLMarkerItem, MarkerType
```

## Usage

### Basic Usage

```python
import pyqtgraph as pg
from pyqtgraph.opengl import GLViewWidget, GLGridItem, GLAxisItem
from pyqtgraph.Qt import QtGui
from mlpyqtgraph.utils import GLMarkerItem, MarkerType

# Create application and 3D view
pg.mkQApp()
glv = GLViewWidget()
glv.show()

# Add grid and axis items (optional)
griditem = GLGridItem()
glv.addItem(griditem)

axisitem = GLAxisItem()
glv.addItem(axisitem)

# Create and add marker item
markers = GLMarkerItem()
glv.addItem(markers)

# Add a red circle marker at position (0, 0, 0)
markers.add_marker(
    position=(0, 0, 0),
    marker_type=MarkerType.CIRCLE,
    size=10,
    stroke_width=1,
    stroke_color=QtGui.QColor(255, 0, 0),
    fill_color=QtGui.QColor(255, 100, 100),
    transparency=1.0
)

pg.exec()
```

### Setting Default Properties

```python
# Set default properties for all subsequently added markers
markers.set_default_properties(
    marker_type=MarkerType.SQUARE,
    size=8,
    stroke_width=0.5,
    stroke_color=QtGui.QColor(0, 255, 0),
    fill_color=QtGui.QColor(100, 255, 100),
    transparency=0.8
)

# These markers will use the default properties set above
markers.add_marker((1, 1, 0))
markers.add_marker((2, 2, 0))
```

### Managing Markers

```python
# Add a marker and get its index
idx = markers.add_marker((3, 3, 3), marker_type=MarkerType.TRIANGLE_UP)

# Update a marker's properties
markers.update_marker(
    idx,
    size=12,
    stroke_width=2,
    stroke_color=QtGui.QColor(255, 255, 0)
)

# Remove a specific marker
markers.remove_marker(idx)

# Clear all markers
markers.clear_markers()

# Get marker count
count = markers.get_marker_count()

# Get marker data (returns a copy)
marker_data = markers.get_marker(idx)
```

## API Reference

### Constructor

```python
GLMarkerItem(**kwds)
```

**Parameters:**
- `glOptions` (str, optional): GL blending options (default: 'additive')

### Methods

#### add_marker(position, marker_type=None, size=None, stroke_width=None, stroke_color=None, fill_color=None, transparency=None) → int

Add a marker at the specified 3D position.

**Parameters:**
- `position` (tuple): 3D position (x, y, z)
- `marker_type` (MarkerType): Type of marker (uses default if not specified)
- `size` (float): Size of marker in viewport pixels
- `stroke_width` (float): Stroke width
- `stroke_color` (QtGui.QColor): Color for the stroke
- `fill_color` (QtGui.QColor): Color for filling
- `transparency` (float): Transparency value 0.0-1.0

**Returns:** Index of the added marker

#### remove_marker(index)

Remove a marker by its index.

#### clear_markers()

Remove all markers.

#### update_marker(index, position=None, marker_type=None, size=None, stroke_width=None, stroke_color=None, fill_color=None, transparency=None)

Update properties of an existing marker.

#### set_default_properties(marker_type=None, size=None, stroke_width=None, stroke_color=None, fill_color=None, transparency=None)

Set default properties for newly added markers.

#### get_marker_count() → int

Get the total number of markers.

#### get_marker(index) → dict or None

Get a copy of marker data at the specified index. Returns None if index is out of range.

### Properties

- `default_marker_type` (MarkerType): Default marker type for new markers
- `default_size` (float): Default size for new markers
- `default_stroke_width` (float): Default stroke width
- `default_stroke_color` (QtGui.QColor): Default stroke color
- `default_fill_color` (QtGui.QColor): Default fill color
- `default_transparency` (float): Default transparency value

## Example: Plotting Multiple Marker Types

See `examples/marker_items.py` for a complete example that displays all marker types with different colors and configurations.

## Implementation Details

The `GLMarkerItem` class extends `GLGraphicsItem.GLGraphicsItem` and uses the following key techniques:

- `compute_projection()`: Converts 3D world coordinates to 2D viewport coordinates
- `paint()`: Called by OpenGL to render the item; immediately sets antialiasing render hints on the QPainter
- `draw()`: Draws all markers in a single pass using the provided QPainter
- **Path-based rendering**: Uses `QPainterPath` with `strokePath()` for lines and `fillPath()` for shapes, providing superior antialiasing quality compared to raw drawing primitives

### Why Path-based Rendering?

QPainter's `strokePath()` method applies antialiasing to stroked paths much more effectively than direct `drawLine()`, `drawEllipse()`, or `drawPolygon()` calls. This is because:
- `strokePath()` vectorizes the outline computation, allowing for sub-pixel accuracy
- The pen's cap and join styles work correctly with the antialiasing pipeline
- Avoids limitations of direct GL rendering on certain platforms/engines

Each marker type has a corresponding `_draw_*` method that:
1. Creates a `QPainterPath` with the appropriate shape
2. Fills the path if the brush is not `NoBrush`  
3. Strokes the path if the pen is not `NoPen`

## Performance Considerations

- All markers are rendered in a single pass, making this efficient for displaying multiple markers
- Markers are rendered as 2D overlays, so they maintain the same screen size regardless of camera distance
- Use `transparency` < 1.0 for blended rendering
- For very large numbers of markers (1000+), consider batching operations

## Antialiasing

Antialiasing is automatically enabled through:
1. **QPainter Render Hints**: `Antialiasing` and `SmoothPixmapTransform` are set on the painter in the `paint()` method
2. **Path-based Rendering**: All marker shapes use `QPainterPath` with `strokePath()` and `fillPath()` methods for superior antialiasing quality
3. **Pen Cap/Join Styles**: Round caps and joins are configured on the pen to ensure smooth visual appearance

### Technical Details

- Antialiasing works within OpenGL contexts through Qt's QPainter abstraction
- Direct drawing methods (`drawLine()`, `drawEllipse()`, etc.) have limited antialiasing quality in GL contexts
- Using `strokePath()` and `fillPath()` vectorizes the rendering pipeline and provides sub-pixel accuracy for smooth edges
- Round cap styles (`RoundCap`) and join styles (`RoundJoin`) ensure clean line endings and corner transitions

## Notes

- Markers are rendered on top of 3D content due to the nature of QPainter rendering
- Stroke width and size are specified in viewport pixels
- Colors can be specified using `QtGui.QColor(r, g, b, a)` with optional alpha channel
- Transparency values should be 0.0 (fully transparent) to 1.0 (fully opaque)
