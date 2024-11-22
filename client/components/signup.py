import flet as ft

from requests import post, RequestException


class Signup(ft.Column):
    def __init__(self, page):
        super().__init__()

        self.page = page
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.SPACE_EVENLY
        self.spacing = 50

        uname_field = ft.TextField(
            label="Username", suffix_text="@gmail.com", border_width="2", color="#6c6c6c")
        fname_field = ft.TextField(
            label="Fullname", border_width="2", color="#6c6c6c")
        s_id_field = ft.TextField(
            label="Student ID", suffix_text="Ex. 2020-2110", border_width="2", color="#6c6c6c")
        institute_dropdown = ft.Dropdown(
            label="Institute",
            width=500,
            border_width="2",
            tooltip="Choose your Institute",
            options=[
                ft.dropdown.Option(
                    "FCDSET"),
                ft.dropdown.Option("FTED"),
                ft.dropdown.Option("FNAHS"),
                ft.dropdown.Option("FGBM"),
            ],
        )
        program_dropdown = ft.Dropdown(
            label="Program",
            width=500,
            border_width="2",
            tooltip="Choose your Program",
            options=[
                ft.dropdown.Option(
                    "BS Information Technology"),
                ft.dropdown.Option("BS Mathematics"),
                ft.dropdown.Option("BS in Civil Engineering"),
                ft.dropdown.Option("BI Technology Management"),

            ],
        )
        password_field = ft.TextField(label="Password", password="True", can_reveal_password=True,
                                      border_width="2")
        cnfrm_password_field = ft.TextField(label="Password (Confirm)", password="True", can_reveal_password=True,
                                            border_width="2")

        def handle_signup(event):
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

                response = post("http://127.0.0.1:5000/auth/signup",
                                json={
                                    "uname": f"{uname_field.value}@gmail.com",
                                    "fname": fname_field.value,
                                    "s_id": s_id_field.value,
                                    "i_drp": institute_dropdown.value,
                                    "p_drp": program_dropdown.value,
                                    "psw": password_field.value,
                                    "pswcfrm": cnfrm_password_field.value
                                })
                response.raise_for_status()
                
                print(response.json())

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
                    fname_field,
                    s_id_field,
                    institute_dropdown,
                    program_dropdown,
                    password_field,
                    cnfrm_password_field,
                    ft.FilledButton(text="SIGNUP", on_click=handle_signup,
                                    width="500", height="40")
                ]
            ),
            ft.Row(
                spacing=5,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Text(value="Already have an Account?"),
                    ft.TextButton(
                        "Login",
                        on_click=lambda _: self.page.go("/")
                    )
                ]
            )
        ]
