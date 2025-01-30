import flet as ft
from requests import post, RequestException
from base64 import b64decode
from os import path

class Students(ft.View):
    def __init__(self, page):
        super().__init__(scroll=ft.ScrollMode.HIDDEN, route="/view_reg_users")
        self.page = page
        self.addr = "https://chiefban.pythonanywhere.com/"
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

                data = request.json()
                
                if len(data) == 0:
                    return

                lv.visible = True
                zero_user_msg.visible = False
                
                for user in data:
                    lv.controls.append(
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(user["full_name"]),
                                ft.Icon(name=ft.Icons.CHECK_OUTLINED),
                            ]
                        )
                    )

                self.update()
                

            except RequestException as err:
                self.page.snack_bar = ft.SnackBar(content=ft.Text(
                    value="Server Unreachable, try again!"),
                    action="Okay",
                )

                self.page.snack_bar.open = True
                self.page.update()

        def handle_generate(e):
            try:
                request = post(
                            f"{self.addr}/views/generate_pdf",
                            headers={
                                "Authorization": f"Bearer {self.TOKEN}"
                            },
                            json={
                                "id": self.page.client_storage.get("event_id")
                            }
                        )

                data = request.json()

                if not request.ok:
                    self.page.snack_bar = ft.SnackBar(content=ft.Text(
                        value=data["msg"]),
                        action="Okay",
                    )

                    self.page.snack_bar.open = True
                    self.page.update()

                    return

                base64_pdf = data["pdf_base64"]
                pdf_content = b64decode(base64_pdf)


                try:
                    with open(path.join("/storage/emulated/0/Documents", f"{data['filename']}.pdf") , "wb") as pdf_file:
                        pdf_file.write(pdf_content)
                except OSError as e:
                    self.page.snack_bar = ft.SnackBar(content=ft.Text(
                        value=f"Error saving PDF!: {e}"),
                        action="Okay",
                    )

                    self.page.snack_bar.open = True
                    self.page.update()
                except Exception as e:
                    self.page.snack_bar = ft.SnackBar(content=ft.Text(
                        value="An unexpected error occurred!: {e}"),
                        action="Okay",
                    )

                    self.page.snack_bar.open = True
                    self.page.update()

                self.page.snack_bar = ft.SnackBar(content=ft.Text(
                    value="PDF Saved Successfully!"),
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
                ...


            

        self.appbar = ft.AppBar(
            leading=ft.IconButton(
                ft.Icons.ARROW_BACK_OUTLINED, icon_color=ft.Colors.GREY_700, on_click=lambda _: self.page.go("/admin")),
            leading_width=40,
            center_title=False,
            bgcolor="#52a3ff",
        )

        self.floating_action_button = ft.FloatingActionButton(
            icon=ft.Icons.DOWNLOAD_OUTLINED, foreground_color=ft.Colors.GREY_300, on_click=handle_generate, bgcolor="#0a0033")


        lv = ft.ListView(divider_thickness=1, visible=False)
        zero_user_msg = ft.Text("No present students for this event!")

        self.controls=[
            lv, 
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    zero_user_msg
                ]
            )
        ]

        handle_mount()
        