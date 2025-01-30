import flet as ft

class SelectedUser(ft.View):
    def __init__(self, page):
        super().__init__(scroll=ft.ScrollMode.HIDDEN, route="/selected_user")
        self.page = page