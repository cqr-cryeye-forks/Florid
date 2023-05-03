from __future__ import absolute_import
import threading

import lib.common
import lib.urlentity
from settings import ROOT_PATH

MODULE_NAME = 'sensi_file'


def init():
    lib.common.PUBLIC_STORAGE[MODULE_NAME] = []


def check(url_obj):
    url_obj.make_get_request()
    if url_obj.get_response() is not None:
        resp = url_obj.get_response()
        if resp.status_code != 404:
            lib.common.RESULT_DICT[MODULE_NAME].append(url_obj.get_url())


def run(url):
    tasks = list([])
    url_obj = lib.urlentity.URLEntity(raw_url=url)
    target_url = url_obj.get_source()
    target_url_list = list([target_url])

    if url_obj.is_file():
        path_section_list = [x for x in url_obj.get_path().split('/') if x != ''][:-1]
    else:
        path_section_list = [x for x in url_obj.get_path().split('/') if x != '']
    for path_section in path_section_list:
        target_url += (path_section + '/')
        target_url_list.append(target_url)

    file_path = ROOT_PATH.parent.joinpath("file_set.txt")
    fp = open(file_path, 'r')
    for __file in fp:
        if __file == '\n':
            continue
        for item in target_url_list:
            url_to_be_checked = item + __file.replace('\n', '')
            if url_to_be_checked not in lib.common.PUBLIC_STORAGE[MODULE_NAME]:
                lib.common.PUBLIC_STORAGE[MODULE_NAME].append(url_to_be_checked)
                tasks.append(threading.Thread(target=check, args=(lib.urlentity.URLEntity(url_to_be_checked),)))

    for t in tasks:
        t.setDaemon(True)
        t.start()
    for t in tasks:
        t.join()

    lib.common.ALIVE_LINE[MODULE_NAME] += 1
