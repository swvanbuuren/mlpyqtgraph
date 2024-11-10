# Installation

mlpyqtgraph is a [python package](https://pypi.org/project/mlpyqtgraph/) which
is available on the [Python Package Index (PyPi)](https://pypi.org/). You can
install it just like any other python package using `pip`:

``` bash
pip install mlpyqtgraph
```

Alternatively, you can install mlpyqtgraph directly from source. To do this,
first clone the package from GitHub using `git`:

```bash
git clone https://github.com/swvanbuuren/mlpyqtgraph.git
```

It is recommended to install the mlpyqtgraph package into a virtual enviroment,
e.g. `venv`. Refer to its [refence
documentation](https://docs.python.org/3/library/venv.html) for more details on
its creation and usage.

After the virtual environment has been created and activated, install the
mlpyqtgraph package using e.g. `pip`:

```bash
pip install /path/to/mlpyqtgraph
```

Now, mpyqtgraph can be used whenever the appropriate virtual environment has
been activated e.g., by trying the [minimal example](https://github.com/swvanbuuren/mlpyqtgraph/blob/master/examples/minimal.py):

```bash
python examples/minimal.py
```

!!! info

    If you receive an error message similar to the following:

    ```plaintext
    Could not load the Qt platform plugin "xcb" in "" even though it was found."
    ```

    Then, you might need to install additional dependencies. On a Debian-based 
    system, this is accomplished with:

    ```bash
    sudo apt install -y libxcb-cursor-dev
    ```
