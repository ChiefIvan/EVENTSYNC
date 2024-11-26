import flet as ft

from requests import post, RequestException


class Login(ft.Column):
    def __init__(self, page):
        super().__init__()

        self.page = page
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.SPACE_EVENLY
        self.spacing = 50

        if self.page.client_storage.get("token"):
            self.page.go("/dashboard")

        def handle_input(event):
            uname_field.border_color = None
            password_field.border_color = None
            self.update()

        def handle_login(event):
            if len(uname_field.value) == 0 or len(password_field.value) == 0:
                uname_field.border_color = "red"
                password_field.border_color = "red"
                self.update()
                return

            try:
                button.visible = False
                pr.visible = True
                uname_field.disabled = True
                password_field.disabled = True
                display_text.visible = False

                self.update()

                response = post("http://127.0.0.1:5000/auth/login",
                                json={
                                    "uname": f"{uname_field.value}@gmail.com",
                                    "psw": password_field.value
                                })

                data = response.json()

                if not response.ok:
                    display_text.value = data["msg"]
                    display_text.visible = True

                    response.raise_for_status()
                    self.update()
                    return

                self.page.client_storage.set("token", data["token"])
                self.page.go("/dashboard")

            except RequestException as err:
                ...
            finally:
                button.visible = True
                pr.visible = False
                uname_field.disabled = False
                password_field.disabled = False
                button.icon = None
                self.update()

        uname_field = ft.TextField(
            label="Username", suffix_text="@gmail.com", border_width="2", color="#6c6c6c", on_change=handle_input)
        password_field = ft.TextField(label="Password", password="True", can_reveal_password=True,
                                      border_width="2", on_change=handle_input)
        display_text = ft.Text(visible=False, color="red", size=13)
        button = ft.FilledButton(text="LOGIN", on_click=handle_login,
                                 width="500", height="40")
        pr = ft.ProgressRing(width=32, height=32,
                             stroke_width=4, visible=False)

        self.controls = [
            ft.Image(
                src="icon.png",
                width=100,
                height=100,
                fit=ft.ImageFit.CONTAIN,
            ),
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    uname_field,
                    password_field,
                    display_text,
                    button,
                    pr
                ]
            ),
            ft.Row(
                spacing=5,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Text(value="Don't have an Account?"),
                    ft.TextButton(
                        "Signup",
                        on_click=lambda _: self.page.go("/signup")
                    )
                ]
            )
        ]
