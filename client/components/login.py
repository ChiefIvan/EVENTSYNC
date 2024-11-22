import flet as ft

from requests import post, RequestException


class Login(ft.Column):
    def __init__(self, page):
        super().__init__()

        self.page = page
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.SPACE_EVENLY
        self.spacing = 50

        uname_field = ft.TextField(
            label="Username", suffix_text="@gmail.com", border_width="2", color="#6c6c6c")
        password_field = ft.TextField(label="Password", password="True", can_reveal_password=True,
                                      border_width="2")

        def handle_login(event):
            if len(uname_field.value) == 0:
                uname_field.border_color = "red"
                self.update()
                return

            if len(password_field.value) == 0:
                password_field.border_color = "red"
                self.update()
                return

            try:
                uname_field.disabled = True
                password_field.disabled = True

                response = post("http://127.0.0.1:5000/auth/login",
                                json={
                                    "uname": f"{uname_field.value}@gmail.com",
                                    "psw": password_field.value
                                })
                response.raise_for_status()

            except RequestException as err:
                print(err)
            finally:
                uname_field.disabled = False
                password_field.disabled = False
                self.update()

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
                    ft.FilledButton(text="LOGIN", on_click=handle_login,
                                    width="500", height="40")
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
