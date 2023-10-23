from .robot import Robot
from .state import State
from .common import *
"""
imports do framework  ↑
imports do usuário    ↓
"""
from make_web_automation import Firefox
import time


@apply_decorator_to_all_methods(handle_exceptions)
class Performer(Robot):

    def __init__(self):
        super().__init__()
        self.current_state = State.PERFORMER

    def on_entry(self):
        print("VOU ESPERAR 5 SEGUNDOS")
        for i in [1, 2, 3, 4, 5]:
            time.sleep(1)
            print(i)
        self.browser = Firefox(download_directory='/home/seluser/temp',
                               headless=True)

    def execute(self):
        self.navigate_to_objective()
        delete_all_temp_files()

    def navigate_to_objective(self):

        self.browser.open('http://the-internet.herokuapp.com/')
        self.browser.click_by_link_text('File Download')
        # ← este objeto pode não estar no html, procure por outro arquivo.
        self.browser.click_by_link_text('sample.png')
        self.browser.close_all_firefox_processes()

    def on_exit(self):
        self.next_state = State.HANDLER

    def on_error(self):
        self.next_state = State.FINISHER
