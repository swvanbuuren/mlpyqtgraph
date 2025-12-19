""" 3D GridAxis with grid planes, axes, ticks and labels """

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
    sides = (
        QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter,
        QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter
    )
    offset_factor = 0.02

    def __init__(self, parentItem=None, **kwargs):
        super().__init__(parentItem=parentItem)

        self.coords = (0, 1)
        self.ax_limits = (-0.05, 1.05)
        self.limits = (-0.05, 1.05), (-0.05, 1.05)
        self.axis = 0
        self.faces = (-1, -1)
        self.tick_axis = 1
        self.label_side = 0
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
        args = ('coords', 'ax_limits', 'limits', 'axis', 'faces', 'tick_axis',
                'label_side', 'font', 'color', 'azimuth_range', 'elevates')
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
        if self._is_bottom:
            self._move_axis_z(self.limits[1][1])
            self._is_bottom = False

    def move_down(self):
        if not self._is_bottom:
            self._move_axis_z(self.limits[1][0])
            self._is_bottom = True

    def elevate(self, elevation):
        if not self.elevates:
            return
        (self.move_up if elevation < 0 else self.move_down)()

    def alignment(self):
        return self.sides[self.label_side ]

    def tick_offset(self):
        a0, a1 = self.ax_limits
        return self.offset_factor * (
            (a1 - a0) + sum(hi - lo for lo, hi in self.limits)
        )

    def fixed_axes(self):
        return (x for x in range(3) if x != self.axis)

    def axis_coordinates(self, coord):
        pos = np.zeros(3, dtype=float)
        pos[self.axis] = coord
        for fixed_axis, face, (lo, hi) in zip(
            self.fixed_axes(), self.faces, self.limits
        ):
            pos[fixed_axis] = lo if face < 0 else hi
        return pos

    def tick_delta(self):
        delta = np.zeros(3)
        idx = tuple(self.fixed_axes()).index(self.tick_axis)
        delta[self.tick_axis] = self.faces[idx]
        return delta

    def tick_coordinates(self, coord):
        base = self.axis_coordinates(coord)
        return np.vstack([base, base + self.tick_offset() * self.tick_delta()])

    def axis_line_coordinates(self):
        return np.vstack([self.axis_coordinates(x) for x in self.ax_limits])

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

    def _yield_line_segments(self, z=None):
        for coord in self.coords:
            segment = self.tick_coordinates(coord)
            segment[1] = 0.5 * (segment[0] + segment[1])
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
        ('x', (270.0, 450.0), None),
        ('x', (90.0, 270.0), None),
        ('y', (0.0, 180.0), None),
        ('y', (180.0, 360.0), None),
        ('z', None, (0.0, 90.0)),
        ('z', None, (-90.0, 0.0)),
    )
    axis_configs = (
        ('x', (-1, -1), 1, 0, (180.0, 270.0), True),
        ('x', (-1, -1), 1, 1, (270.0, 360.0), True),
        ('x', (+1, -1), 1, 1, (90.0, 180.0), True),
        ('x', (+1, -1), 1, 0, (0.0, 90.0), True),
        ('y', (-1, -1), 0, 1, (180.0, 270.0), True),
        ('y', (-1, -1), 0, 0, (90.0, 180.0), True),
        ('y', (+1, -1), 0, 0, (270.0, 360.0), True),
        ('y', (+1, -1), 0, 1, (0.0, 90.0), True),
        ('z', (-1, -1), 1, 0, (135.0, 180.0), False),
        ('z', (-1, +1), 0, 0, (45.0, 90.0), False),
        ('z', (+1, -1), 0, 0, (215.0, 270.0), False),
        ('z', (+1, +1), 1, 0, (315.0, 360.0), False),
        ('z', (+1, +1), 0, 1, (90.0, 135.0), False),
        ('z', (+1, -1), 1, 1, (0.0, 45.0), False),
        ('z', (-1, +1), 1, 1, (180.0, 215.0), False),
        ('z', (-1, -1), 0, 1, (270.0, 315.0), False),
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
            for plane, azimuth_range, elevation_range in self.grid_configs
        ]
        self._axes = [
            GLAxis(
                parentItem=self,
                axis='xyz'.index(axis),
                faces=faces,
                tick_axis=tick_axis,
                label_side=label_side,
                azimuth_range=azimuth_range,
                elevates=elevates,
            )
            for axis, faces, tick_axis, label_side, azimuth_range, elevates in self.axis_configs
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
            plane, _, _ = self.grid_configs[idx]
            coord1, coord2 = self._get_coords(plane)
            grid.setData(
                offset=self.limits[plane][idx % 2],
                coords=[self.coords[coord1], self.coords[coord2]],
                limits=[self.limits[coord1], self.limits[coord2]],
            )
        for idx, axis in enumerate(self._axes):
            axis_char, _, _, _, _, _ = self.axis_configs[idx]
            coord1, coord2 = self._get_coords(axis_char)
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

    @staticmethod
    def _get_coords(axis):
        return (c for c in 'xyz' if c != axis)