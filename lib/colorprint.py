from __future__ import absolute_import
from . import common


def color():
    if common.CONFIG['OS_type'] == 'WIN':
        from . import __colorprint_win
        return __colorprint_win.ColorPrintWin()
    else:
        from . import __colorprint_nix
        return __colorprint_nix.ColorPrintNix()
