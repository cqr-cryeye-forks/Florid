from __future__ import absolute_import, print_function
import json
import time

import config.config
import lib.colorprint
import lib.common
from settings import ROOT_PATH


class Checker:
    """A class to handle the URLs, works as a queue handler."""

    def __init__(self):
        self.url_queue = []
        self.count_elements = 0

    def queue_add(self, url):
        self.url_queue.append(url)
        self.count_elements += 1

    def queue_pop(self):
        url = self.url_queue.pop(0)
        return url

    def get_producer_state(self):
        return lib.common.FLAG['producer_done']

    def get_queue_length(self):
        return len(self.url_queue)

    def get_total_length(self):
        return self.count_elements


class ResultPrinter:
    FINAL_RESULT = {}

    def __init__(self):
        self.all_module_list = lib.common.MODULE_NAME_LIST
        self.phase_one_printed = False

    def run(self):

        while self.all_module_list:
            # Stop if configuration dictates exit without result and stop signal is set
            if config.config.config.get('exit_without_result') and lib.common.FLAG['stop_signal']:
                break
            # Wait until the producer's task is finished
            if lib.common.FLAG['producer_done']:
                print(222)
                time.sleep(0.06)
                # Print phase one results if not printed
                if not self.phase_one_printed:
                    one_finish_count = sum(
                        lib.common.ALIVE_LINE.get(module, 0) for module in lib.common.MODULE_ONE_NAME_LIST)
                    print(333)
                    time.sleep(0.06)
                    if one_finish_count == len(lib.common.MODULE_ONE_NAME_LIST):
                        self._print_phase_one_results()
                        self.phase_one_printed = True
                        print(444)
                        time.sleep(0.06)

                # Print phase two results
                if self.phase_one_printed:
                    self._print_phase_two_results()
                    print(555)
                    time.sleep(0.06)
        print(666)

        # Handle stop signal
        if lib.common.FLAG['stop_signal']:
            lib.colorprint.color().yellow('[!] User abort. Results may be incomplete.')

        # Save results to file
        self._save_results()

        lib.common.FLAG['scan_done'] = True

    def _print_phase_one_results(self):
        lib.colorprint.color().sky_blue('[====\t' + 'Site Info'.ljust(14) + '====]')
        Site_Info = lib.common.RESULT_ONE_DICT

        for key in ["Ip_Addr", "IP_Info", "X-Powered-By", "Server"]:
            Site_Info.setdefault(key, "Not defined")

        ResultPrinter.FINAL_RESULT["Site_Info"] = Site_Info

        longest_key = max(len(key) for key in Site_Info)
        for key, value in Site_Info.items():
            print((key + ': ').ljust(longest_key + 2) + value)
        print()

    def _print_phase_two_results(self):
        for module_name in self.all_module_list[:]:
            if lib.common.ALIVE_LINE.get(module_name, -1) >= 0:
                title = '[====\t' + module_name.ljust(14) + '====]'
                lib.colorprint.color().sky_blue(title)
                self.all_module_list.remove(module_name)

                context = lib.common.RESULT_DICT.get(module_name, [])
                ResultPrinter.FINAL_RESULT[module_name] = [{"file": file} for file in context]

                for item in context:
                    lib.colorprint.color().green('\t> ' + item)
                print()

    def _save_results(self):
        file_path = ROOT_PATH.joinpath("result.json")
        file_path.write_text(json.dumps(ResultPrinter.FINAL_RESULT, indent=4))
        lib.common.FLAG['scan_done'] = True
