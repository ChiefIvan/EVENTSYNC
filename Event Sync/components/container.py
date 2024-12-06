import flet as ft

from requests import post, RequestException


class UserDashboard(ft.Row):
    def __init__(self):
        self.controls = [
            ft.Row(
                controls=[
                    ft.Text(value="Hello from Dashboard")
                ]
            )
        ]


class Dashboard(ft.View):
    def __init__(self, page):
        super().__init__(route="/dashboard", scroll=ft.ScrollMode.AUTO)
        self.page = page
        self.index = 0

        self.TOKEN = self.page.client_storage.get("token")

        if self.TOKEN is None:
            self.page.go("/login")

        def update_view(is_called_by_function=False):
            if self.index == 0:
                self.controls = [
                    ft.Container(height=1),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.Dropdown(
                                elevation=10,
                                label="Sort Month",
                                border_width=0,
                                width=140,
                                value="Default",
                                on_change=lambda _: print("Change"),
                                options=[
                                    ft.dropdown.Option(
                                        "October"),
                                    ft.dropdown.Option(
                                        "November"),
                                    ft.dropdown.Option(
                                        "December"),
                                    ft.dropdown.Option(
                                        "Default")
                                ]
                            ),
                        ]
                    ),
                    ft.Column(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            lv
                        ]
                    )
                ]

                if is_called_by_function:
                    self.update()

            else:
                self.controls = [
                    ft.Row(
                        controls=[
                            ft.Text(value="Hello from Users")
                        ]
                    )
                ]

                self.update()

        def handle_nav_change(e):
            self.index = e.control.selected_index
            page.close(self.drawer)
            update_view(True)

        def handle_add(e):
            for i in range(100):
                lv.controls.append(
                    ft.Column(
                        controls=[

                            ft.Text(value="FaCET Christmas Party",
                                    weight=ft.FontWeight.BOLD, size=20),
                            ft.Text(value="Sample Description",
                                    color=ft.Colors.GREY_800),
                            ft.Text(value="December 13, 2024",
                                    italic=True, color=ft.Colors.GREY_600, size=10),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.END,
                                spacing=0,
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_FOREVER_ROUNDED,
                                        icon_color="red",
                                        icon_size=25,
                                        tooltip="Delete record",
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT_DOCUMENT,
                                        icon_color="#52a3ff",
                                        icon_size=22,
                                        tooltip="Edit record",
                                    ),
                                ]
                            )
                        ]
                    )
                )
                self.update()

        self.drawer = ft.NavigationDrawer(
            selected_index=self.index,
            on_change=handle_nav_change,
            controls=[
                ft.NavigationDrawerDestination(
                    label="Dashboard",
                    icon=ft.Icons.DASHBOARD_CUSTOMIZE_OUTLINED,
                    selected_icon=ft.Icon(ft.Icons.DASHBOARD_CUSTOMIZE),
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.Icon(ft.Icons.PEOPLE_ALT_OUTLINED),
                    label="Users",
                    selected_icon=ft.Icons.PEOPLE_ALT,
                ),
            ],
        )

        self.appbar = ft.AppBar(
            leading=ft.IconButton(
                ft.Icons.MENU, icon_color=ft.Colors.GREY_700, on_click=lambda _: self.page.open(
                    self.drawer)),
            leading_width=40,
            center_title=False,
            bgcolor="#52a3ff",
            actions=[
                ft.PopupMenuButton(
                    icon_color=ft.Colors.GREY_700,
                    items=[
                        ft.PopupMenuItem(content=ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Image(
                                    src="../assets/img/user-icon.webp", width=250, height=250)
                            ],
                        ),
                            disabled=True
                        ),
                        ft.PopupMenuItem(),
                        ft.PopupMenuItem(
                            text="Checked item", checked=False
                        ),
                    ]
                ),
            ],
        )

        self.floating_action_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD, on_click=handle_add, bgcolor="#52a3ff")

        lv = ft.ListView(
            spacing=40,
        )

        update_view()
