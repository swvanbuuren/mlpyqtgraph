""" mlpyqtgraph axes module, with 2D and 3D Axis classes """


import math
from dataclasses import dataclass
from typing import List
from pyqtgraph import PlotItem, ColorMap, colormap, QtCore, Point, mkBrush, mkPen
from pyqtgraph.opengl import GLSurfacePlotItem, GLLinePlotItem, GLViewWidget
from pyqtgraph.opengl.GLGraphicsItem import GLGraphicsItem
import pyqtgraph.functions as fn
import numpy as np

from mlpyqtgraph.config import options
from mlpyqtgraph import colors
from mlpyqtgraph.grid_axes import GLGridAxis
from mlpyqtgraph.utils.ticklabels import coord_generator, limit_generator, coord_transformers


class RootException(Exception):
    """ Root Exception of the windows module """


class InvalidAxis(RootException):
    """ Exception raised for invalid axes """


class Axis2D(PlotItem):  # noqa: PLR0904
    """ Axis for plots in a given figure layout """
    pen_styles = {'-': QtCore.Qt.SolidLine,
                  '--': QtCore.Qt.DashLine,
                  ':': QtCore.Qt.DotLine,
                  '.-': QtCore.Qt.DashDotLine}

    def __init__(self, index, **kwargs):
        parent = kwargs.pop('parent', None)
        super().__init__(parent=parent, **kwargs)
        self.index = index
        self.colors_defs = colors.ColorDefinitions()
        self.line_colors = self.colors_defs.get_line_colors()
        self.scale_box_line_color = \
            self.colors_defs.get_scale_box_colors(part='line')
        self.scale_box_fill_color = \
            self.colors_defs.get_scale_box_colors(part='fill')
        self.setup()

    def setup(self, padding=0.01):
        """ Setup axes and grid """
        self.show_axis_border('right')
        self.show_axis_border('top')
        self.getViewBox().setDefaultPadding(padding=padding)
        self.getViewBox().rbScaleBox.setPen(fn.mkPen(self.scale_box_line_color, width=2))
        self.getViewBox().rbScaleBox.setBrush(fn.mkBrush(*self.scale_box_fill_color))
        for axis_key in self.axes:
            self.getAxis(axis_key).setZValue(-1) # force axis and corresponding ticks to background

    @property
    def x_axis(self):
        """ Returns the x-axis """
        return self.getAxis('bottom')

    @property
    def y_axis(self):
        """ Returns the y-axis """
        return self.getAxis('left')

    def show_axis_border(self, axis):
        """ Enables/shows an axis, wihtout values and ticks

        Parameters:
            axis: axis string designation, 'left', 'top', 'right' or 'bottom'
        """
        self.showAxis(axis, show=True)
        self.getAxis(axis).setStyle(showValues=False)
        self.getAxis(axis).setTicks([(),()])

    def get_line_color(self, index=None):
        """ Generate line color for given index """
        return self.line_colors[index % len(self.line_colors)]

    def default_line_color(self):
        """ Returns next available color, based on the number of plotted lines """
        return self.get_line_color(len(self.listDataItems()))

    @staticmethod
    def fix_line_artifacts(width, color):
        """
        Fall to conventional slower drawing method by settings alpha < 1

        pyqtgraph pull request #2011 introduced a new (experimental) line
        drawing mode for thick lines. This also leads to unwanted line artifacts
        if antialiasing is enabled. This method causes a fallback to the old
        (slower) drawing method.
        """
        if width > 1:
            if color in fn.Colors:
                qcolor = fn.Colors[color]
                color = (qcolor.red(), qcolor.green(), qcolor.blue())
            return color[:3] + (254,)
        return color

    def add(self, x_coord: np.ndarray, y_coord: np.ndarray, **kwargs):
        """Add a line to the Axes

        Arguments:
            x_coord:
                x coordinates
            y_coord:
                y coordinates

        Keyword arguments:
            color:
                line color, default value will determine using
                [`default_line_color`](./#mlpyqtgraph.axes.Axis2D.default_line_color)
            style:
                line style
            width:
                line width
            symbol:
                symbol type symbol_size: symbol size
            symbol_color:
                symbol color

        """
        color = kwargs.get('color', self.default_line_color())
        width = kwargs.get('width', 2.0)
        if options.get_option('no_segmented_line_mode'):
            color = self.fix_line_artifacts(width, color)
        style = kwargs.get('style', '-')
        symbol = kwargs.get('symbol')
        symbol_size = kwargs.get('symbol_size', 5)
        symbol_color = kwargs.get('symbol_color', 'k')

        line_pen = None
        if width > 0:
            line_pen = mkPen(color, width=width)
            if style:
                line_pen.setStyle(self.pen_styles[style])

        symbol_pen = None
        if symbol is not None:
            symbol_pen = mkPen(symbol_color, width=0)

        self.plot(x_coord, y_coord,
                  pen=line_pen, symbol=symbol, symbolSize=symbol_size,
                  symbolPen=symbol_pen, symbolBrush=symbol_color)

    @property
    def grid(self):
        """ Returns grid activation state """
        return self.ctrl.xGridCheck.isChecked() and self.ctrl.yGridCheck.isChecked()

    @grid.setter
    def grid(self, active=False):
        """ Set gris activation """
        self.showGrid(x=active, y=active, alpha=0.5)

    @property
    def xlim(self):
        """ Obtain xlimits """
        return self.x_axis.range

    @xlim.setter
    def xlim(self, limits):
        """ Change x limits """
        self.setLimits(xMin=limits[0], xMax=limits[1])
        self.setRange(xRange=limits)

    @property
    def ylim(self):
        """ Obtain ylimits """
        return self.y_axis.range

    @ylim.setter
    def ylim(self, limits):
        """ Change y limits """
        self.setLimits(yMin=limits[0], yMax=limits[1])
        self.setRange(yRange=limits)

    @property
    def xlabel(self):
        """ Obtain xlabel """
        return self.x_axis.label.toPlainText()

    @xlabel.setter
    def xlabel(self, label, units=None):
        """ Change x label """
        self.x_axis.setLabel(label, units=units)

    @property
    def ylabel(self):
        """ Obtain ylabel """
        return self.y_axis.label.toPlainText()

    @ylabel.setter
    def ylabel(self, label, units=None):
        """ Change y label """
        self.y_axis.setLabel(label, units=units)

    @property
    def xticks(self):
        """ Obtain x tick labels """
        return self.get_ticks(self.x_axis)

    @xticks.setter
    def xticks(self, major):
        """ Change x tick labels """
        self.set_xticks(major)

    @property
    def yticks(self):
        """ Obtain y tick labels """
        return self.get_ticks(self.y_axis)

    @yticks.setter
    def yticks(self, major):
        """ Sets major tick labels on y-axis  """
        self.set_yticks(major)

    def set_xticks(self, major, minor=None):
        """ Sets the major and minor ticks on the x-axis """
        self.set_ticks(self.x_axis, major, minor)

    def set_yticks(self, major, minor=None):
        """ Sets the major and minor ticks on the y-axis """
        self.set_ticks(self.y_axis, major, minor)

    @staticmethod
    def set_ticks(axis, major, minor=None):
        """ Sets the major and minor ticks on a given axis """
        if minor is None:
            minor = ()
        axis.setTicks([major, minor])

    def add_legend(self, *legend_labels, offset=(1,1)):
        """ Add legend labels """
        legend_brush = mkBrush(color=(255, 255, 255, 200))
        self.addLegend(brush=legend_brush, verSpacing=-5, offset=offset)
        plot_items = self.listDataItems()
        for label, item in zip(legend_labels, plot_items):
            self.legend.addItem(item, label)

    def get_axis_span(self, axis):
        """ Determine span of this axis """
        bounds = axis.mapRectFromParent(axis.geometry())
        if axis.orientation == 'left':
            return (bounds.topRight(), bounds.bottomRight())
        if axis.orientation == 'right':
            return (bounds.topLeft(), bounds.bottomLeft())
        if axis.orientation == 'top':
            return (bounds.bottomLeft(), bounds.bottomRight())
        if axis.orientation == 'bottom':
            return (bounds.topLeft(), bounds.topRight())
        return None

    def get_axis_size(self, axis):
        """ Determine size of this axis in pixels """
        axis_span = self.get_axis_span(axis)
        if axis_span is None:
            return None
        points = list(map(self.mapToDevice, axis_span))
        if None in points:
            return None
        length_px = Point(points[1] - points[0]).length()
        if length_px == 0:
            return None
        return length_px

    def get_ticks(self, axis):
        """ Obtain the tick values for a given axis """
        if axis._tickLevels is not None:
            return axis._tickLevels  # return manually set ticks
        length_px = self.get_axis_size(axis)
        if length_px is None:
            return []
        tick_values = axis.tickValues(axis.range[0], axis.range[1], length_px)
        ticks = list()
        for (_, values) in tick_values:
            ticks.extend(values)
        return sorted(ticks)

    def delete(self):
        """ Closes the axis """

@dataclass
class Axis3DItem:
    instance: GLSurfacePlotItem | GLLinePlotItem
    data: tuple
    options: dict


class ViewNotDefinedError(Exception):
    """ Raised if view is not defined yet """


class InvalidTicks(Exception):
    """ Raised for invalid no. of ticks entries """


class Axis3D(GLGraphicsItem):
    """ 3D axis """

    aspect_ratios = {
        'auto': (1.0, 1.0, 0.8),
        'flat': (1.0, 1.0, 0.6),
        'cube': (1.0, 1.0, 1.0),
    }

    def __init__(self, index, parentItem=None, **kwargs):
        super().__init__(parentItem=parentItem)
        antialiasing = options.get_option('antialiasing')
        self.index = index
        self.grid_axes = GLGridAxis(parentItem=self, line_antialias=antialiasing)
        self.default_surface_options = {
            'color': (0, 0, 0, 1),
            'showGrid': True,
            'lineAntialias': antialiasing,
            'colormap': options.get_option('colormap'),
        }
        self.default_line_options = {
            'color': (0, 0, 0, 1),
            'antialias': antialiasing,
            'width': 1,
        }
        self._items: List[Axis3DItem] = []
        self._aspect_ratio = 'auto'
        self._projection_method = options.get_option('projection')
        self._label_fmt = '.1f'
        self._lim = { c: [] for c in 'xyz' }
        self._max_no_ticks = { c: 6 for c in 'xyz' }

    def surf(self, *args, **kwargs):
        """ Adds a 3D surface plot item to the view widget  """
        kwargs = dict(self.default_surface_options, **kwargs)
        surface = GLSurfacePlotItem(**kwargs)
        self._add_item(surface, *args, **kwargs)
        self.update()

    def line(self, *args, **kwargs):
        """ Plots a single grid line for given coordinates """
        kwargs = dict(self.default_line_options, **kwargs)
        line = GLLinePlotItem(**kwargs)
        self._add_item(line, *args, **kwargs)
        self.update()

    def update(self):
        for item in self._items:
            plot_item = item.instance
            coord_kwargs = dict(zip('xyz', item.data))
            coords, coords_labels, limits = self._transform_coordinates(coord_kwargs)
            if isinstance(plot_item, GLSurfacePlotItem):
                plot_item.setData(**coord_kwargs)
                if colormap := item.options.get('colormap'):
                    self._set_colormap(plot_item, colormap_type=colormap)
            elif isinstance(plot_item, GLLinePlotItem):
                points = np.column_stack(list(coord_kwargs.values()))
                plot_item.setData(pos=points)
            self._set_projection_method(*coord_kwargs.values())
            self.grid_axes.setData(coords=coords, coords_labels=coords_labels, limits=limits)
            self._get_view().setCameraPosition(**self.grid_axes.best_camera(method=self._projection_method))
        super().update()

    def _get_view(self) -> GLViewWidget:
        if view := self.view():
            return view
        raise ViewNotDefinedError('Axis3D doesn\'t have a view!')

    def _add_item(self, item: GLSurfacePlotItem | GLLinePlotItem, *data, **options):
        self._items.append(Axis3DItem(item, data, options))
        self._get_view().addItem(item)

    def _aspect_coords(self):
        """ Returns the aspect ratio coordinates """
        if self._aspect_ratio == 'equal':
            return False
        elif isinstance(self._aspect_ratio, str):
            ratios = self.aspect_ratios.get(self._aspect_ratio, (1.0, 1.0, 0.8))
        elif isinstance(self._aspect_ratio, tuple | list):
            ratios = self.aspect_ratio
        else:
            raise ValueError()
        return {label: (0.0, ratio) for label, ratio in zip('xyz', ratios)}

    def _transform_coordinates(self, coord_kwargs):
        """ Transforms the given coordinates according to fixed coords """
        coords_labels = dict(coord_generator(coord_kwargs, max_no_ticks=self._max_no_ticks, limits=self._lim))
        if aspect_coords := self._aspect_coords():
            coords = {}
            for key, transformer in coord_transformers(coords_labels, aspect_coords):
                coord_kwargs[key] = transformer(coord_kwargs[key])
                coords[key] = transformer(coords_labels[key])
        else:
            coords = coords_labels
        limits = dict(limit_generator(limit_ratio=0.05, **coords))
        coords_str_labels = dict(self._gen_str_labels(coords_labels))
        return coords, coords_str_labels, limits

    def _gen_str_labels(self, coords):
        for key, value in coords.items():
            yield key, [f'{x:{self._label_fmt}}' for x in value]

    @staticmethod
    def _set_colormap(surface, colormap_type='CET-L10'):
        """ Assign colormap to surface using surface height """
        heights = surface._z
        normalized_heights = (heights - heights.min())/np.ptp(heights)
        if current_colormap := colormap.get(colormap_type):
            colors = current_colormap.map(normalized_heights, mode=ColorMap.FLOAT)
            surface._meshdata.setFaceColors(colors)

    def _set_projection_method(self, *coords):
        """ Sets the projection method, either perspective or orthographic """
        object_size = (sum([np.ptp(coord)**3.0 for coord in coords]))**(1.0/3.0)
        field_of_view = 60
        if self._projection_method == 'orthographic':
            field_of_view = 1
        distance = 0.75*object_size/math.tan(0.5*field_of_view/180.0*math.pi)
        self._get_view().setCameraParams(fov=field_of_view, distance=distance)

    @property
    def azimuth(self):
        """ Azimuth view angle """
        return self._get_view().cameraParams()['azimuth']

    @azimuth.setter
    def azimuth(self, value):
        self._get_view().setCameraParams(azimuth=value)

    @property
    def elevation(self):
        """ Elevation view angle """
        return self._get_view().cameraParams()['elevation']

    @elevation.setter
    def elevation(self, value):
        self._get_view().setCameraParams(elevation=value)

    @property
    def aspect_ratio(self):
        """ Axes and data scaling aspect ratio
        
        Either a string or a tuple/list.

        - `'auto'`: `(1.0, 1.0, 0.8)`
        - `'flat'`: `(1.0, 1.0, 0.6)`
        - `'cube'`: `(1.0, 1.0, 1.0)`
        - `'equal'`: No scaling, respect data aspect ratio
        - `tuple` with three floats
        """
        return self._aspect_ratio
    
    @aspect_ratio.setter
    def aspect_ratio(self, ratio='auto'):
        """ Set aspect ratio of the 3D axis """
        self._aspect_ratio = ratio
        self.update()

    @property
    def projection(self):
        """ Projection method, can be either 'perspective' or 'orthographic' """
        return self._projection_method
    
    @projection.setter
    def projection(self, projection_method='perspective'):
        self._projection_method = projection_method
        self.update()

    @property
    def label_fmt(self):
        """ Number format of the labels, default: '.1f' """
        return self._label_fmt
    
    @label_fmt.setter
    def label_fmt(self, fmt: str):
        self._label_fmt = fmt
        self.update()

    @property
    def xlim(self):
        """Custom x-axis limits"""
        return self._lim['x']
    
    @xlim.setter
    def xlim(self, xlim: list):
        self._lim['x'] = xlim
        self.update()

    @property
    def ylim(self):
        """Custom y-axis limits"""
        return self._lim['y']
    
    @ylim.setter
    def ylim(self, ylim: list):
        self._lim['y'] = ylim
        self.update()

    @property
    def zlim(self):
        """Custom z-axis limits"""
        return self._lim['z']
    
    @zlim.setter
    def zlim(self, zlim: list):
        self._lim['z'] = zlim
        self.update()

    @staticmethod
    def _check_ticks(no_ticks):
        if no_ticks > 1:
            return no_ticks
        raise InvalidTicks(
            f'No. of ticks should be larger than 1, received: {no_ticks}'
        )

    @property
    def xticks(self):
        """ Approximate number of x-axis ticks

        Should be 2 or larger.
        """
        return self._max_no_ticks['x']

    @xticks.setter
    def xticks(self, no_ticks: int):
        self._max_no_ticks['x'] = self._check_ticks(no_ticks)
        self.update()

    @property
    def yticks(self):
        """ Approximate number of x-axis ticks

        Should be 2 or larger.
        """
        return self._max_no_ticks['y']

    @yticks.setter
    def yticks(self, no_ticks: int):
        self._max_no_ticks['y'] = self._check_ticks(no_ticks)
        self.update()

    @property
    def zticks(self):
        """ Approximate number of x-axis ticks

        Should be 2 or larger.
        """
        return self._max_no_ticks['z']

    @zticks.setter
    def zticks(self, no_ticks: int):
        self._max_no_ticks['z'] = self._check_ticks(no_ticks)
        self.update()

    def delete(self):
        """ Closes the axis """


class Axis:
    """ General Axis class, creates either 2D or 3D axis """
    def __new__(cls, *args, **kwargs):
        axis_type = kwargs.pop('axis_type', '2D')
        if axis_type == '2D':
            return Axis2D(*args, **kwargs)
        if axis_type == '3D':
            return Axis3D(*args, **kwargs)
        raise InvalidAxis(f'Invalid Axis Type: {axis_type}. Should be either 2D or 3D')
