import flet as ft
from requests import post, RequestException

class Students(ft.View):
    def __init__(self, page):
        super().__init__(route="/view_reg_users")
        self.page = page
        self.addr = "http://127.0.0.1:5000"
        self.TOKEN = self.page.client_storage.get("token")

        def handle_mount():
            try:
                request = post(
                        f"{self.addr}/views/get_all_reg_users",
                        headers={
                            "Authorization": f"Bearer {self.TOKEN}"
                        },
                        json={
                            "event_id": self.page.client_storage.get("event_id")
                        }
                    )
                
                if not request.ok:
                    self.page.snack_bar = ft.SnackBar(content=ft.Text(
                        value="Something went wrong! try to refresh."),
                        action="Okay",
                    )

                    self.page.snack_bar.open = True
                    self.page.update()

                    return

                response = request.json()
                
                if len(response) != 0:
                    for user in response:
                        lv.controls.append(
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(user["full_name"]),
                                    ft.Icon(name=ft.Icons.CHECK_OUTLINED),
                                ]
                            )
                        )

            except RequestException as err:
                self.page.snack_bar = ft.SnackBar(content=ft.Text(
                    value="Server Unreachable, try again!"),
                    action="Okay",
                )

                self.page.snack_bar.open = True
                self.page.update()

        self.appbar = ft.AppBar(
            leading=ft.IconButton(
                ft.Icons.ARROW_BACK_OUTLINED, icon_color=ft.Colors.GREY_700, on_click=lambda _: self.page.go("/admin")),
            leading_width=40,
            center_title=False,
            bgcolor="#52a3ff",
        )

        lv = ft.ListView(divider_thickness=1)

        self.controls=[lv]

        handle_mount()
        