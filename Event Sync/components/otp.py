import flet as ft
from requests import post, RequestException

class Otp(ft.View):
    def __init__(self, page):
        super().__init__(route="/otp")

        self.page = page
        self.addr = "https://chiefban.pythonanywhere.com/"
        self.user_email = self.page.client_storage.get("email")

        def handle_submit(e):
            try:
                pr.visible = True
                button.visible = False
                self.update()

                request = post(
                            f"{self.addr}/auth/request_otp",
                            json={
                                "email": self.user_email,
                                "pin": text_field.value
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
                
                self.page.client_storage.set("token", data["token"])
                self.page.go("/login")

            except RequestException as err:
                self.page.snack_bar = ft.SnackBar(content=ft.Text(
                    value="Server Unreachable, try again!"),
                    action="Okay",
                )

                self.page.snack_bar.open = True
                self.page.update()
            finally:
                pr.visible = False
                button.visible = True

                self.update()

        text_field = ft.TextField(label="Enter a Pin", border_width="0", bgcolor="#03f8fc", border_radius=ft.border_radius.all(25))
        pr = ft.ProgressRing(width=32, height=32,
                             stroke_width=4, visible=False)
        button = ft.FilledButton(text="Submit", on_click=handle_submit,
                                 width="500", height="40")

        self.controls = [
            ft.Row(height=40),
            ft.Text("Please enter the pin sent from your email!", size="12", italic=True),
            text_field,
            button,
            pr
                
            
        ]