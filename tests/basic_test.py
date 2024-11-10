""" Basic tests for mlpyqtgraph """

import mlpyqtgraph as mpg


def test_open_close():
    """ Test opening and closing a figure """

    @mpg.plotter()
    def main():
        fig = mpg.figure(title='Test')
        mpg.plot([1, 2, 3], [2, 3, 4])
        fig.close()

    main()
