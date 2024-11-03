""" Module to determine nice ticklabels """

import math
import numpy as np


class NiceTicks:
    """ Determine nice ticklabels values """
    fractions = (1, 2, 5, 10)
    limit_fractions = ((1.5, 1), (3, 2), (7, 5))

    def __init__(self, minv, maxv, max_ticks=6):
        self.max_ticks = max_ticks
        self.tick_spacing = 0
        self.nice_min = 0
        self.nice_max = 0
        self.calculate_tick_params(minv, maxv)

    def calculate_tick_params(self, min_point, max_point):
        """ Calculate nice tick parameters """
        lst = self.nice_number(max_point - min_point, False)
        tick_spacing = self.nice_number(lst / (self.max_ticks - 1.0), True)
        self.tick_spacing = tick_spacing
        self.nice_min = tick_spacing*math.floor(min_point / tick_spacing)
        self.nice_max = tick_spacing*math.ceil(max_point / tick_spacing)

    def tick_values(self):
        """ Return nice tick values """
        return np.arange(
            self.nice_min,
            self.nice_max+self.tick_spacing,
            self.tick_spacing
        )

    def nice_fraction(self, fraction, rround):
        """ Return nice fraction """
        if (rround):
            return next(
                (f for limit, f in self.limit_fractions if fraction < limit),
                10
            )
        return next((f for f in self.fractions if fraction <= f), 10)

    def nice_number(self, value, rround):
        """ Return nice number """
        exponent = math.floor(math.log10(value))
        fraction = value / 10**exponent
        return self.nice_fraction(fraction, rround) * 10**exponent


def nice_ticks(data_min, data_max, num_ticks=6):
    """Calculate nice axis tick positions and labels. """
    nice_ticks = NiceTicks(data_min, data_max)
    return nice_ticks.tick_values()


def coord_limits(coord, limit_ratio=0.05):
    """ Define the grid points in the plain defined by axis=offset """
    limit_distance = limit_ratio*abs(coord[0]-coord[-1])
    limits = (coord[0] - limit_distance, coord[-1] + limit_distance)
    return limits


def coord_generator(num_ticks=6, **input_data):
    """Yield nice axis tick positions """
    for label, data in input_data.items():
        yield label, nice_ticks(np.min(data), np.max(data), num_ticks=6)


def limit_generator(limit_ratio=0.05, **coord_data):
    """Yield nice axis limits """
    for label, data in coord_data.items():
        yield label, coord_limits(data, limit_ratio=0.05)
