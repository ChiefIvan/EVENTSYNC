import flet as ft

class Scan(ft.View):
    def __init__(self, page, data=None):
        super().__init__(route="/scan")
        self.page = page
        

        self.appbar =  ft.AppBar(
            leading=ft.IconButton(
                ft.Icons.ARROW_BACK, icon_color=ft.Colors.GREY_500, on_click=lambda _: self.page.go("/container")),
            title=ft.Text(self.page.client_storage.get('event_name')),
            center_title=True,
            bgcolor=ft.Colors.BROWN_900)
