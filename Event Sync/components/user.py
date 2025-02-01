import flet as ft

from requests import get, post, RequestException
from base64 import b64encode

class User(ft.View):
    def __init__(self, page):
        super().__init__(scroll=ft.ScrollMode.HIDDEN, route="/user")

        self.page = page
        self.index = 0
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.TOKEN = self.page.client_storage.get("token")
        self.addr = "https://chiefban.pythonanywhere.com/"
        self.base64_string_img = ""

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

        def pick_files_result(e: ft.FilePickerResultEvent):
            if e.files:
                img_details = e.files[0]

                with open(img_details.path, "rb") as file:
                    img = file.read()

                base64_string = b64encode(img).decode('utf-8')

                user_img.src_base64 = base64_string
                self.base64_string_img = base64_string
                
                selected_img_name.value = img_details.name
                selected_img_name.visible = True

                cnfrm_btn.visible = True


                self.update()

        def handle_upload(e):
            selected_img_name.visible = False
            edit_btn.visible = False
            cnfrm_btn.visible = False
            pr.visible = True
            self.update()
            
            try:
                request = post(
                        f"{self.addr}/views/upl_prf",
                        headers={
                            "Authorization": f"Bearer {self.TOKEN}"
                        },
                        json={
                            "img": self.base64_string_img
                        }
                    )

                if not request.ok:
                    self.page.snack_bar = ft.SnackBar(content=ft.Text(
                        value="Something went wrong! try to refresh."),
                        action="Okay",
                    )

                    self.page.snack_bar.open = True
                    self.page.update()
                
            except RequestException as err:
                self.page.snack_bar = ft.SnackBar(content=ft.Text(
                    value="Server Unreachable, try again!"),
                    action="Okay",
                )

                self.page.snack_bar.open = True
                self.page.update()
            finally:
                edit_btn.visible = True
                pr.visible = False
                self.update()

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

                    if data["img"]:
                        user_img.src_base64 = data["img"]


                    name.value = data["full_name"]
                    email.value = data["email"]
                    s_id.value = data["s_id"]
                    institute.value = data["institute"]
                    program.value = data["program"]
                    bar_code.value = data["code"]
                    code.src_base64 = data["barcode"]

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
                            selected_img_name,
                            pick_files_dialog,
                            ft.Row(
                                height=40,
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    edit_btn,
                                    cnfrm_btn,
                                    pr
                                ]
                            ),
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
                                    ft.Text("Student ID"),
                                    s_id,
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
            

        pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
        selected_img_name = ft.Text(visible=False)

        pr = ft.ProgressRing(width=25, height=25,
                             stroke_width=4, visible=False)
        
        edit_btn = ft.IconButton(
            icon=ft.Icons.MODE_EDIT_OUTLINED,
            on_click=lambda _: pick_files_dialog.pick_files(allowed_extensions=["jpg", "jpeg", "webp"]))
        
        cnfrm_btn = ft.IconButton(
                icon=ft.Icons.CHECK_OUTLINED,
                on_click=handle_upload,
                visible=False, 
            )

        user_img = ft.Image(src="../assets/img/user-icon.webp", width=250, height=250, border_radius=ft.border_radius.all(1000))
        name = ft.Text(size=20)
        privilege = ft.Text("User", text_align=ft.TextAlign.CENTER, size=10, italic=True)
        email = ft.Text()
        s_id = ft.Text()
        institute = ft.Text()
        program = ft.Text()
        bar_code = ft.Text()
        code = ft.Image(src_base64="", width=250, height=200)


        update_view()