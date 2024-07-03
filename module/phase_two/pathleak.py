from __future__ import absolute_import
import lib.common
import lib.urlentity

MODULE_NAME = 'pathleak'


def init():
    pass


def run(url):
    url_obj = lib.urlentity.URLEntity(raw_url=url)

    # Check if the URL points to a file
    if url_obj.is_file():
        query = url_obj.get_query()
        if query:
            query_list = query.split('&')
            for item_num in range(len(query_list)):
                tmp_query_list = query_list.copy()
                # Remove the value for the current query parameter
                tmp_query_list[item_num] = tmp_query_list[item_num].split('=')[0] + '='
                tmp_url = f"{url_obj.get_source()}{url_obj.get_file()}?{'&'.join(tmp_query_list)}"
                tmp_url_obj = lib.urlentity.URLEntity(raw_url=tmp_url)
                tmp_url_obj.make_get_request()
                html_text = tmp_url_obj.get_response().text.lower()
                if 'directory listing' in html_text:
                    lib.common.RESULT_DICT[MODULE_NAME].append(tmp_url)

    # Check if the URL points to a directory and contains 'directory listing' in the response
    elif 'directory listing' in url_obj.get_response().text.lower():
        lib.common.RESULT_DICT[MODULE_NAME].append(url)

    lib.common.ALIVE_LINE[MODULE_NAME] += 1
