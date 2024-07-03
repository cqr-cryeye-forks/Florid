from __future__ import absolute_import
from __future__ import print_function
import importlib.util
import os
import platform
import time

import lib.common

# from six.moves import input

NEEDED_MODULES = ['requests', 'bs4']


class Initializer:
    def __init__(self):
        self.__uninstalled_modules_list = list()

    def __os_init(self):
        lib.common.CONFIG['OS_type'] = 'WIN' if platform.system() == 'Windows' else 'NIX'

    def __time_init(self):
        lib.common.CONFIG['time:'] = time.localtime(time.time())

    def __modules_init(self):
        # Check if needed modules are installed
        for needed_module in NEEDED_MODULES:
            if not self.__is_module_installed(needed_module):
                self.__uninstalled_modules_list.append(needed_module)

        if self.__uninstalled_modules_list:
            print('[!] Some necessary modules are needed:')
            for needed_module in self.__uninstalled_modules_list:
                print(f'\t* {needed_module}')
            # Uncomment the following line if you want to prompt user input
            # input('Press [Enter] to install them.')
            for needed_module in self.__uninstalled_modules_list:
                os.system(f'pip install {needed_module}')

            self.__clear_screen()

    def __is_module_installed(self, module_name):
        spec = importlib.util.find_spec(module_name)
        return spec is not None

    def __clear_screen(self):
        if lib.common.CONFIG['OS_type'] == 'WIN':
            os.system('cls')
        else:
            os.system('clear')

    def init(self):
        self.__os_init()
        self.__time_init()
        self.__modules_init()
        return True


if __name__ == '__main__':
    init = Initializer().init()
