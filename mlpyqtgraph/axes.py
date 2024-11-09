""" mlpyqtgraph axes module, with 2D and 3D Axis classes """


import math
from pyqtgraph.Qt import QtCore
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import pyqtgraph.functions as fn
import OpenGL.GL as ogl
import numpy as np

import mlpyqtgraph.config_options as config
from mlpyqtgraph import colors
from mlpyqtgraph.grid_axes import GLGridAxis
from mlpyqtgraph.utils.ticklabels import coord_generator, limit_generator


class RootException(Exception):
    """ Root Exception of the windows module """


class InvalidAxis(RootException):
    """ Exception raised for invalid axes """


class Axis2D(pg.PlotItem):
    """ Axis for plots in a given figure layout """
    axis_type = '2D'
    pen_styles = {'-': QtCore.Qt.SolidLine,
                  '--': QtCore.Qt.DashLine,
                  ':': QtCore.Qt.DotLine,
                  '.-': QtCore.Qt.DashDotLine}
    colors_defs = colors.ColorDefinitions()
    line_colors = colors_defs.get_line_colors()
    scale_box_line_color = colors_defs.get_scale_box_colors(part='line')
    scale_box_fill_color = colors_defs.get_scale_box_colors(part='fill')
    def __init__(self, index, **kwargs):
        parent = kwargs.pop('parent', None)
        super().__init__(parent=parent, **kwargs)
        self.index = index
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

    def add(self, x_coord, y_coord, **kwargs):
        """
        Add a line to the Axes

        **Keyword arguments**

        ============ ===========================================================
        color        line color, default value will determine using
                     :py:meth:`default_line_color()<mlpyqtgraph.axes.Axis2D.default_line_color>`
        style        line style
        width        line width
        symbol       symbol type
        symbol_size  symbol size
        symbol_color symbol color
        ============ ===========================================================
        """
        color = kwargs.get('color', self.default_line_color())
        width = kwargs.get('width', 2.0)
        if config.options.get_option('no_segmented_line_mode'):
            color = self.fix_line_artifacts(width, color)
        style = kwargs.get('style', '-')
        symbol = kwargs.get('symbol')
        symbol_size = kwargs.get('symbol_size', 5)
        symbol_color = kwargs.get('symbol_color', 'k')

        line_pen = None
        if width > 0:
            line_pen = pg.mkPen(color, width=width)
            if style:
                line_pen.setStyle(self.pen_styles[style])

        symbol_pen = None
        if symbol is not None:
            symbol_pen = pg.mkPen(symbol_color, width=0)

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
        legend_brush = pg.mkBrush(color=(255, 255, 255, 200))
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
        length_px = pg.Point(points[1] - points[0]).length()
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


class Axis3D(gl.GLGraphicsItem.GLGraphicsItem):
    """ 3D axis """
    axis_type = '3D'

    glOption = {
        ogl.GL_DEPTH_TEST: True,
        ogl.GL_BLEND: True,
        ogl.GL_ALPHA_TEST: False,
        ogl.GL_CULL_FACE: False,
        ogl.GL_LINE_SMOOTH: True,
        'glHint': (ogl.GL_LINE_SMOOTH_HINT, ogl.GL_NICEST),
        'glBlendFunc': (ogl.GL_SRC_ALPHA, ogl.GL_ONE_MINUS_SRC_ALPHA),
    }

    glOption_surface = {
        **glOption,
        ogl.GL_POLYGON_OFFSET_FILL: True,
        'glPolygonOffset': (1.0, 1.0 ),
    }

    glOption_lines = {
        **glOption,
        ogl.GL_POLYGON_OFFSET_FILL: False,
    }

    default_surface_options = {
        'glOptions': glOption_surface,
        'colormap': 'viridis',
        'smooth': True,
        'projection': 'perspective',
    }

    default_line_options = {
        'color': (0, 0, 0, 1),
        'antialias': True,
        'width': 1,
    }

    grid_line_options = {
        **default_line_options,
        'glOptions': glOption_lines,
    }

    def __init__(self, index, parentItem=None, **kwargs):
        super().__init__(parentItem=parentItem, **kwargs)
        self.index = index
        self.grid_axes = GLGridAxis(parentItem=self)
        #self.view().setCameraPosition(**self.grid_axes.best_camera())

    def _setView(self, v):
        super()._setView(v)
        for child in self.childItems():
            child._setView(v)

    @staticmethod
    def set_colormap(surface, colormap='CET-L10'):
        """ Assign colormap to surface using surface height """
        heights = surface._z
        normalized_heights = (heights - heights.min())/np.ptp(heights)
        colors = pg.colormap.get(colormap).map(normalized_heights, mode='float')
        surface._meshdata.setFaceColors(colors)

    def set_projection_method(self, *coords, method='orthographic'):
        """ Sets the projection method, either perspective or orthographic """
        object_size = (sum([np.ptp(coord)**3.0 for coord in coords]))**(1.0/3.0)
        field_of_view = 60
        if method == 'orthographic':
            field_of_view = 1
        distance = 0.75*object_size/math.tan(0.5*field_of_view/180.0*math.pi)
        self.view().setCameraParams(fov=field_of_view, distance=distance)

    def surf(self, *args, **kwargs):
        """ Adds a 3D surface plot item to the view widget  """
        kwargs = dict(self.default_surface_options, **kwargs)
        surface = gl.GLSurfacePlotItem(*args, **kwargs)
        self.view().addItem(surface)
        self.set_colormap(surface, colormap=kwargs['colormap'])
        self.set_projection_method(*args, method=kwargs['projection'])
        self.add_grid_lines(*args)
        self.update_grid_axes(*args, **kwargs)

    def calculate_ax_coord_lims(self, x, y, z):
        """ Calculates the axis coordinates limits """
        coords = dict(coord_generator(x=x, y=y, z=z))
        limits = dict(limit_generator(limit_ratio=0.05, **coords))
        return coords, limits

    def update_grid_axes(self, *args, **kwargs):
        """ Plots the grid axes """
        coords, limits = self.calculate_ax_coord_lims(*args)
        self.grid_axes.setData(coords=coords, limits=limits)
        projection = kwargs.get('projection', 'perspective')
        print(projection)
        self.view().setCameraPosition(**self.grid_axes.best_camera(method=projection))

    def add_grid_lines(self, *args):
        """ Plots all grid lines """
        x, y, z = args[:3]
        rows, columns = z.shape
        for row in range(rows):
            self.add_line(
                x[row]*np.ones(columns), y, z[row],
                **self.grid_line_options
            )
        for col in range(columns):
            self.add_line(
                x, y[col]*np.ones(rows), z[:, col],
                **self.grid_line_options
            )

    def add_line(self, *args, **kwargs):
        """ Plots a single grid line for given coordinates """
        points = np.column_stack(args)
        line = gl.GLLinePlotItem(pos=points, **kwargs)
        self.view().addItem(line)

    def line(self, *args, **kwargs):
        """ Plots a single grid line for given coordinates """
        kwargs = dict(self.default_line_options, **kwargs)
        lines_kwargs = dict(kwargs)
        lines_kwargs.pop('projection')
        self.add_line(*args, **lines_kwargs)
        self.set_projection_method(*args, method=kwargs['projection'])
        self.update_grid_axes(*args, **kwargs)

    @property
    def azimuth(self):
        return self.view().cameraParams()['azimuth']

    @azimuth.setter
    def azimuth(self, value):
        self.view().setCameraParams(azimuth=value)

    @property
    def elevation(self):
        return self.view().cameraParams()['elevation']

    @elevation.setter
    def elevation(self, value):
        self.view().setCameraParams(elevation=value)

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
