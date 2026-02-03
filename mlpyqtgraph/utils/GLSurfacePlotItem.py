import numpy as np

from pyqtgraph.opengl import MeshData
from pyqtgraph.opengl import GLMeshItem, GLLinePlotItem
from OpenGL import GL as ogl

__all__ = ['GLSurfacePlotItem']


class GLSurfacePlotItem(GLMeshItem):
    """
    **Bases:** :class:`GLMeshItem <pyqtgraph.opengl.GLMeshItem>`
    
    Displays a surface plot on a regular x,y grid with optional wireframe overlay.
    """

    mesh_keys = ('x', 'y', 'z', 'colors')
    grid_keys = ('showGrid', 'lineColor', 'lineWidth', 'lineAntialias')

    def __init__(self, parentItem=None, **kwds):
        """
        The x, y, z, colors, showGrid, lineColor, lineWidth and lineAntialias
        arguments are passed to setData().
        All other keyword arguments are passed to GLMeshItem.__init__().
        """
        self._x = None
        self._y = None
        self._z = None
        self._color = None
        self._x_shape = None
        self._y_shape = None
        self._showGrid = False
        self._lineColor = (0, 0, 0, 1)
        self._lineWidth = 1.0
        self._lineAntialias = False
        self._vertexes = None
        self._meshdata = MeshData()

        # splitout GLSurfacePlotItem from kwds
        surface_keys = self.mesh_keys + self.grid_keys
        surface_kwds = {}
        for arg in surface_keys:
            if arg in kwds:
                surface_kwds[arg] = kwds.pop(arg)

        super().__init__(meshdata=self._meshdata, **kwds)
        
        self.lineplot = GLLinePlotItem(parentItem=self, mode='lines', glOptions='translucent')
        # in GLViewWidget.drawItemTree(), at the same depth value, child items
        # come before the parent. make it such that our grid lines get drawn
        # after the surface mesh.
        self.lineplot.setDepthValue(self.depthValue() + 1)
        self.setParentItem(parentItem)

        self.setData(**surface_kwds)
        
    def setData(self, **kwds):
        """
        Update the data in this surface plot. 
        
        ==============  =====================================================================
        **Arguments:**
        x,y             1D or 2D arrays of values specifying positions of vertexes.
                        If 1D: shape (N,) - interpreted as grid coordinates
                        If 2D: shape (rows, cols) - interpreted as per-vertex positions
                        If omitted, integers are assumed.
        z               2D array of height values, shape (rows, cols)
        colors          (width, height, 4) array of vertex colors.
        showGrid        Show the grid lines.
        lineColor       Color of the grid lines.
        lineWidth       Width of the grid lines.
        lineAntialias   Enable antialiasing for the grid lines.
        ==============  =====================================================================
        
        All arguments are optional.
        
        Note that if vertex positions are updated, the normal vectors for each triangle must 
        be recomputed. This is somewhat expensive if the surface was initialized with smooth=False
        and very expensive if smooth=True. For faster performance, initialize with 
        computeNormals=False and use per-vertex colors or a normal-independent shader program.
        """

        for arg in self.grid_keys:
            if arg in kwds:
                setattr(self, '_' + arg, kwds[arg])

        x, y, z, colors = map(kwds.get, self.mesh_keys)

        if x is not None:
            x_shape = np.asarray(x).shape
            if self._x is None or self._x_shape != x_shape:
                self._vertexes = None
            self._x = x
            self._x_shape = x_shape
        
        if y is not None:
            y_shape = np.asarray(y).shape
            if self._y is None or self._y_shape != y_shape:
                self._vertexes = None
            self._y = y
            self._y_shape = y_shape
        
        if z is not None:
            if self._x is not None and z.shape[0] != self._x_shape[0]:
                raise Exception('Z values must have shape (len(x), len(y)) or match x.shape[0]')
            if self._y is not None and z.shape[1] != self._y_shape[-1]:  # -1 handles both 1D and 2D
                raise Exception('Z values must have shape (len(x), len(y)) or match y.shape[-1]')
            self._z = z
            if self._vertexes is not None and self._z.shape != self._vertexes.shape[:2]:
                self._vertexes = None
        
        if colors is not None:
            self._colors = colors
            self._meshdata.setVertexColors(colors)
        
        if self._z is None:
            return
        
        updateMesh = False
        newVertexes = False
        
        ## Generate vertex and face array
        if self._vertexes is None:
            newVertexes = True
            self._vertexes = np.empty((self._z.shape[0], self._z.shape[1], 3), dtype=np.float32)
            self.generateFaces()
            self._meshdata.setFaces(self._faces)
            updateMesh = True
        
        ## Copy x, y, z data into vertex array
        if newVertexes or x is not None:
            if x is None:
                if self._x is None:
                    x = np.arange(self._z.shape[0])
                else:
                    x = self._x
            
            x_arr = np.asarray(x)
            if x_arr.ndim == 1:
                self._vertexes[:, :, 0] = x_arr.reshape(len(x_arr), 1)
            elif x_arr.ndim == 2:
                if x_arr.shape != self._vertexes.shape[:2]:
                    raise Exception(f'x shape {x_arr.shape} must match z shape {self._z.shape}')
                self._vertexes[:, :, 0] = x_arr
            updateMesh = True
        
        if newVertexes or y is not None:
            if y is None:
                if self._y is None:
                    y = np.arange(self._z.shape[1])
                else:
                    y = self._y
            
            y_arr = np.asarray(y)
            if y_arr.ndim == 1:
                self._vertexes[:, :, 1] = y_arr.reshape(1, len(y_arr))
            elif y_arr.ndim == 2:
                if y_arr.shape != self._vertexes.shape[:2]:
                    raise Exception(f'y shape {y_arr.shape} must match z shape {self._z.shape}')
                self._vertexes[:, :, 1] = y_arr
            updateMesh = True
        
        if newVertexes or z is not None:
            self._vertexes[...,2] = self._z
            updateMesh = True

        ## Update MeshData
        if updateMesh:
            self._meshdata.setVertexes(self._vertexes.reshape(self._vertexes.shape[0]*self._vertexes.shape[1], 3))
            self.meshDataChanged()

        # rebuild grid whenever mesh or parent changes
        self._update_grid()

    def paint(self):
        if self._showGrid:
            ogl.glEnable(ogl.GL_POLYGON_OFFSET_FILL)
            ogl.glPolygonOffset(1.0, 1.0)
        super().paint()
        if self._showGrid:
            ogl.glDisable(ogl.GL_POLYGON_OFFSET_FILL)
            ogl.glPolygonOffset(0.0, 0.0)

    def generateFaces(self):
        cols = self._z.shape[1]-1
        rows = self._z.shape[0]-1
        faces = np.empty((cols*rows*2, 3), dtype=np.uint32)
        rowtemplate1 = np.arange(cols).reshape(cols, 1) + np.array([[0, 1, cols+1]])
        rowtemplate2 = np.arange(cols).reshape(cols, 1) + np.array([[cols+1, 1, cols+2]])
        for row in range(rows):
            start = row * cols * 2 
            faces[start:start+cols] = rowtemplate1 + row * (cols+1)
            faces[start+cols:start+(cols*2)] = rowtemplate2 + row * (cols+1)
        self._faces = faces

    @staticmethod
    def _broadcast_coords(coords, target_shape, z_shape, reshaped):
        """Broadcast 1D coords or use 2D coords directly."""
        if coords is None:
            coords = np.arange(target_shape)
        coords = np.asarray(coords)
        if coords.ndim == 1:
            coords = np.broadcast_to(coords.reshape(*reshaped), z_shape)
        return coords

    def _update_grid(self):
        if not self._showGrid or self._z is None:
            return

        opts = {
            'antialias':  self._lineAntialias,
            'color':      self._lineColor,
            'width':      self._lineWidth,
        }

        z = self._z.astype(np.float32)
        rows, cols = z.shape

        xvals = self._broadcast_coords(self._x, rows, z.shape, (rows, 1))
        yvals = self._broadcast_coords(self._y, cols, z.shape, (1, cols))

        verts_flat = np.column_stack((xvals.ravel(), yvals.ravel(), z.ravel()))

        idx = np.arange(z.size, dtype=np.int32).reshape(*z.shape)
        h = np.column_stack((idx[:, :-1].ravel(), idx[:, 1:].ravel()))
        v = np.column_stack((idx[:-1, :].ravel(), idx[1:, :].ravel()))
        edges = np.vstack((h, v))

        pts = verts_flat[edges].reshape(-1, 3)

        self.lineplot.setData(pos=pts, **opts)
