import flet as ft
import numpy as np

from datetime import datetime
from requests import post, get, delete, RequestException
from cv2 import (VideoCapture, cvtColor, QRCodeDetector, polylines, destroyAllWindows, imshow, waitKey, COLOR_BGR2GRAY, LINE_AA)

class Admin(ft.View):
    def __init__(self, page):
        super().__init__(route="/admin", scroll=ft.ScrollMode.AUTO)

        self.page = page
        self.index = 0
        self.addr = "http://127.0.0.1:5000"
        self.TOKEN = self.page.client_storage.get("token")

        if self.TOKEN is None:
            self.page.go("/login")

        def handle_item_click(event_id, event_name):
            self.page.client_storage.set("event_id", event_id)
            self.page.client_storage.set("event_name", event_name)

            cam = VideoCapture(0)
            while True:
                ret, frame = cam.read()
                if not ret:
                    break

                gray = cvtColor(frame, COLOR_BGR2GRAY)
                detector = QRCodeDetector()
                data, points, _ = detector.detectAndDecode(gray)

                if data:
                    polylines(frame, [np.int32(points)], True, (255, 0, 0), 2, LINE_AA)

                    print(f"QR Code: {data}")
                    
                    cam.release()
                    destroyAllWindows()
                    break

                imshow(event_name, frame)
                if waitKey(1) & 0xFF == ord("q"):
                    break

        def handle_mount():
            try:
                # pr.visible = True

                response = get(
                    f"{self.addr}/views/get_all_event",
                    headers={
                        "Authorization": f"Bearer {self.TOKEN}"
                    }
                )

                events = response.json()

                if not response.ok:
                    response.raise_for_status()
                    self.update()
                    return

                for event in events:
                    lv.controls.append(
                        ft.Container(
                        on_click=lambda e, event=event: handle_item_click(event["id"], event["event_name"]),
                        ink=True,
                        padding=20, 
                        content=ft.Column(
                            controls=[
                                ft.Text(value=event["event_name"],
                                        weight=ft.FontWeight.BOLD, size=20),
                                ft.Text(value=event["event_description"],
                                        color=ft.Colors.GREY_800, selectable=True),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Text(value=event["event_date"],
                                                italic=True, color=ft.Colors.GREY_600, size=10),
                                        ft.Text(value=f"{event['event_start_time']} - {event['event_end_time']}",
                                                italic=True, color=ft.Colors.GREY_600, size=10)
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
                                            on_click=handle_event_delete,
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
                    )

            except RequestException as err:
                ...
            finally:
                # pr.visible = False
                ...

        def update_view(is_called_by_function=False):
            if self.index == 0:
                self.controls = [
                    ft.Row(
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

        def handle_event_delete(e):
            row = e.control.parent
            column = row.control.parent

            text_control = column.controls[0]

            print(text_control.value)
            # try:
            #     request = delete(
            #         "http://127.0.0.1:5000/views/delete_event", json={})
            # except:
            #     ...


        def handle_add(e):
            try:
                # pr.visible = True

                response = post(f"{self.addr}/views/add_event",
                                json={
                                    "event_name": event_title.value,
                                    "event_description": description.value,
                                    "event_date": date_picker.value.strftime("%B %d, %Y"),
                                    "event_start_time": start_time_selection.value.strftime("%I:%M %p"),
                                    "event_end_time": end_time_selection.value.strftime("%I:%M %p"),
                                })

                data = response.json()

                if not response.ok:
                    response.raise_for_status()
                    self.update()
                    return

                handle_mount()

            except RequestException as err:
                ...
            finally:
                # pr.visible = False
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
                        ft.PopupMenuItem(content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            width=500,
                            controls=[
                                ft.Text(value="eventsync.admin@dorsu.edu.ph",
                                        color=ft.Colors.GREY_800),
                                ft.Text(value="Hello Admin!",
                                        weight=ft.FontWeight.BOLD, size=20, color=ft.Colors.GREY_800)
                            ]
                        ),
                            disabled=True,
                        ),
                    ]
                ),
            ],
        )

        self.floating_action_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD, on_click=lambda _: self.page.open(modal), bgcolor="#52a3ff")

        lv = ft.ListView(
            divider_thickness=1
        )

        event_title = ft.TextField(label="Event Title")
        description = ft.TextField(label="Description",
                                   multiline=True, max_lines=8)
        date_text = ft.Text(value="Select Date")
        start_time_text = ft.Text(value="Start Time")
        end_time_text = ft.Text(value="End Time")

        date_picker = ft.DatePicker(
            first_date=datetime(
                year=2024, month=10, day=31),
            last_date=datetime(
                year=2024, month=12, day=31),
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

    

