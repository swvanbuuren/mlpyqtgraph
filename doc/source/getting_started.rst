Getting started
===============

To get started using mlpyqtgraph, it first needs to be installed. Refer to
:ref:`installation page <Installation>` for instructions.

Now, mlpyqtgraph can be used in existing python programs.

To get started, try out the `minimal example
<https://github.com/swvanbuuren/mlpyqtgraph/blob/main/examples/minimal.py>`_
from the `mlpyqtgraph examples
<https://github.com/swvanbuuren/mlpyqtgraph/blob/main/examples>`_.

.. code-block:: python

   import mlpyqtgraph as mpg

   def main():
       """ Existing program where mlpyqtgrpah plotting is available """
       mpg.plot(range(5), (1, 3, 2, 0, 5))

   if __name__ == '__main__':
       mpg.GUIController(worker=main)
