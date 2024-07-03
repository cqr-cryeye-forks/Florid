from __future__ import absolute_import, print_function

import os
from urllib.parse import urljoin
import bs4
import requests
import lib.colorprint
import lib.common
import lib.urlentity


class Producer:
    def __init__(self, source_url):
        self.__source_url_obj = lib.urlentity.URLEntity(source_url)
        self.waiting_list = [self.__source_url_obj.get_url()]
        self.crawled_list = [self.__source_url_obj.get_url()]
        self.results = []

        # Create the directory for log files such as the list of URLs
        log_dir = os.path.join(lib.common.CONFIG['project_path'], 'log', self.__source_url_obj.get_hostname())
        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
            except Exception as e:
                print('Creating Log File Failed:', e)

        self.log_fp = open(os.path.join(log_dir, 'urllist.txt'), 'w+')

    def __find_joint(self, soup, tags, attribute):
        """Finds new URLs from the given soup object and adds them to the waiting and crawled lists."""
        for tag in soup.find_all(tags):
            url_new = urljoin(self.__source_url_obj.get_url(), tag.get(attribute))
            url_new_obj = lib.urlentity.URLEntity(url_new)
            if (url_new_obj.get_url() not in self.crawled_list and
                    url_new_obj.get_hostname() == self.__source_url_obj.get_hostname() and
                    '#' not in url_new_obj.get_url()):
                self.waiting_list.append(url_new_obj.get_url())
                self.crawled_list.append(url_new_obj.get_url())

    def run(self):
        lib.colorprint.color().blue('[*] Scanning')
        while not lib.common.FLAG['producer_done']:
            if lib.common.FLAG['stop_signal']:
                break

            while self.waiting_list:
                if lib.common.FLAG['stop_signal']:
                    break

                current_url = self.waiting_list[0]
                print('\r+ ' + current_url)
                url_obj_to_be_checked = lib.urlentity.URLEntity(current_url)

                # Skip certain file types
                while url_obj_to_be_checked.get_file().lower().endswith(('png', 'jpg', 'bmp', 'gif')):
                    if self.waiting_list:
                        self.waiting_list.pop(0)
                    else:
                        break

                try:
                    response = requests.get(url=current_url)
                    soup = bs4.BeautifulSoup(response.text, 'html.parser')

                    # Save the current URL to results as a dictionary
                    self.results.append({"URL": current_url})

                except Exception as e:
                    print(f"Request failed for {current_url}: {e}")
                    self.waiting_list.pop(0)
                    continue

                lib.common.CHECKER_OBJ.queue_add(url=current_url)
                self.log_fp.write(current_url + '\n')
                self.waiting_list.pop(0)

                # Find new URLs from the current page
                self.__find_joint(soup, tags='a', attribute='href')
                self.__find_joint(soup, tags='form', attribute='action')
                self.__find_joint(soup, tags='link', attribute='href')

            lib.colorprint.color().yellow('[*] ' + str(lib.common.CHECKER_OBJ.get_total_length()) + ' URLs Found')
            lib.common.FLAG['producer_done'] = True

        self.log_fp.close()


if __name__ == '__main__':
    producer = Producer('http://testphp.vulnweb.com/')
    producer.run()
    # Print results
    print(producer.results)
