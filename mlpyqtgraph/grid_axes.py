""" 3D GridAxis classes """

import numpy as np
from pyqtgraph import QtGui, QtCore, Vector
from pyqtgraph.opengl.GLGraphicsItem import GLGraphicsItem
from pyqtgraph.opengl import GLLinePlotItem, GLMeshItem, GLTextItem


def check_visibility(azimuth_range, azimuth, elevation_range=None, elevation=None):
    """Check if item should be visible based on camera angles.
    
    Handles azimuth ranges that may wrap around 360 degrees.
    For example, (270, 450) covers both 270-360 and 0-90.
    
    Args:
        azimuth_range: tuple (min, max) or None
        elevation_range: tuple (min, max) or None
        azimuth: current azimuth angle
        elevation: current elevation angle
    
    Returns:
        bool: True if visible, False otherwise
    """
    if azimuth_range is not None:
        min_az, max_az = azimuth_range
        if max_az > 360:
            azimuth_extended = azimuth + 360 if azimuth < min_az % 360 else azimuth
            if not (min_az <= azimuth_extended < max_az):
                return False
        else:
            if not (min_az <= azimuth < max_az):
                return False
    
    if elevation_range is not None:
        min_el, max_el = elevation_range
        if not (min_el <= elevation < max_el):
            return False
    
    return True


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
        self.azimuth_range: tuple | None = None
        self.elevation_range: tuple | None = None

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
        azimuth_range         tuple (min, max) or list of tuples for visibility
        elevation_range       tuple (min, max) or list of tuples for visibility
        ====================  ==================================================
        """
        args = ('plane', 'offset', 'coords', 'limits', 'azimuth_range', 'elevation_range')
        for k in kwargs.keys():
            if k not in args:
                raise ValueError(f'Invalid keyword argument: {k} (allowed arguments are {args})')
        for key, value in kwargs.items():
            setattr(self, key, value)
        vertices, faces = self._backplane_face()
        self.mesh.setMeshData(vertexes=vertices, faces=faces)
        self.lineplot.setData(pos=self._collect_grid_line_segments())
        self.update()

    def is_visible(self, azimuth, elevation):
        """Check if plane should be visible based on camera angles."""
        return check_visibility(
            self.azimuth_range, azimuth, self.elevation_range, elevation
        )

    def _grid_positions(self):
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

    def _collect_grid_line_segments(self):
        if lines := list(self._grid_positions()):
            return np.vstack(lines).astype(np.float32)
        return np.empty((0, 3), dtype=np.float32)

    def _backplane_face(self):
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
    line_options = dict(color=(0, 0, 0, 1), antialias=True, width=1)
    offset_map = {
        'xm':  (0, -1, 0),
        'xp':  (0, +1, 0),
        'ym':  (-1, 0, 0),
        'yp':  (+1, 0, 0),
        'zrmm': (0, -1, 0),
        'zrmp': (-1, 0, 0),
        'zrpm': (+1, 0, 0),
        'zrpp': (0, +1, 0),
        'zlmm': (+1, 0, 0),
        'zlmp': (0, -1, 0),
        'zlpm': (0, +1, 0),
        'zlpp': (-1, 0, 0),
    }
    align_left = QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
    align_right = QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
    alignment_by_axis_prefix = {
        'x':  (align_left, align_right),
        'y':  (align_right, align_left),
        'zr': (align_left, align_left),
        'zl': (align_right, align_right),
    }
    offset_factor = 0.02

    def __init__(self, parentItem=None, **kwargs):
        super().__init__(parentItem=parentItem)

        self.coords = (0, 1)
        self.ax_limits = (-0.05, 1.05)
        self.limits = (-0.05, 1.05), (-0.05, 1.05)
        self.axis = 'xm'
        self.font = QtGui.QFont('Helvetica', 10)
        self.color = (0, 0, 0, 255)
        self.azimuth_range: tuple | None = None
        self.elevates: bool = True

        self._is_bottom = True
        self._labels = []

        self.lineplot = GLLinePlotItem(parentItem=self, mode='lines', **self.line_options)
        self.lineplot.setDepthValue(self.depthValue() + 1)

        self.setData(**kwargs)

    def setData(self, **kwargs):
        """ Update the axis labels """
        args = ('coords', 'ax_limits', 'limits', 'axis', 'font', 'color', 'azimuth_range', 'elevates')
        for k in kwargs.keys():
            if k not in args:
                raise ValueError(f'Invalid keyword argument: {k} (allowed arguments are {args})')
        for key, value in kwargs.items():
            setattr(self, key, value)
        self._labels = list(self.create_labels())
        self.lineplot.setData(pos=self.build_line_segments())
        self.update()

    def is_visible(self, azimuth, elevation):
        """Check if axis should be visible based on camera angles."""
        return check_visibility(self.azimuth_range, azimuth)

    def move_up(self):
        """ Move the labels up """
        if not self._is_bottom:
            return
        self._move_axis_z(self.limits[1][1])
        self._is_bottom = False

    def move_down(self):
        """ Move the labels down """
        if self._is_bottom:
            return
        self._move_axis_z(self.limits[1][0])
        self._is_bottom = True

    def elevate(self, elevation):
        """ Raise or lower the axis labels based on elevation """
        if not self.elevates:
            return
        if elevation < 0.0:
            self.move_up()
        else:
            self.move_down()

    def alignment(self):
        """Return text alignment based on axis orientation."""
        axis = self.axis
        suffix_is_mp = axis.endswith(('mp', 'pm'))

        for prefix, (normal, flipped) in self.alignment_by_axis_prefix.items():
            if axis.startswith(prefix):
                return flipped if suffix_is_mp else normal

        raise ValueError(f'Invalid axis: {axis}')

    def tick_offset(self):
        """Scalar offset used for tick marks."""
        (l1a, l1b), (l2a, l2b) = self.limits
        a0, a1 = self.ax_limits
        return self.offset_factor * ((a1 - a0) + (l1b - l1a) + (l2b - l2a))

    def axis_coordinates(self, coord):
        """Return base coordinate for given axis and scalar coord."""
        lim1, lim2 = self.limits

        axis_map = {
            'xm':   (coord, lim1[0], lim2[0]),
            'xp':   (coord, lim1[1], lim2[0]),
            'ym':   (lim1[0], coord, lim2[0]),
            'yp':   (lim1[1], coord, lim2[0]),
            'zrmm': (lim1[0], lim2[0], coord),
            'zrmp': (lim1[0], lim2[1], coord),
            'zrpm': (lim1[1], lim2[0], coord),
            'zrpp': (lim1[1], lim2[1], coord),
            'zlmm': (lim1[1], lim2[1], coord),
            'zlmp': (lim1[1], lim2[0], coord),
            'zlpm': (lim1[0], lim2[1], coord),
            'zlpp': (lim1[0], lim2[0], coord),
        }

        return np.asarray(axis_map[self._axis_key()], dtype=float)

    def tick_coordinates(self, coord):
        base = self.axis_coordinates(coord)
        delta = self.tick_offset()*np.asarray(self.offset_map[self._axis_key()])
        return np.vstack([base, base + delta])

    def axis_line_coordinates(self):
        start, end = self.ax_limits
        return np.vstack([
            self.axis_coordinates(start),
            self.axis_coordinates(end),
        ])

    def create_labels(self):
        """Orphans old labels and yield new ones."""
        for label in self._labels:
            label.setParentItem(None)
        alignment = self.alignment()
        for coord in self.coords:
            yield GLTextItem(
                parentItem=self,
                pos=self.tick_coordinates(coord)[1],
                text=f'{coord:.1f}',
                color=self.color,
                font=self.font,
                alignment=alignment,
            )

    def build_line_segments(self, z=None):
        if segments := list(self._yield_line_segments(z)):
            return np.vstack(segments).astype(np.float32)
        return np.empty((0, 3), np.float32)

    def _axis_key(self):
        """Key used for offset & alignment (direction only)."""
        return self.axis if self.axis in self.offset_map else self.axis[:2]

    def _yield_line_segments(self, z=None):
        for coord in self.coords:
            segment = self.tick_coordinates(coord)
            segment[1] -= 0.5 * (segment[1] - segment[0])
            if z is not None:
                segment[:, 2] = z
            yield segment
        
        axis = self.axis_line_coordinates()
        if z is not None:
            axis[:, 2] = z
        yield axis

    def _move_axis_z(self, z):
        for label in self._labels:
            x, y, _ = label.pos
            label.setData(pos=(x, y, z))
        self.lineplot.setData(pos=self.build_line_segments(z))


class GLGridAxis(GLGraphicsItem):
    """ Draw a grid with axes, ticks and labels in 3D space for given
    coordinates and limits """
    grid_configs = (
        ('x', 'y', 'z', (270.0, 450.0), None),
        ('x', 'y', 'z', (90.0, 270.0), None),
        ('y', 'x', 'z', (0.0, 180.0), None),
        ('y', 'x', 'z', (180.0, 360.0), None),
        ('z', 'x', 'y', None, (0.0, 90.0)),
        ('z', 'x', 'y', None, (-90.0, 0.0)),
    )
    axis_configs = (
        ('x', 'mm', 'y', 'z', (180.0, 270.0), True),
        ('x', 'mp', 'y', 'z', (270.0, 360.0), True),
        ('x', 'pm', 'y', 'z', (90.0, 180.0), True),
        ('x', 'pp', 'y', 'z', (0.0, 90.0), True),
        ('y', 'mm', 'x', 'z', (180.0, 270.0), True),
        ('y', 'pm', 'x', 'z', (270.0, 360.0), True),
        ('y', 'mp', 'x', 'z', (90.0, 180.0), True),
        ('y', 'pp', 'x', 'z', (0.0, 90.0), True),
        ('z', 'rmm', 'x', 'y', (135.0, 180.0), False),
        ('z', 'rmp', 'x', 'y', (45.0, 90.0), False),
        ('z', 'rpm', 'x', 'y', (215.0, 270.0), False),
        ('z', 'rpp', 'x', 'y', (315.0, 360.0), False),
        ('z', 'lmm', 'x', 'y', (90.0, 135.0), False),
        ('z', 'lmp', 'x', 'y', (0.0, 45.0), False),
        ('z', 'lpm', 'x', 'y', (180.0, 215.0), False),
        ('z', 'lpp', 'x', 'y', (270.0, 315.0), False),
    )

    def __init__(self, parentItem=None, **kwargs):
        super().__init__(parentItem=parentItem)
        self.coords = {axis: [-1.0, 0.0, 1.0] for axis in 'xyz'}
        self.limits = {axis: [-1.05, 1.05] for axis in 'xyz'}
        self._last_view = [0.0, 0.0]
        self._grid = [
            GLGridPlane(
                parentItem=self,
                plane=plane,
                azimuth_range=azimuth_range,
                elevation_range=elevation_range,
            )
            for plane, _, _, azimuth_range, elevation_range in self.grid_configs
        ]
        self._axes = [
            GLAxis(
                parentItem=self,
                axis=axis+edge,
                azimuth_range=azimuth_range,
                elevates=elevates,
            )
            for axis, edge, _, _, azimuth_range, elevates in self.axis_configs
        ]
        self.setData(**kwargs)

    def setData(self, **kwargs):
        """ Update the axis labels """
        args = ('coords', 'limits')
        for k in kwargs.keys():
            if k not in args:
                raise ValueError(f'Invalid keyword argument: {k} (allowed arguments are {args})')
        for key, value in kwargs.items():
            setattr(self, key, value)
        for idx, grid in enumerate(self._grid):
            plane, coord1, coord2, _, _ = self.grid_configs[idx]
            grid.setData(
                offset=self.limits[plane][idx % 2],
                coords=[self.coords[coord1], self.coords[coord2]],
                limits=[self.limits[coord1], self.limits[coord2]],
            )
        for idx, axis in enumerate(self._axes):
            axis_char, _, coord1, coord2, _, _ = self.axis_configs[idx]
            axis.setData(
                ax_limits=self.limits[axis_char],
                coords=self.coords[axis_char],
                limits=[self.limits[coord1], self.limits[coord2]],
            )
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
        new_pos = Vector(*center)
        bounding_box_diagonal = np.linalg.norm(bbox_max - bbox_min)
        fov_rad = np.radians(field_of_view)
        camera_distance = (bounding_box_diagonal / 2.0) / np.tan(fov_rad / 2.0) * distance_factor
        return {'pos': new_pos, 'distance': camera_distance}

    def view_angle(self):
        """ Get the current view angle """
        if not self.view():
            return 0.0, 0.0
        camera_params = self.view().cameraParams()
        azimuth, elevation = camera_params['azimuth'], camera_params['elevation']
        azimuth = np.mod(azimuth, 360.0)
        return azimuth, elevation
    
    def paint(self):
        super().paint()

        azimuth, elevation = self.view_angle()
        if self._last_view == [azimuth, elevation]:
            return
        self._last_view = [azimuth, elevation]

        for grid in self._grid:
            grid.hide()
        for axis in self._axes:
            axis.hide()

        for grid in self._grid:
            if grid.is_visible(azimuth, elevation):
                grid.show()

        for axis in self._axes:
            if axis.is_visible(azimuth, elevation):
                axis.show()
                axis.elevate(elevation)
