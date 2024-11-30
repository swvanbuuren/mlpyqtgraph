""" Basic tests for mlpyqtgraph """

import mlpyqtgraph as mpg


def test_simple_plot():
    """ Test opening and closing a figure """

    @mpg.plotter
    def main():
        fig = mpg.figure(title='Test')
        mpg.plot([1, 2, 3], [2, 3, 4])
        fig.close()

    main()


def test_decorator_option():
    """ Test usage of decorator options """

    @mpg.plotter(line_color_profile='matplotlib')
    def main():
        fig = mpg.figure(title='Test')
        mpg.plot([1, 2, 3], [2, 3, 4])
        fig.close()

    main()
