"""
The colors module defines classes to define colors

"""

import mlpyqtgraph.config_options as config


class ColorDefinitions:
    """ Provide color definitions """
    line_colors = {
        'matlab': (
            (  0, 113, 188),
            (216,  82,  24),
            (118, 171,  47),
            (236, 176,  31),
            (125,  46, 141),
            ( 76, 189, 237),
            (161,  19,  46),
            ( 63,  63,  63),
        ),
        'matplotlib': (
            (31,  119, 180),
            (255, 127,  14),
            ( 44, 160,  44),
            (214,  39,  40),
            (148, 103, 189),
            (140,  86,  75),
            (227, 119, 194),
            (127, 127, 127),
            (188, 189,  34),
            (23,  190, 207),
        ),
    }
    scale_box_colors = {
        'line': (175, 175, 175),
        'fill': (175, 175, 175, 50),
    }

    def get_line_colors(self):
        """ Returns list of line colors"""
        color_profile = config.options.get_option('line_color_profile')
        return self.line_colors.get(color_profile, 'matlab')

    def get_scale_box_colors(self, part='line'):
        """ Returns scale box colors"""
        return self.scale_box_colors[part]
