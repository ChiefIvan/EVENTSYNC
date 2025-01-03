import flet as ft

from requests import post, get, RequestException


class Login(ft.View):
    def __init__(self, page):
        super().__init__(route="/login")

        self.page = page
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.spacing = 50
        self.addr = "http://127.0.0.1:5000"
        self.token = self.page.client_storage.get("token")

        if self.token:
            try:
                request = get(
                    f"{self.addr}/views/get_privilege",
                    headers={
                        "Authorization": f"Bearer {self.token}"
                    }    
                )

                request.raise_for_status()

                data = request.json()
                print(data["privilege"])

                if int(data["privilege"]) == 1:
                    self.page.go("/admin")
                else:
                    self.page.go("/user")

            except RequestException as err:
                ...

        def handle_input(event):
            email_field.border_color = None
            password_field.border_color = None
            self.update()

        def handle_login(event):
            if len(email_field.value) == 0:
                email_field.border_color = "red"

            if len(password_field.value) == 0:
                password_field.border_color = "red"

                self.page.snack_bar = ft.SnackBar(content=ft.Text(
                    value="Please fill all entries!"),
                    action="Okay",
                )

                self.page.snack_bar.open = True
                self.page.update()

                return

            try:
                button.visible = False
                pr.visible = True
                email_field.disabled = True
                password_field.disabled = True

                self.update()

                request = post(f"{self.addr}/auth/login",
                                json={
                                    "email": email_field.value,
                                    "psw": password_field.value
                                })

                request.raise_for_status()
                
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
                print(data["privilege"])
                
                if int(data["privilege"]) == 1:
                    self.page.go("/admin")
                else:
                    self.page.go("/user")

            except RequestException as err:
                self.page.snack_bar = ft.SnackBar(content=ft.Text(
                    value="Server Unreachable, try again!"),
                    action="Okay",
                )

                self.page.snack_bar.open = True
                self.page.update()
            finally:
                button.visible = True
                pr.visible = False
                email_field.disabled = False
                password_field.disabled = False
                button.icon = None
                self.update()

        email_field = ft.TextField(
            label="Username", border_width="1", on_change=handle_input)
        password_field = ft.TextField(label="Password", password="True", can_reveal_password=True,
                                      border_width="1", on_change=handle_input)
        button = ft.FilledButton(text="LOGIN", on_click=handle_login,
                                 width="500", height="40")
        pr = ft.ProgressRing(width=32, height=32,
                             stroke_width=4, visible=False)

        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Hello, world!"),
            action="Alright!",
        )

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
                    email_field,
                    password_field,
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
