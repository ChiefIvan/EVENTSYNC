import flet as ft
import numpy as np

from barcode import EAN13
from barcode.writer import ImageWriter
from requests import get, RequestException
from base64 import b64encode
from io import BytesIO

class User(ft.View):
    def __init__(self, page):
        super().__init__(route="/user", scroll=ft.ScrollMode.AUTO)

        self.page = page
        self.index = 0
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.token = self.page.client_storage.get("token")
        self.addr = "http://127.0.0.1:5000"

        def update_view(is_called_by_function=False):
            if self.index == 0:
                try:
                    request = get(
                        f"{self.addr}/views/get_user_info",
                        headers={
                            "Authorization": f"Bearer {self.token}"
                        }
                    )

                    
                    request.raise_for_status()
                    data = request.json()

                    if request.ok:
                        name.value = data["full_name"]
                        data = EAN13('123456789056', writer=ImageWriter())
                        io = BytesIO()  # Create an instance of BytesIO
                        data.write(io)   # Write to the BytesIO instance
                        barcode_base64 = b64encode(io.getvalue()).decode('utf-8') # Use io.getvalue()
                        code.src_base64 = barcode_base64


                except RequestException as err:
                    ...

                self.controls = [
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            user_img,
                            name,
                            privilege,
                            code
                        ]
                    )
                ]

                if is_called_by_function:
                    self.update()

            else:
                self.controls = [
                    ft.Row(
                        controls=[
                            ft.Text(value="Hello from Events")
                        ]
                    )
                ]

                self.update()

        def handle_nav_change(e):
            self.index = e.control.selected_index
            self.page.close(self.drawer)
            update_view(True)

        self.appbar = ft.AppBar(
            leading=ft.IconButton(
                ft.Icons.MENU, icon_color=ft.Colors.GREY_700, on_click=lambda _: self.page.open(
                    self.drawer)),
            leading_width=40,
            center_title=False,
            bgcolor="#52a3ff",
        )

        self.drawer = ft.NavigationDrawer(
            selected_index=self.index,
            on_change=handle_nav_change,
            controls=[
                ft.NavigationDrawerDestination(
                    label="My Profile",
                    icon=ft.Icons.PEOPLE_ALT_OUTLINED,
                    selected_icon=ft.Icon(ft.Icons.PEOPLE_ALT),
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.Icon(ft.Icons.EVENT_AVAILABLE_OUTLINED),
                    label="Events",
                    selected_icon=ft.Icons.EVENT_AVAILABLE,
                ),
            ],
        )

        user_img = ft.Image(src="../assets/img/user-icon.webp", width=250, height=250)
        name = ft.Text(size=20)
        privilege = ft.Text("User", text_align=ft.TextAlign.CENTER, size=10, italic=True)
        code = ft.Image(width=250, height=200)


        update_view()