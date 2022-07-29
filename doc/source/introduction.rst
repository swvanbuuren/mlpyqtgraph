Introduction
============

mlpyqtgraph enables |matplotlib|\ -like plotting with |pyqtgraph| in existing
python programs.

It accomplishes this, by offering an interface very similar to |matplotlib|,
while maintaining key |pyqtgraph| features such as speed and interactivity.

mlpyqtgraph diverts the existing python program into a dedicated thread, while
using the main thread solely for plotting with pyqtgraph. This is a `requirement
of Qt
<https://doc.qt.io/qt-6/thread-basics.html#gui-thread-and-worker-thread>`_: the
Graphical User Interface (GUI) is required to run in the main thread (also known
as the "GUI thread").

The following example illustrates how mlpyqtgraph can be used in an existing
python program defined in ``main``.

.. code-block:: python

   import mlpyqtgraph as mpg

   def main():
       """ Existing program where mlpyqtgrpah plotting is available """
       mpg.plot(range(5), (1, 3, 2, 0, 5))

   if __name__ == '__main__':
       mpg.GUIController(worker=main)
