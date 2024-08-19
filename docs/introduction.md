# Introduction

mlpyqtgraph enables [matplotlib](https://matplotlib.org/)-like plotting with
|[pyqtgraph](https://github.com/pyqtgraph/pyqtgraph) in existing
python programs.

It accomplishes this, by offering an interface very similar to |matplotlib|,
while maintaining key |pyqtgraph| features such as speed and interactivity.

mlpyqtgraph diverts the existing python program into a dedicated thread, while
using the main thread solely for plotting with pyqtgraph. This is a [requirement
of Qt](https://doc.qt.io/qt-6/thread-basics.html#gui-thread-and-worker-thread):
the Graphical User Interface (GUI) is required to run in the main thread (also
known as the "GUI thread").

The following example illustrates how mlpyqtgraph can be used in an existing
python program defined in `main`.


```python
--8<-- "examples/minimal.py:4"
```
