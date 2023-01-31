"""
The configuration options module defines tools to acquire and change global
configuration options
"""

import pyqtgraph as pg


class ConfigOptions:
    """
    Holds global configuration options and offers the possibility to changes
    them
    """
    config_options = {
        'line_color_profile': 'matlab',
        'antialiasing': True,
        'segmentedLineMode': 'off',
        'no_segmented_line_mode': False,
        'black_on_white': True,
    }
    def __init__(self, **kwargs):
        self.set_options(**kwargs)

    def set_options(self, **kwargs):
        """ Change one or more global configuration options """
        self.config_options = dict(self.config_options, **kwargs)
        self.enable_pg_options()

    def enable_pg_options(self):
        """ Activate pyqtgraph options """
        pg.setConfigOption('background', 'k')
        pg.setConfigOption('foreground', 'w')
        if self.config_options['black_on_white']:
            pg.setConfigOption('background', 'w')
            pg.setConfigOption('foreground', 'k')
        pg.setConfigOptions(antialias=self.config_options['antialiasing'])
        self.config_options['no_segmented_line_mode'] = False
        try:
            pg.setConfigOption('segmentedLineMode',
                               self.config_options['segmentedLineMode'])
        except KeyError:
            self.config_options['no_segmented_line_mode'] = True

    def get_option(self, option):
        """ Obtain or more global configuration options """
        return self.config_options[option]


options = ConfigOptions()
