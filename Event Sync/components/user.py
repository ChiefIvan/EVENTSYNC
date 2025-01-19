import flet as ft

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
        self.TOKEN = self.page.client_storage.get("token")
        self.addr = "http://127.0.0.1:5000"

        def handle_logout(e):
            try:
                # pr.visible = True
                self.page.snack_bar = ft.SnackBar(content=ft.Text(
                    value="Logging Out... Please wait!"),
                    action="Okay",
                )

                self.page.snack_bar.open = True
                self.page.update()

                response = get(
                    f"{self.addr}/views/logout",
                    headers={
                        "Authorization": f"Bearer {self.TOKEN}"
                    }
                )

                response.raise_for_status()

                self.page.client_storage.remove("token")
                self.page.go("/login")
                
            except RequestException as err:
                self.page.snack_bar = ft.SnackBar(content=ft.Text(
                    value="Server Unreachable, try again!"),
                    action="Okay",
                )

                self.page.snack_bar.open = True
                self.page.update()

        def update_view(is_called_by_function=False):
            if self.index == 0:
                try:
                    request = get(
                        f"{self.addr}/views/get_user_info",
                        headers={
                            "Authorization": f"Bearer {self.TOKEN}"
                        }
                    )

                    
                    data = request.json()

                    if not request.ok:
                        self.page.snack_bar = ft.SnackBar(content=ft.Text(
                            value="Something went wrong! try to refresh."),
                            action="Okay",
                        )

                        self.page.snack_bar.open = True
                        self.page.update()

                        return


                    name.value = data["full_name"]
                    email.value = data["email"]
                    institute.value = data["institute"]
                    program.value = data["program"]
                    bar_code.value = data["code"]
                    data = EAN13((data["code"]), writer=ImageWriter(), no_checksum=True)
                    io = BytesIO()
                    data.write(io)
                    barcode_base64 = b64encode(io.getvalue()).decode('utf-8')
                    code.src_base64 = barcode_base64


                except RequestException as err:
                    self.page.snack_bar = ft.SnackBar(content=ft.Text(
                        value="Server Unreachable, try again!"),
                        action="Okay",
                    )

                    self.page.snack_bar.open = True
                    self.page.update()

                self.controls = [
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            user_img,
                            name,
                            privilege,
                            ft.Divider(thickness=2),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text("Email"),
                                    email,
                                ]
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text("Institute"),
                                    institute,
                                ]
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text("Program"),
                                    program,
                                ]
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text("Code"),
                                    bar_code,
                                ]
                            ),
                            code,
                            ft.Divider(thickness=2),
                            ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.ElevatedButton("Logout", width=500, on_click=handle_logout),
                                ]
                            ),
                        ]
                    )
                ]

                if is_called_by_function:
                    self.update()

            else:
                lv = ft.ListView(
                    divider_thickness=1
                )

                try:
                    response = get(
                        f"{self.addr}/views/get_all_event",
                        headers={
                            "Authorization": f"Bearer {self.TOKEN}"
                        }
                    )

                    events = response.json()

                    if not response.ok:
                        self.page.snack_bar = ft.SnackBar(content=ft.Text(
                            value="Something went wrong! try to refresh."),
                            action="Okay",
                        )

                        self.page.snack_bar.open = True
                        self.page.update()

                        return

                    for event in events:
                        lv.controls.append(
                            ft.Container(
                                ink=True,
                                padding=20, 
                                content=ft.Column(
                                    controls=[
                                        ft.Text(value=event["event_name"],
                                                weight=ft.FontWeight.BOLD, size=20),
                                        ft.Text(value=event["event_description"],
                                                color=ft.Colors.GREY_500),
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            controls=[
                                                ft.Text(value=event["event_date"],
                                                        italic=True, color=ft.Colors.GREY_300, size=10),
                                                ft.Text(value=f"{event['event_start_time']} - {event['event_end_time']}",
                                                        italic=True, color=ft.Colors.GREY_300, size=10)
                                            ]
                                        ),
                                    ]
                                )
                            )
                        )

                except RequestException as err:
                    self.page.snack_bar = ft.SnackBar(content=ft.Text(
                        value="Server Unreachable, try again!"),
                        action="Okay",
                    )

                    self.page.snack_bar.open = True
                    self.page.update()
                finally:
                    # pr.visible = False
                    ...

                self.controls = [
                    lv
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
                 ft.Row(
                    controls=[
                        ft.Image(
                            src="icon.png",
                            width=60,
                            height=60,
                            fit=ft.ImageFit.CONTAIN,
                        ),
                        ft.Text("Event Sync")
                    ]
                ),
                ft.Divider(thickness=2),
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
        email = ft.Text()
        institute = ft.Text()
        program = ft.Text()
        bar_code = ft.Text()
        code = ft.Image(width=250, height=200)


        update_view()