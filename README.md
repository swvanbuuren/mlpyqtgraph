# mlpyqtgraph

mlpyqtgraph enables [matplotlib](https://matplotlib.org/)-like plotting with
[pyqtgraph](https://github.com/pyqtgraph/pyqtgraph) in existing python programs.
It relies on [pqthreads](https://github.com/swvanbuuren/pqthreads) to separate mlpyqtgraph's plotting functionality from the existing python program, by separating them in different `Qthread`s.

Checkout the [documentation's
introduction](https://swvanbuuren.github.io/mlpyqtgraph/introduction/) for more
background information.

## Getting started

### Installation

First, install mlpyqtgraph like any other python package using `pip`:

``` bash
pip install mlpyqtgraph
```

Detailed installation instructions are found in the
[documentation](https://swvanbuuren.github.io/mlpyqtgraph/installation/).

### Usage

To use mlpyqtgraph, decorate your main function with mlpyqtgraph's `plotter`
decorator. This diverts the existing python program into a dedicated thread,
while using the main thread solely for plotting with pyqtgraph.

Now you can use mlpyqtgraph's plot functionalities inside your decorated
function. A python program that shows a very basic plot could look like this:

```python
import mlpyqtgraph as mpg

@mpg.plotter
def main():
    """ Minimal mlpyqtgraph example """
    mpg.plot(range(5), (1, 3, 2, 0, 5))

if __name__ == '__main__':
    main()
```

## Examples

Please refer to the [examples](/examples) for a few applications of mlpyqtgraph.

## Documentation

Check out the [documentation](https://swvanbuuren.github.io/mlpyqtgraph/)!
Please note that it's currently still under construction.

## License

An MIT style license applies for mlpyqtgraph, see the [LICENSE](LICENSE) file
for more details.
