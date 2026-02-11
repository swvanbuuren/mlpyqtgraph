import enum
import importlib

import numpy as np
from OpenGL import GL
from OpenGL.GL import shaders
from pyqtgraph import functions as fn
from pyqtgraph.Qt import QT_LIB, QtGui
from pyqtgraph.opengl.GLGraphicsItem import GLGraphicsItem

if QT_LIB in ["PyQt5", "PySide2"]:
    QtOpenGL = QtGui
else:
    QtOpenGL = importlib.import_module(f"{QT_LIB}.QtOpenGL")


__all__ = ["GLPointsItem"]


class DirtyFlag(enum.Flag):
    POSITION = enum.auto()
    COLOR = enum.auto()


class GLPointsItem(GLGraphicsItem):
    """Draws points in 3D with fixed pixel size."""

    _shaderProgram = None

    def __init__(self, parentItem=None, **kwds):
        """All keyword arguments are passed to setData()."""
        super().__init__()
        glopts = kwds.pop("glOptions", "opaque")
        self.setGLOptions(glopts)
        self.pos = None
        self.size = 5.0
        self.color = (1.0, 1.0, 1.0, 1.0)
        self.depth_offset = "auto"
        self.depth_bias = "auto"

        self.m_vbo_position = QtOpenGL.QOpenGLBuffer(
            QtOpenGL.QOpenGLBuffer.Type.VertexBuffer
        )
        self.m_vbo_color = QtOpenGL.QOpenGLBuffer(
            QtOpenGL.QOpenGLBuffer.Type.VertexBuffer
        )
        self.dirty_bits = DirtyFlag(0)

        self.setParentItem(parentItem)
        self.setData(**kwds)

    def setData(self, **kwds):
        """
        Update the data displayed by this item. All arguments are optional.

        ====================  ==================================================
        **Arguments:**
        ------------------------------------------------------------------------
        pos                   (N,3) array of floats specifying point locations.
        color                 (N,4) array of floats (0.0-1.0) or
                      tuple of floats specifying
                      a single color for all points.
        size                  float specifying point size in pixels (default 5.0)
        depth_offset          tuple (factor, units), "auto", or None.
                      Uses GL_POLYGON_OFFSET_POINT when supported.
        depth_bias            float, "auto", or None.
                      Clip-space bias applied as z -= bias * w.
        ====================  ==================================================
        """
        args = ["pos", "color", "size", "depth_offset", "depth_bias"]
        for k in kwds.keys():
            if k not in args:
                raise Exception(
                    "Invalid keyword argument: %s (allowed arguments are %s)"
                    % (k, str(args))
                )

        if "pos" in kwds:
            pos = kwds.pop("pos")
            self.pos = np.ascontiguousarray(pos, dtype=np.float32)
            self.dirty_bits |= DirtyFlag.POSITION

        if "color" in kwds:
            color = kwds.pop("color")
            if isinstance(color, np.ndarray):
                color = np.ascontiguousarray(color, dtype=np.float32)
                self.dirty_bits |= DirtyFlag.COLOR
            if isinstance(color, str):
                color = fn.mkColor(color)
            if isinstance(color, QtGui.QColor):
                color = color.getRgbF()
            self.color = color

        for k, v in kwds.items():
            setattr(self, k, v)

        self.update()

    def upload_vbo(self, vbo, arr):
        if arr is None:
            vbo.destroy()
            return
        if not vbo.isCreated():
            vbo.create()
        vbo.bind()
        if vbo.size() != arr.nbytes:
            vbo.allocate(arr, arr.nbytes)
        else:
            vbo.write(0, arr, arr.nbytes)
        vbo.release()

    @staticmethod
    def getShaderProgram():
        klass = GLPointsItem

        if klass._shaderProgram is not None:
            return klass._shaderProgram

        ctx = QtGui.QOpenGLContext.currentContext()
        fmt = ctx.format()

        if ctx.isOpenGLES():
            if fmt.version() >= (3, 0):
                glsl_version = "#version 300 es\n"
                sources = SHADER_CORE
            else:
                glsl_version = ""
                sources = SHADER_LEGACY
        else:
            if fmt.version() >= (3, 1):
                glsl_version = "#version 140\n"
                sources = SHADER_CORE
            else:
                glsl_version = ""
                sources = SHADER_LEGACY

        compiled = [shaders.compileShader([glsl_version, v], k) for k, v in sources.items()]
        program = shaders.compileProgram(*compiled)

        GL.glBindAttribLocation(program, 0, "a_position")
        GL.glBindAttribLocation(program, 1, "a_color")
        GL.glLinkProgram(program)

        klass._shaderProgram = program
        return program

    def _resolve_depth_settings(self):
        depth_offset = self.depth_offset
        depth_bias = self.depth_bias

        if depth_offset != "auto" and depth_bias != "auto":
            return depth_offset, depth_bias

        is_ortho = False
        view = self.view()
        if view is not None:
            params = view.cameraParams()
            fov = params.get("fov")
            if fov is not None and fov <= 1.1:
                is_ortho = True

        if is_ortho:
            auto_offset = (0.0, -2.0)
            auto_bias = 1.0e-6
        else:
            auto_offset = (0.0, -1.0)
            auto_bias = 1.0e-4

        if depth_offset == "auto":
            depth_offset = auto_offset
        if depth_bias == "auto":
            depth_bias = auto_bias

        return depth_offset, depth_bias

    def paint(self):
        if self.pos is None:
            return
        self.setupGLState()

        mat_mvp = self.mvpMatrix()
        mat_mvp = np.array(mat_mvp.data(), dtype=np.float32)

        context = QtGui.QOpenGLContext.currentContext()

        if DirtyFlag.POSITION in self.dirty_bits:
            self.upload_vbo(self.m_vbo_position, self.pos)
        if DirtyFlag.COLOR in self.dirty_bits:
            self.upload_vbo(self.m_vbo_color, self.color)
        self.dirty_bits = DirtyFlag(0)

        program = self.getShaderProgram()

        enabled_locs = []

        loc = 0
        self.m_vbo_position.bind()
        GL.glVertexAttribPointer(loc, 3, GL.GL_FLOAT, False, 0, None)
        self.m_vbo_position.release()
        enabled_locs.append(loc)

        loc = 1
        if isinstance(self.color, np.ndarray):
            self.m_vbo_color.bind()
            GL.glVertexAttribPointer(loc, 4, GL.GL_FLOAT, False, 0, None)
            self.m_vbo_color.release()
            enabled_locs.append(loc)
        else:
            GL.glVertexAttrib4f(loc, *self.color)

        depth_was_enabled = GL.glIsEnabled(GL.GL_DEPTH_TEST)
        depth_func = GL.glGetIntegerv(GL.GL_DEPTH_FUNC)
        depth_mask = GL.glGetBooleanv(GL.GL_DEPTH_WRITEMASK)
        if hasattr(depth_mask, "__len__"):
            depth_mask = bool(depth_mask[0])
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glDepthFunc(GL.GL_LEQUAL)
        GL.glDepthMask(GL.GL_TRUE)

        depth_offset, depth_bias = self._resolve_depth_settings()

        point_offset_supported = hasattr(GL, "GL_POLYGON_OFFSET_POINT")
        offset_was_enabled = False
        prev_offset_factor = None
        prev_offset_units = None
        if point_offset_supported and depth_offset is not None:
            offset_was_enabled = GL.glIsEnabled(GL.GL_POLYGON_OFFSET_POINT)
            prev_offset_factor = GL.glGetFloatv(GL.GL_POLYGON_OFFSET_FACTOR)
            prev_offset_units = GL.glGetFloatv(GL.GL_POLYGON_OFFSET_UNITS)
            if hasattr(prev_offset_factor, "__len__"):
                prev_offset_factor = float(prev_offset_factor[0])
            if hasattr(prev_offset_units, "__len__"):
                prev_offset_units = float(prev_offset_units[0])
            GL.glEnable(GL.GL_POLYGON_OFFSET_POINT)
            GL.glPolygonOffset(*depth_offset)

        sfmt = context.format()
        core_forward_compatible = (
            sfmt.profile() == sfmt.OpenGLContextProfile.CoreProfile
            and not sfmt.testOption(sfmt.FormatOption.DeprecatedFunctions)
        )

        if not core_forward_compatible:
            GL.glEnable(GL.GL_PROGRAM_POINT_SIZE)
            GL.glPointSize(self.size)

        for loc in enabled_locs:
            GL.glEnableVertexAttribArray(loc)

        with program:
            loc = GL.glGetUniformLocation(program, "u_mvp")
            GL.glUniformMatrix4fv(loc, 1, False, mat_mvp)

            size_loc = GL.glGetUniformLocation(program, "u_pointSize")
            GL.glUniform1f(size_loc, self.size)

            bias_loc = GL.glGetUniformLocation(program, "u_depthBias")
            GL.glUniform1f(bias_loc, float(depth_bias or 0.0))

            GL.glDrawArrays(GL.GL_POINTS, 0, len(self.pos))

        for loc in enabled_locs:
            GL.glDisableVertexAttribArray(loc)

        if not core_forward_compatible:
            GL.glDisable(GL.GL_PROGRAM_POINT_SIZE)
            GL.glPointSize(1.0)

        if point_offset_supported and depth_offset is not None:
            if not offset_was_enabled:
                GL.glDisable(GL.GL_POLYGON_OFFSET_POINT)
            if prev_offset_factor is not None and prev_offset_units is not None:
                GL.glPolygonOffset(prev_offset_factor, prev_offset_units)

        GL.glDepthFunc(depth_func)
        GL.glDepthMask(depth_mask)
        if not depth_was_enabled:
            GL.glDisable(GL.GL_DEPTH_TEST)


SHADER_LEGACY = {
    GL.GL_VERTEX_SHADER: """
        uniform mat4 u_mvp;
        uniform float u_pointSize;
        uniform float u_depthBias;
        attribute vec4 a_position;
        attribute vec4 a_color;
        varying vec4 v_color;
        void main() {
            v_color = a_color;
            vec4 clip = u_mvp * a_position;
            clip.z -= u_depthBias * clip.w;
            gl_Position = clip;
            gl_PointSize = u_pointSize;
        }
    """,
    GL.GL_FRAGMENT_SHADER: """
        #ifdef GL_ES
        precision mediump float;
        #endif
        varying vec4 v_color;
        void main() {
            gl_FragColor = v_color;
        }
    """,
}

SHADER_CORE = {
    GL.GL_VERTEX_SHADER: """
        uniform mat4 u_mvp;
        uniform float u_pointSize;
        uniform float u_depthBias;
        in vec4 a_position;
        in vec4 a_color;
        out vec4 v_color;
        void main() {
            v_color = a_color;
            vec4 clip = u_mvp * a_position;
            clip.z -= u_depthBias * clip.w;
            gl_Position = clip;
            gl_PointSize = u_pointSize;
        }
    """,
    GL.GL_FRAGMENT_SHADER: """
        #ifdef GL_ES
        precision mediump float;
        #endif
        in vec4 v_color;
        out vec4 fragColor;
        void main() {
            fragColor = v_color;
        }
    """,
}


