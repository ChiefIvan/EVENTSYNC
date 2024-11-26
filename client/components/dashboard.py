import flet as ft

from requests import post, RequestException


class Dashboard(ft.Column):
    def __init__(self, page):
        super().__init__()
        self.page = page
