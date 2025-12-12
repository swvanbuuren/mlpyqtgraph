""" 3D GridAxis classes """

import numpy as np
from pyqtgraph import QtGui, QtCore
import pyqtgraph as pg
from pyqtgraph.opengl.GLGraphicsItem import GLGraphicsItem
from pyqtgraph.opengl import GLLinePlotItem, GLMeshItem, GLTextItem
import OpenGL.GL as ogl
from collections import namedtuple


class GLGridPlane(GLGraphicsItem):
    """ Grid plane in 3D space """

    surface_options = {
        'color': (0.95, 0.95, 0.95, 1),
        'smooth': True,
        'projection': 'perspective',
    }

    line_options = {
        'color': (0.7, 0.7, 0.7, 1),
        'antialias': True,
        'width': 1,
    }

    def __init__(self, parentItem=None, **kwargs):
        super().__init__(parentItem=parentItem)
        self.items = []
        self.plane = 'x'
        self.offset = 0.0
        self.coords = (0, 1), (0, 1)
        self.limits = (-0.05, 1.05), (-0.05, 1.05)
        
        self.lineplot = GLLinePlotItem(parentItem=self, mode='lines', **self.line_options)
        self.lineplot.setDepthValue(self.depthValue() + 1)
        self.setParentItem(parentItem)

        self.mesh = GLMeshItem(parentItem=self, **self.surface_options)

        self.setData(**kwargs)

    def setData(self, **kwargs):
        """Update the grid plane

        ====================  ==================================================
        **Arguments:**
        ------------------------------------------------------------------------
        plane                 'x', 'y', or 'z', specifies in which plane the
                              grid lies
        offset                the offset along the axis orthogonal to the plane
        coords                tuples with the coordinates for the first and
                              second axis and the grid
        limits                tuples with the limits for the first and
                              second axis and the grid
        ====================  ==================================================
        """
        args = ('plane', 'offset', 'coords', 'limits')
        for k in kwargs.keys():
            if k not in args:
                raise ValueError(f'Invalid keyword argument: {k} (allowed arguments are {args})')
        for key, value in kwargs.items():
            setattr(self, key, value)
        vertices, faces = self.backplane_face()
        self.mesh.setMeshData(vertexes=vertices, faces=faces)
        self.lineplot.setData(pos=self._get_all_grid_lines())
        self.update()

    def grid_positions(self):
        """Create a grid positions in the specified plane.

        Parameters:
        - plane: 'x', 'y', or 'z', specifies in which plane the grid lies.
        - offset: the offset along the axis orthogonal to the plane.
        - coord1: coordinates for the first axis of the grid.
        - coord2: coordinates for the second axis of the grid.
        """
        coord1, coord2 = self.coords
        lim1, lim2 = self.limits
        plane, offset = self.plane, self.offset
        if plane == 'x':
            for y in coord1:
                yield np.array([[offset, y, lim2[0]], [offset, y, lim2[1]]])
            for z in coord2:
                yield np.array([[offset, lim1[0], z], [offset, lim1[1], z]])
        elif plane == 'y':
            for x in coord1:
                yield np.array([[x, offset, lim2[0]], [x, offset, lim2[1]]])
            for z in coord2:
                yield np.array([[lim1[0], offset, z], [lim1[1], offset, z]])
        elif plane == 'z':
            for x in coord1:
                yield np.array([[x, lim2[0], offset], [x, lim2[1], offset]])
            for y in coord2:
                yield np.array([[lim1[0], y, offset], [lim1[1], y, offset]])

    def _get_all_grid_lines(self):
        """Collect all grid line segments into a single flattened array.
        
        Returns a (N, 3) array where consecutive pairs of points form line segments.
        """
        if lines := list(self.grid_positions()):
            # Concatenate all line segments: (N_lines*2, 3)
            return np.vstack(lines).astype(np.float32)
        return np.empty((0, 3), dtype=np.float32)

    def backplane_face(self):
        """Create a backplane face in the specified plane.

        Parameters:
        - plane: 'x', 'y', or 'z', specifies in which plane the grid lies.
        - offset: the offset along the axis orthogonal to the plane.
        - coord1: coordinates for the first axis of the grid.
        - coord2: coordinates for the second axis of the grid.
        """
        plane = self.plane
        offset = self.offset
        lim1, lim2 = self.limits
        faces = np.array([[0, 1, 2], [0, 2, 3]])
        if plane == 'x':
            vertices = np.array([
                [offset, lim1[0], lim2[0]],
                [offset, lim1[1], lim2[0]],
                [offset, lim1[1], lim2[1]],
                [offset, lim1[0], lim2[1]],
            ])
            return vertices, faces
        if plane == 'y':
            vertices = np.array([
                [lim1[0], offset, lim2[0]],
                [lim1[1], offset, lim2[0]],
                [lim1[1], offset, lim2[1]],
                [lim1[0], offset, lim2[1]],
            ])
            return vertices, faces
        if plane == 'z':
            vertices = np.array([
                [lim1[0], lim2[0], offset],
                [lim1[1], lim2[0], offset],
                [lim1[1], lim2[1], offset],
                [lim1[0], lim2[1], offset],
            ])
            return vertices, faces
        raise ValueError('Invalid plane')


class GLAxis(GLGraphicsItem):
    """ Axis with ticks and labels in 3D space """
    line_options = {
        'color': (0, 0, 0, 1),
        'antialias': True,
        'width': 1,
    }
    offset_map = {
        'xm': [0, -1, 0],
        'xp': [0, +1, 0],
        'ym': [-1, 0, 0],
        'yp': [+1, 0, 0],
        'zrmm': [0, -1, 0],
        'zrmp': [-1, 0, 0],
        'zrpm': [+1, 0, 0],
        'zrpp': [0, +1, 0],
        'zlmm': [+1, 0, 0],
        'zlmp': [0, -1, 0],
        'zlpm': [0, +1, 0],
        'zlpp': [-1, 0, 0]

    }
    left_alignment = QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
    right_alignment = QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
    offset_factor = 0.02

    def __init__(self, parentItem=None, **kwargs):
        super().__init__(parentItem=parentItem)
        self.coords = (0, 1), (0, 1)
        self.ax_limits = (-0.05, 1.05)
        self.limits = (-0.05, 1.05), (-0.05, 1.05)
        self.axis = 'xm'
        self.font = QtGui.QFont('Helvetica', 10)
        self.color = (0, 0, 0, 255)
        self._is_bottom = True
        self.labels = []
        self.lineplot = GLLinePlotItem(parentItem=self, mode='lines', **self.line_options)
        self.lineplot.setDepthValue(self.depthValue() + 1)
        self.setData(**kwargs)

    def setData(self, **kwargs):
        """ Update the axis labels """
        args =  ('coords', 'ax_limits', 'limits', 'axis', 'font', 'color')
        for k in kwargs.keys():
            if k not in args:
                raise ValueError(f'Invalid keyword argument: {k} (allowed arguments are {args})')
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.labels = list(self.create_labels())
        self.lineplot.setData(pos=self.build_line_segments())
        self.update()

    def alignments(self):
        """ Define the grid points in the plain defined by axis=offset """
        if self.axis.startswith('x'):
            if self.axis.endswith('mp') or self.axis.endswith('pm'):
               return self.right_alignment
            return self.left_alignment

        if self.axis.startswith('y'):
            if self.axis.endswith('mp') or self.axis.endswith('pm'):
               return self.left_alignment
            return self.right_alignment

        if self.axis.startswith('zr'):
            return self.left_alignment

        if self.axis.startswith('zl'):
            return self.right_alignment

        raise ValueError('Invalid axis')

    def calculate_tick_offset(self):
        """ Calculate the tick offset """
        lim1, lim2 = self.limits
        return self.offset_factor*(np.diff(self.ax_limits) +
                                   np.diff(lim1) +
                                   np.diff(lim2))

    def get_axis_map(self, coord):
        """Get axis coordinate mapping based on axis type and limits.
        """
        lim1, lim2 = self.limits
        axis_map = {
            'xm': [coord, lim1[0], lim2[0]],
            'xp': [coord, lim1[1], lim2[0]],
            'ym': [lim1[0], coord, lim2[0]],
            'yp': [lim1[1], coord, lim2[0]],
            'zrmm': [lim1[0], lim2[0], coord],
            'zrmp': [lim1[0], lim2[1], coord],
            'zrpm': [lim1[1], lim2[0], coord],
            'zrpp': [lim1[1], lim2[1], coord],
            'zlmm': [lim1[1], lim2[1], coord],
            'zlmp': [lim1[1], lim2[0], coord],
            'zlpm': [lim1[0], lim2[1], coord],
            'zlpp': [lim1[0], lim2[0], coord],

        }
        return axis_map

    def _resolve_axis_key(self, axis_map):
        return self.axis if self.axis in axis_map else self.axis[:2]

    def tick_coordinates(self, coord):
        """ Define the grid points in the plain defined by axis=offset """
        axis_map = self.get_axis_map(coord)
        offset = self.calculate_tick_offset()
        
        axis_key = self._resolve_axis_key(axis_map)
        base = axis_map[axis_key]
        delta = offset * self.offset_map[axis_key]
        
        return np.array([base, np.add(base, delta)])

    def tick_axis_coordinates(self):
        """ Define the grid points in the plain defined by axis=offset """
        start, end = self.ax_limits
        
        axis_map_start = self.get_axis_map(start)
        axis_key = self._resolve_axis_key(axis_map_start)
        start_coords = axis_map_start[axis_key]
        end_coords = self.get_axis_map(end)[axis_key]
        
        return np.array([start_coords, end_coords])

    def create_labels(self):
        """Orphans old labels and yield new ones."""
        for label in self.labels:
            label.setParentItem(None)
        alignment = self.alignments()
        for tick_coord in self.coords:
            text = f'{tick_coord:.1f}'
            pos = self.tick_coordinates(tick_coord)
            yield GLTextItem(
                parentItem=self,
                pos=pos[1],
                text=text,
                color=self.color,
                font=self.font,
                alignment=alignment,
            )

    def yield_line_segments(self, z_position=None):
        """Yield all axis and tick line segments."""
        for tick_coord in self.coords:
            pos = self.tick_coordinates(tick_coord)
            pos[1] = pos[1] - 0.5 * (pos[1] - pos[0])
            if z_position is not None:
                pos[:, 2] = z_position
            yield pos
        
        axis_pos = self.tick_axis_coordinates()
        if z_position is not None:
            axis_pos[:, 2] = z_position
        yield axis_pos

    def build_line_segments(self, z_position=None):
        """Build all axis and tick line segments."""
        if all_lines := list(self.yield_line_segments(z_position=z_position)):
            return np.vstack(all_lines).astype(np.float32)
        return np.empty((0, 3), dtype=np.float32)

    def move_axis_z(self, position):
        """Move the axis to a given z-position."""
        for label in self.labels:
            pos = list(label.pos)
            label.setData(pos=pos[:2] + [position, ])
        self.lineplot.setData(pos=self.build_line_segments(z_position=position))

    def move_up(self):
        """ Move the labels up """
        if not self._is_bottom:
            return
        self.move_axis_z(self.limits[1][1])
        self._is_bottom = False

    def move_down(self):
        """ Move the labels down """
        if self._is_bottom:
            return
        self.move_axis_z(self.limits[1][0])
        self._is_bottom = True


class GLGridAxis(GLGraphicsItem):
    """ Draw a grid with axes, ticks and labels in 3D space for given
    coordinates and limits """

    GridPlaneParams = namedtuple(
        'GridPlaneParams', ['plane', 'side', 'coord1', 'coord2']
    )
    AxisParams = namedtuple(
        'GridPlaneParams', ['axis', 'edge', 'coord1', 'coord2']
    )

    def __init__(self, parentItem=None, **kwargs):
        super().__init__(parentItem=parentItem)
        self.grid = {}
        self.axes = {}
        self.coords = {
            'x': [-1.0, 0.0, 1.0],
            'y': [-1.0, 0.0, 1.0],
            'z': [-1.0, 0.0, 1.0],
        }
        self.limits = {
            'x': (-1.05, 1.05),
            'y': (-1.05, 1.05),
            'z': (-1.05, 1.05),
        }
        self.last_view = [0.0, 0.0]
        self.force_paint = False
        self.setData(**kwargs)

    def grid_generator(self):
        """ yields the grid planes with their parameters """
        grid_plane_params = {
            'xl': self.GridPlaneParams('x', 0, 'y', 'z'),
            'xr': self.GridPlaneParams('x', 1, 'y', 'z'),
            'yl': self.GridPlaneParams('y', 0, 'x', 'z'),
            'yr': self.GridPlaneParams('y', 1, 'x', 'z'),
            'zb': self.GridPlaneParams('z', 0, 'x', 'y'),
            'zt': self.GridPlaneParams('z', 1, 'x', 'y'),
        }
        for key, params in grid_plane_params.items():
            plane = params.plane
            side = params.side
            coord1 = params.coord1
            coord2 = params.coord2
            grid_data = {
                'plane': plane,
                'offset': self.limits[plane][side],
                'coords': [self.coords[coord1], self.coords[coord2]],
                'limits': [self.limits[coord1], self.limits[coord2]],
            }
            yield key, grid_data

    def label_generator(self):
        """ yields the axis labels with their parameters """
        axis_labels_params = {
            'xmm': self.AxisParams('x', 'mm', 'y', 'z'),
            'xmp': self.AxisParams('x', 'mp', 'y', 'z'),
            'xpm': self.AxisParams('x', 'pm', 'y', 'z'),
            'xpp': self.AxisParams('x', 'pp', 'y', 'z'),
            'ymm': self.AxisParams('y', 'mm', 'x', 'z'),
            'ypm': self.AxisParams('y', 'pm', 'x', 'z'),
            'ymp': self.AxisParams('y', 'mp', 'x', 'z'),
            'ypp': self.AxisParams('y', 'pp', 'x', 'z'),
            'zrmm': self.AxisParams('z', 'rmm', 'x', 'y'),
            'zrmp': self.AxisParams('z', 'rmp', 'x', 'y'),
            'zrpm': self.AxisParams('z', 'rpm', 'x', 'y'),
            'zrpp': self.AxisParams('z', 'rpp', 'x', 'y'),
            'zlmm': self.AxisParams('z', 'lmm', 'x', 'y'),
            'zlmp': self.AxisParams('z', 'lmp', 'x', 'y'),
            'zlpm': self.AxisParams('z', 'lpm', 'x', 'y'),
            'zlpp': self.AxisParams('z', 'lpp', 'x', 'y'),
        }

        for key, params in axis_labels_params.items():
            axis = params.axis
            edge = params.edge
            coord1 = params.coord1
            coord2 = params.coord2
            axis_data = {
                'axis': axis + edge,
                'ax_limits': self.limits[axis],
                'coords': self.coords[axis],
                'limits': [self.limits[coord1], self.limits[coord2]],
            }
            yield key, axis_data

    def _update_container(self, container: dict, generator, item_class):
        for key, data in generator():
            if key in container:
                container[key].setData(**data)
            else:
                container[key] = item_class(parentItem=self, **data)

    def setData(self, **kwargs):
        """ Update the axis labels """
        args = ('coords', 'limits')
        for k in kwargs.keys():
            if k not in args:
                raise ValueError(f'Invalid keyword argument: {k} (allowed arguments are {args})')
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        self._update_container(self.grid, self.grid_generator, GLGridPlane)
        self._update_container(self.axes, self.label_generator, GLAxis)
       
        if self.view():
            self.paint1()
        self.update()

    def bounding_box_corners(self):
        xlim, ylim, zlim = self.limits['x'], self.limits['y'], self.limits['z']
        return (
            np.array([xlim[0], ylim[0], zlim[0]]),
            np.array([xlim[1], ylim[1], zlim[1]]),
        )

    def best_camera(self, distance_factor=1.5, method='perspective'):
        field_of_view = 60.0
        if method == 'orthographic':
            field_of_view = 1.0
            distance_factor = 1.4
        bbox_min, bbox_max = self.bounding_box_corners()
        center = (bbox_min + bbox_max) / 2.0
        new_pos = pg.Vector(*center)
        bounding_box_diagonal = np.linalg.norm(bbox_max - bbox_min)
        fov_rad = np.radians(field_of_view)
        camera_distance = (bounding_box_diagonal / 2.0) / np.tan(fov_rad / 2.0) * distance_factor

        return {'pos': new_pos, 'distance': camera_distance}

    def show_grids(self, *grid_items):
        """Show chosen grid items"""
        for item in grid_items:
            self.grid[item].show()

    def show_axes(self, *axis_items):
        """Show chosen axis items"""
        for item in axis_items:
            self.axes[item].show()

    def move_axes(self, move_up=False, move_down=False):
        """Move chosen axis items up or down"""
        axis_items = ('xmm', 'xmp', 'xpm', 'xpp', 'ymm', 'ymp', 'ypm', 'ypp')
        for item in axis_items:
            if move_up:
                self.axes[item].move_up()
            if move_down:
                self.axes[item].move_down()

    def paint1(self):
        """ Forcefully paint the scene """
        self.force_paint = True
        self.paint()

    def paint(self):
        super().paint()

        camera_params = self.view().cameraParams()
        azimuth, elevation = camera_params['azimuth'], camera_params['elevation']

        if self.last_view == [azimuth, elevation]:
            if not self.force_paint:
                return
        self.last_view = [azimuth, elevation]
        self.force_paint = False

        # hide by default
        for grid in self.grid.values():
            grid.hide()
        for label in self.axes.values():
            label.hide()

        azimuth = np.mod(azimuth, 360.0)

        if 0.0 <= azimuth < 90.0:
            self.show_axes('xpp', 'ypp')
            self.show_grids('xl', 'yl')
        elif 90.0 <= azimuth < 180.0:
            self.show_axes('xpm', 'ymp')
            self.show_grids('xr', 'yl')
        elif 180.0 <= azimuth < 270.0:
            self.show_axes('xmm', 'ymm')
            self.show_grids('xr', 'yr')
        else:
            self.show_axes('xmp', 'ypm')
            self.show_grids('xl', 'yr')

        if 0.0 <= azimuth < 45.0:
            self.show_axes('zlmp')
        elif 45.0 <= azimuth < 90.0:
            self.show_axes('zrmp')
        elif 90.0 <= azimuth < 135.0:
            self.show_axes('zlmm')
        elif 135.0 <= azimuth < 180.0:
            self.show_axes('zrmm')
        elif 180.0 <= azimuth < 215.0:
            self.show_axes('zlpm')
        elif 215.0 <= azimuth < 270.0:
            self.show_axes('zrpm')
        elif 270.0 <= azimuth < 315.0:
            self.show_axes('zlpp')
        elif 315.0 <= azimuth < 360.0:
            self.show_axes('zrpp')

        if elevation < 0.0:
            self.show_grids('zt')
            self.move_axes(move_up=True)
        else:
            self.show_grids('zb')
            self.move_axes(move_down=True)
