import flet as ft

from datetime import datetime
from requests import post, get, RequestException

class Admin(ft.View):
    def __init__(self, page):
        super().__init__(scroll=ft.ScrollMode.HIDDEN, route="/admin")

        self.page = page
        self.index = 0
        self.addr = "https://chiefban.pythonanywhere.com/"
        self.TOKEN = self.page.client_storage.get("token")

        if self.TOKEN is None:
            self.page.go("/login")

        def handle_item_click(event_id, event_name):
            try:
                request = post(
                    "https://api.tinyurl.com/create",
                    headers={
                        "Authorization": "Bearer pQHnPuQimBNJONKbD1Th6I90r6wZem3HQJXZH7rEEZS1JGtylL6KcCMW5cRX",
                        "Content-Type": "application/json",
                    },
                    json={
                        "url": f"https://jocular-figolla-efd785.netlify.app/?id={event_id}&name={event_name}&token={self.TOKEN}",
                        "domain": "tiny.one",
                    }
                )

                data: dict = request.json()
                data_body = data.get("data")
                self.page.set_clipboard(data_body.get("tiny_url"))
                self.page.update()

            except RequestException as err:
                self.page.snack_bar = ft.SnackBar(content=ft.Text(
                    value="Server Unreachable, try again!"),
                    action="Okay",
                )

                self.page.snack_bar.open = True
                self.page.update()

            self.page.snack_bar = ft.SnackBar(content=ft.Text(
                    value="Scanner link copied to clipboard"),
                    action="Okay",
            )

            self.page.snack_bar.open = True
            self.page.update()

        def handle_view_user(event_id):
            self.page.client_storage.set("event_id", event_id)
            self.page.go("/view_reg_users")      

        def handle_mount():

            def handle_event_delete(e_id):
                try :
                    response = post(
                        f"{self.addr}/views/delete_event",
                        headers={
                            "Authorization": f"Bearer {self.TOKEN}"
                        },
                        json={
                            "id": e_id
                        }

                    )

                    if response.ok:
                        self.page.snack_bar = ft.SnackBar(content=ft.Text(
                        value="Event deleted Successfully!"),
                        action="Okay",
                    )

                    self.page.snack_bar.open = True
                    lv.visible = False
                    self.page.update()
                    handle_mount()

                except RequestException as err:
                    self.page.snack_bar = ft.SnackBar(content=ft.Text(
                        value="Server Unreachable, try again!"),
                        action="Okay",
                    )

                    self.page.snack_bar.open = True
                    self.page.update()

            try:
                pr.visible = True
                self.page.update()

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
                if len(events) != 0:
                    lv.visible = True
                    zero_count_msg.visible = False
                    self.page.update()

                    for event in events:
                        lv.controls.append(
                            ft.Container(
                                on_click=lambda e, event=event: handle_view_user(event["id"]),
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
                                                        italic=True, color=ft.Colors.GREY_500, size=10),
                                                ft.Text(value=f"{event['event_start_time']} - {event['event_end_time']}",
                                                        italic=True, color=ft.Colors.GREY_500, size=10)
                                            ]
                                        ),
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.END,
                                            spacing=0,
                                            controls=[
                                                ft.IconButton(
                                                    icon=ft.Icons.DELETE_FOREVER_ROUNDED,
                                                    icon_color="red",
                                                    icon_size=25,
                                                    tooltip="Delete record",
                                                    on_click=lambda _: handle_event_delete(event["id"]),
                                                ),
                                                ft.IconButton(
                                                    icon=ft.Icons.COPY_ALL_ROUNDED,
                                                    icon_color="#52a3ff",
                                                    icon_size=22,
                                                    tooltip="Copy Scanner Link",
                                                    on_click=lambda _: handle_item_click(event["id"], event["event_name"])
                                                ),
                                                
                                            ]
                                        )
                                    ]
                                )
                            )
                        )

                else:
                    zero_count_msg.visible = True
                    self.page.update()


            except RequestException as err:
                self.page.snack_bar = ft.SnackBar(content=ft.Text(
                    value="Server Unreachable, try again!"),
                    action="Okay",
                )

                self.page.snack_bar.open = True
                self.page.update()
            finally:
                pr.visible = False
                self.page.update()

        def handle_logout(e):
            try:
                # pr.visible = True
                self.page.snack_bar = ft.SnackBar(content=ft.Text(
                    value="Logging Out... Please wait!"),
                    action="Okay",
                )

                self.page.snack_bar.open = True
                self.page.update()

                get(
                    f"{self.addr}/views/logout",
                    headers={
                        "Authorization": f"Bearer {self.TOKEN}"
                    }
                )

                self.page.client_storage.remove("token")
                self.page.go("/login")
                
            except RequestException as err:
                self.page.snack_bar = ft.SnackBar(content=ft.Text(
                    value="Server Unreachable, try again!"),
                    action="Okay",
                )

                self.page.snack_bar.open = True
                self.page.update()

        def handle_selected_user(img, full_name, institue, program, privilege, code, barcode, s_id):
            if isinstance(img, str):
                self.page.client_storage.set("img", img)
            
            print(img)

            self.page.client_storage.set("full_name", full_name)
            self.page.client_storage.set("institue", institue)
            self.page.client_storage.set("program", program)
            self.page.client_storage.set("privilege", privilege)
            self.page.client_storage.set("code", code)
            self.page.client_storage.set("barcode", barcode)
            self.page.client_storage.set("s_id", s_id)

            self.page.go("/selected_user")

        def update_view(is_called_by_function=False):
            if self.index == 0:
                self.floating_action_button.visible = True

                self.controls = [
                    lv,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            zero_count_msg,
                            pr
                        ]
                    )
                ]


                if is_called_by_function:
                    self.page.update()

            else:
                self.floating_action_button.visible = False

                self.controls = [
                    user_lv,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            zero_count_msg_user,
                            user_pr
                        ]
                    )
                ]

                self.update()
                
                user_lv.clean()
                self.update()

                try:
                    response = get(
                        f"{self.addr}/views/get_all_users",
                        headers={
                            "Authorization": f"Bearer {self.TOKEN}"
                        }
                    )

                    if not response.ok:
                        self.page.snack_bar = ft.SnackBar(content=ft.Text(
                            value="Something went wrong! try to refresh."),
                            action="Okay",
                        )

                        self.page.snack_bar.open = True
                        self.page.update()

                        return
                    
                    users = response.json()

                    if len(users) != 0:
                        user_lv.visible = True
                        zero_count_msg_user.visible = False
                        self.update()

                        for user in users:
                            user_lv.controls.append(
                                ft.Container(
                                    on_click=lambda e, user=user: handle_selected_user(user["img"], user["full_name"], user["institute"], user["program"], user["privilege"], user["code"], user["barcode"], user["s_id"]),
                                    ink=True,
                                    padding=10,
                                    content=ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Row(
                                                controls=[
                                                    ft.Image(src_base64=user["img"], src="../assets/img/user-icon.webp", width=70, height=70, border_radius=ft.border_radius.all(1000)),
                                            ft.Text(user["full_name"], size=12)
                                                ]
                                            ),
                                            ft.Text(user["s_id"], size=13)
                                        ]
                                    )
                                )
                            )

                    else:
                        zero_count_msg_user.visible = True

                    self.update()



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
                

        def handle_nav_change(e):
            self.index = e.control.selected_index
            self.page.close(self.drawer)
            update_view(True)

        def handle_date(e):
            date_text.value = date_picker.value.strftime("%Y-%m-%d")
            self.page.update()

        def handle_start_time(e):
            start_time_text.value = start_time_selection.value
            self.page.update()

        def handle_end_time(e):
            end_time_text.value = end_time_selection.value
            self.page.update()


        def handle_add(e):
            try:
                if len(event_title.value) > 50:
                    self.page.snack_bar = ft.SnackBar(content=ft.Text(
                        value="Event Title must not exceed 50 characters!"),
                        action="Okay",
                    )

                    self.page.snack_bar.open = True
                    self.page.update()
                    
                    return

                if len(description.value) >= 200:
                    self.page.snack_bar = ft.SnackBar(content=ft.Text(
                        value="Description must not exceed 200 characters!"),
                        action="Okay",
                    )

                    self.page.snack_bar.open = True
                    self.page.update()

                    return

                response = post(
                    f"{self.addr}/views/add_event",
                    json={
                        "event_name": event_title.value,
                        "event_description": description.value,
                        "event_date": date_picker.value.strftime("%B %d, %Y"),
                        "event_start_time": start_time_selection.value.strftime("%I:%M %p"),
                        "event_end_time": end_time_selection.value.strftime("%I:%M %p"),
                    },
                    headers={
                        "Authorization": f"Bearer {self.TOKEN}"
                    }
                )

                if not response.ok:
                    self.page.snack_bar = ft.SnackBar(content=ft.Text(
                        value="Something went wrong! try to refresh."),
                        action="Okay",
                    )

                    self.page.snack_bar.open = True
                    self.page.update()

                    return

                lv.clean()
                handle_mount()
                self.page.close(modal)
                self.update()

            except RequestException as err:
                self.page.snack_bar = ft.SnackBar(content=ft.Text(
                    value="Server Unreachable, try again!"),
                    action="Okay",
                )

                self.page.snack_bar.open = True
                self.page.update()
                
            finally:
                event_title.value = ""
                description.value = ""
                date_text.value = "Select Date"
                start_time_text.value = "Start Time"
                end_time_text.value = "End Time"
                self.update()

        def handle_modal_close(e):
            self.page.close(modal)
            event_title.value = ""
            description.value = ""
            date_text.value = "Select Date"
            start_time_text.value = "Start Time"
            end_time_text.value = "End Time"
            self.update()

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
                    label="Dashboard",
                    icon=ft.Icons.DASHBOARD_CUSTOMIZE_OUTLINED,
                    selected_icon=ft.Icon(ft.Icons.DASHBOARD_CUSTOMIZE),
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.Icon(ft.Icons.PEOPLE_ALT_OUTLINED),
                    label="Students",
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
                        ft.PopupMenuItem(
                            disabled=True,
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Image(
                                        src="../assets/img/user-icon.webp", width=250, height=250)
                                ],
                            ),
                        ),
                        ft.PopupMenuItem(
                            disabled=True,
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                width=500,
                                controls=[
                                    ft.Column(
                                        height=100,
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            ft.Text(value="eventsync.admin@dorsu.edu.ph",
                                            color=ft.Colors.GREY_500),
                                            ft.Text(value="Hello Admin!",
                                            weight=ft.FontWeight.BOLD, size=20, color="#4c4c4c",)
                                        ]
                                    )
                                ]
                            ),
                        ),
                        ft.PopupMenuItem(
                            disabled=True,
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.ElevatedButton("Logout", width=500, on_click=handle_logout),
                                ]
                            ),
                        ),
                    ]
                ),
            ],
        )

        self.floating_action_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD, on_click=lambda _: self.page.open(modal), bgcolor="#52a3ff")

        lv = ft.ListView(
            divider_thickness=1,
            visible=False
        )

        user_lv = ft.ListView(
            divider_thickness=2,
            visible=False
        )

        pr = ft.ProgressRing(width=32, height=32,
                             stroke_width=4, visible=False)

        user_pr = ft.ProgressRing(width=32, height=32,
                             stroke_width=4, visible=False)
        
        zero_count_msg = ft.Text(value="No Event's Yet!", visible=False)
        zero_count_msg_user = ft.Text(value="No User's Yet!", visible=False)

        event_title = ft.TextField(label="Event Title", border_width="0", color="#4c4c4c", bgcolor="#03f8fc", border_radius=ft.border_radius.all(25))
        description = ft.TextField(label="Subject",
                                   color="#4c4c4c", border_width="0", bgcolor="#03f8fc", border_radius=ft.border_radius.all(25),
                                   multiline=True, max_lines=8)
        date_text = ft.Text(value="Select Date")
        start_time_text = ft.Text(value="Start Time")
        end_time_text = ft.Text(value="End Time")

        date_picker = ft.DatePicker(
            first_date=datetime(
                year=2025, month=1, day=1),
            last_date=datetime(
                year=2025, month=12, day=31),
            on_change=handle_date,
        )

        start_time_selection = ft.TimePicker(
            confirm_text="Confirm",
            error_invalid_text="Time out of range",
            help_text="Pick Event Start Time",
            on_change=handle_start_time,
        )

        end_time_selection = ft.TimePicker(
            confirm_text="Confirm",
            error_invalid_text="Time out of range",
            help_text="Pick Event End Time",
            on_change=handle_end_time,
        )

        modal = ft.AlertDialog(
            title=ft.Text("Add Event", weight=ft.FontWeight.BOLD),
            modal=True,
            content=ft.Column(
                width=500,
                controls=[
                    event_title,
                    description,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            date_text,
                            ft.ElevatedButton(
                                "Pick Date",
                                icon=ft.Icons.CALENDAR_MONTH,
                                on_click=lambda e: self.page.open(
                                    date_picker
                                ),
                            )
                        ]
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            start_time_text,
                            ft.ElevatedButton(
                                "Pick Time",
                                icon=ft.Icons.LOCK_CLOCK,
                                on_click=lambda e: page.open(
                                    start_time_selection
                                ),
                            )
                        ]
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            end_time_text,
                            ft.ElevatedButton(
                                "Pick Time",
                                icon=ft.Icons.LOCK_CLOCK,
                                on_click=lambda e: page.open(
                                    end_time_selection
                                ),
                            )
                        ]
                    )
                ]
            ),

            actions=[
                ft.ElevatedButton(
                    text="Add", on_click=handle_add),
                ft.ElevatedButton(
                    text="Cancel", on_click=handle_modal_close)

            ]
        )

        update_view()
        handle_mount()

    

