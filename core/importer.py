from __future__ import absolute_import
from __future__ import print_function
import lib.colorprint
import lib.common


class Importer(object):
    def __int__(self):
        lib.colorprint.color().blue('[*] Importing Modules')

    def import_one(self):
        for __module_name in lib.common.MODULE_ONE_NAME_LIST:
            if __module_name == "getip":
                from module.phase_one import getip as __module_obj
            elif __module_name == "headers":
                from module.phase_one import headers as __module_obj
            elif __module_name == "sample_1":
                from module.phase_one import sample_1 as __module_obj
            elif __module_name == "timeout":
                from module.phase_one import timeout as __module_obj
            else:
                continue
            try:
                # __module_obj = __import__('module.phase_one.' + __module_name, fromlist=['*.py'])
                lib.common.MODULE_ONE_OBJ_DICT[__module_name] = __module_obj
                lib.common.ALIVE_LINE[__module_name] = 0
            except Exception as e:
                lib.colorprint.color().red(str(e))

    def import_two(self):
        for __module_name in lib.common.MODULE_NAME_LIST:
            if __module_name == "bakdown":
                from module.phase_two import bakdown as __module_obj
            elif __module_name == "djangodebug":
                from module.phase_two import djangodebug as __module_obj
            elif __module_name == "dnstransfer":
                from module.phase_two import dnstransfer as __module_obj
            elif __module_name == "geditdown":
                from module.phase_two import geditdown as __module_obj
            elif __module_name == "gitcheck":
                from module.phase_two import gitcheck as __module_obj
            elif __module_name == "hgcheck":
                from module.phase_two import hgcheck as __module_obj
            elif __module_name == "pathleak":
                from module.phase_two import pathleak as __module_obj
            elif __module_name == "sample_2":
                from module.phase_two import sample_2 as __module_obj
            elif __module_name == "sensi_dir":
                from module.phase_two import sensi_dir as __module_obj
            elif __module_name == "svncheck":
                from module.phase_two import svncheck as __module_obj
            elif __module_name == "vimdown":
                from module.phase_two import vimdown as __module_obj
            elif __module_name == "sensi_file":
                from module.phase_two import sensi_file as __module_obj
            else:
                continue
            print('*', __module_name.ljust(40, '.'), end=' ')
            try:
                # __module_obj = __import__('module.phase_two.' + __module_name, fromlist=['*.py'])
                lib.common.MODULE_OBJ_DICT[__module_name] = __module_obj
                lib.common.RESULT_DICT[__module_name] = []
                lib.common.ALIVE_LINE[__module_name] = 0
                __module_obj.init()
                lib.colorprint.color().green('SUCCESS')
            except Exception as e:
                lib.common.MODULE_NAME_LIST.remove(__module_name)
                lib.colorprint.color().red(str(e))
        print()

    def do_import(self):
        lib.colorprint.color().blue('[*] Importing Modules')
        self.import_one()
        self.import_two()
