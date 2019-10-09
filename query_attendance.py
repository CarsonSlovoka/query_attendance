"""
prepared:
    1. chromedriver.exe: download from https://chromedriver.chromium.org/downloads
    #. put ``chromedriver.exe`` to {executable}/Scripts/

USAGE::
    employee_id_1234 password --action=1 --debug=0
"""
from os.path import abspath, dirname
from os import path, startfile
from time import sleep
from sys import executable

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException

from pandas import DataFrame
from enum import Enum

from argparse import ArgumentParser
from configparser import ConfigParser, ExtendedInterpolation

try:
    import colorama
    from colorama import Fore, Back
    colorama.init(autoreset=True)
except ImportError as _e:
    colorama = _e

BACKGROUND_MODE = True


class URL:
    __slots__ = []
    EMPLOYEE = ""


class Action(Enum):
    __slots__ = []
    QUERY_ATTENDANCE = 1


def highlight_print(msg: str) -> None:
    if isinstance(colorama, ImportError):
        print(msg)
    else:
        print(Back.LIGHTYELLOW_EX + Fore.RED + msg)


def main(args):
    try:
        args.action = Action(args.action)
    except ValueError:
        highlight_print(f'ERROR. wrong action number: {args.action}') if args.debug else None
        return

    dict_run = {Action.QUERY_ATTENDANCE: lambda web_driver: query_attendance(web_driver), }

    try:
        web = login(args.url, args.username, args.password)
    except UnexpectedAlertPresentException as e:
        highlight_print(f'ERROR. MSG:{e.alert_text}') if args.debug else None
        return
    dict_run[args.action](web)


def login(url, username, password):
    global BACKGROUND_MODE
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_experimental_option("detach", True)  # It still exists when the program ends.
    chrome_options.add_argument("--start-maximized") if not BACKGROUND_MODE else None
    chrome_options.add_argument("headless") if BACKGROUND_MODE else None
    # chrome_options.add_argument('window-size=2560,1440')
    chrome_driver_exe_path = abspath(abspath(path.join(dirname(executable), r'Scripts\chromedriver.exe')))
    assert path.exists(chrome_driver_exe_path), 'chromedriver.exe not found!'
    web = webdriver.Chrome(executable_path=chrome_driver_exe_path, options=chrome_options)
    web.set_window_position(-9999, 0) if not BACKGROUND_MODE else None
    web.implicitly_wait(3)  # global setting ``maximum wait time``
    web.get(url)
    try:
        entry_username = web.find_element_by_name('username')
        entry_password = web.find_element_by_name('password')
    except NoSuchElementException:  # has been login before.
        print('NoSuchElementException: identifierId')
        web.maximize_window() if not BACKGROUND_MODE else None
        return

    entry_username.send_keys(username)
    entry_password.send_keys(password)
    btn_commit = web.find_element_by_name('imageField')
    # btn_commit.click()
    webdriver.ActionChains(web).move_to_element(btn_commit).click(btn_commit).perform()
    sleep(2)
    web.maximize_window()
    return web


def query_attendance(web):
    page_root = web.window_handles[0]  # This means the original page that will be empty after logging
    page_home = web.window_handles[1]
    web.switch_to.window(page_home)

    if '個人專區':
        personal_area = web.find_element_by_css_selector('#T_PM000600')
        personal_area.click()
        label_query_attendance = web.find_element_by_xpath('//*[@id="mtDropDown5"]/div/div[2]/div/table/tbody/tr[2]/td[1]')
        label_query_attendance.click()

        if '異常回報':
            error_report = web.find_element_by_xpath('//*[@id="mtDropDown6"]/div/div[2]/div/table/tbody/tr[4]/td[1]')
            webdriver.ActionChains(web).move_to_element(error_report).click(error_report).perform()

    if 'Enter Query Page...':
        web.switch_to.frame('frmMAIN')
        select_begin_month = Select(web.find_element_by_name("selM_A"))

        if 'select pre-month':
            begin_month_value = int(select_begin_month.first_selected_option.text)
            if begin_month_value == 1:  # change year
                input_year = web.find_element_by_name('txtY_A')
                begin_year = int(input_year.get_attribute('value')) - 1
                input_year.clear()
                input_year.send_keys(str(begin_year))
            begin_month_value = begin_month_value - 1 if begin_month_value != 1 else 12
            select_begin_month.select_by_value(str(begin_month_value))

            if 'commit':
                Select(web.find_element_by_name("sltDataType")).select_by_visible_text("異常刷卡資料")  # or 全部刷卡資料
                go_btn = web.find_element_by_xpath('/html/body/form/table/tbody/tr/td[2]/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[3]/table/tbody/tr[2]/td[3]')
                go_btn.click()

        if 'select last page':
            web.switch_to.frame('mainFrame')

            select_page = Select(web.find_element_by_name('selPage'))
            n_last_page = len(select_page.options)
            select_page.select_by_visible_text(str(n_last_page))

        if 'get report':
            web.switch_to.default_content()
            web.switch_to.frame('frmMAIN')
            web.switch_to.frame('mainFrame')
            """
            Important!
                The error of "element is not attached to the page document" still happened even the elements you obviously can found.
                That is because the page was changed.
                so you need reload it again. (switch_to)
            """
            tbody = web.find_element_by_xpath('/html/body/form/table[1]/tbody')  # https://stackoverflow.com/questions/24795198/get-all-child-elements
            list_rows = [[cell.text for cell in row.find_elements_by_tag_name('td')] for row in tbody.find_elements_by_tag_name('tr')]
            columns_title = list_rows[0]
            list_rows = list_rows[1:]  # max data count: 17

            list_rows = [e for e in list_rows if not all(data == ' ' for data in e)]
            df = DataFrame(list_rows, columns=columns_title)
            df.sort_values(['應刷卡時段'], ascending=[False], inplace=True)
            df.to_csv('temp.txt', index=False)
            startfile('temp.txt')


if __name__ == '__main__':
    highlight_print(f'{executable}')
    config = ConfigParser(interpolation=ExtendedInterpolation())
    read_result = config.read(['config.ini'], encoding='utf-8')
    arg_parser = ArgumentParser()
    if len(read_result) == 0:  # file exists
        arg_parser.add_argument("username", help="username")
        arg_parser.add_argument("password", help="password")
        arg_parser.add_argument("URL", dest='URL', help="URL")
        arg_parser.add_argument("--action", help="action", dest="action", default=None)
        arg_parser.add_argument("--debug", help="debug", dest="debug", default=False)
    else:
        arg_parser.add_argument("--username", help="username", dest='username', default=config['Required']['username'])
        arg_parser.add_argument("--password", help="password", dest='password', default=config['Required']['password'])
        arg_parser.add_argument("--URL", help='URL', dest='url', default=config['Required']['URL'])
        arg_parser.add_argument("--action", help="action", dest="action", default=config['Option']['action'])
        arg_parser.add_argument("--debug", help="debug", dest="debug", default=config['Option']['debug'])

    g_args = arg_parser.parse_args()
    g_args.debug = int(g_args.debug)
    g_args.action = int(g_args.action)
    main(g_args)
