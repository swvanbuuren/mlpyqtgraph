# Introduction

mlpyqtgraph enables [matplotlib](https://matplotlib.org/)-like plotting with
[pyqtgraph](https://github.com/pyqtgraph/pyqtgraph) in existing
python programs.

It accomplishes this, by offering an interface very similar to
[matplotlib](https://matplotlib.org/), while maintaining key
[pyqtgraph](https://github.com/pyqtgraph/pyqtgraph) features such as speed and
interactivity.

mlpyqtgraph diverts the existing python program into a dedicated thread, while
using the main thread solely for plotting with pyqtgraph. This is a [requirement
of Qt](https://doc.qt.io/qt-6/thread-basics.html#gui-thread-and-worker-thread):
the Graphical User Interface (GUI) is required to run in the main thread (also
known as the "GUI thread").

This is facilitated using the python package
[pqthreads](https://github.com/swvanbuuren/pqthreads), which exposes class
interfaces from the main GUI Thread in another `QThread` in [Qt for Python
(PySide)](https://wiki.qt.io/Qt_for_Python). In doing so, it facilitates
communication between the main (GUI) thread and a dedicated `QThread`s as
offered by [Qt for Python](https://wiki.qt.io/Qt_for_Python).

The following example illustrates how mlpyqtgraph can be used in an existing
python program defined in `main`. The decorator takes care of diverting all code
within the function it decorates into a separate `QThead`. mlpyqtgraph
functionality is only available inside the decorated function and any of the
function it calls.


```python
--8<-- "examples/minimal.py:4"
```
