import flet as ft

from requests import post, RequestException


class Signup(ft.View):
    def __init__(self, page):
        super().__init__(scroll=ft.ScrollMode.HIDDEN, route="/signup")

        self.page = page
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.spacing = 50
        self.dropdownOpt = {
            "FCDSET": [
                "BS Information Technology",
                "BS Mathematics",
                "BS in Civil Engineering",
                "BI Technology Management"
            ],
            "FNAHS": [
                "BS Nursing"
            ],
            "FGBM": [
                "BS Criminology",
                "BS Business Administration",
            ]
        }

        def handle_institute_dropdown(e):
            selected_institute = institute_dropdown.value
            program_options = self.dropdownOpt.get(selected_institute, [])
            program_dropdown.options = [ft.dropdown.Option(
                program) for program in program_options]
            self.update()

        def handle_signup(event):
            for field in [
                email_field.value,
                password_field.value,
                s_id_field.value,
                institute_dropdown.value,
                program_dropdown.value,
                password_field.value,
                cnfrm_password_field.value
            ]:
                if len(field) == 0:
                    email_field.border_color = "red"
                    fname_field.border_color = "red"
                    password_field.border_color = "red"
                    s_id_field.border_color = "red"
                    institute_dropdown.border_color = "red"
                    program_dropdown.border_color = "red"
                    password_field.border_color = "red"
                    cnfrm_password_field.border_color = "red"
                    self.update()
                    return

                # if email_field.value

            email_value = email_field.split("@")[0]

            try:
                pr.visible = True
                button.visible = False
                email_field.disabled = True
                fname_field.disabled = True
                password_field.disabled = True
                s_id_field.disabled = True
                institute_dropdown.disabled = True
                program_dropdown.disabled = True
                password_field.disabled = True
                cnfrm_password_field.disabled = True

                response = post("http://127.0.0.1:5000/auth/signup",
                                json={
                                    "email": f"{email_field.value}@gmail.com",
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
                pr.visible = False
                button.visible = True
                email_field.disabled = False
                fname_field.disabled = False
                password_field.disabled = False
                s_id_field.disabled = False
                institute_dropdown.disabled = False
                program_dropdown.disabled = False
                password_field.disabled = False
                cnfrm_password_field.disabled = False
                self.update()

        email_field = ft.TextField(
            label="Email", suffix_text="@gmail.com", border_width="1")
        fname_field = ft.TextField(
            label="Fullname", border_width="1")
        s_id_field = ft.TextField(
            label="Student ID", suffix_text="Ex. 2020-2110", border_width="1")
        institute_dropdown = ft.Dropdown(
            label="Institute",
            width=1000,
            border_width="1",
            tooltip="Choose your Institute",
            on_change=handle_institute_dropdown,
            options=[
                ft.dropdown.Option(
                    "FCDSET"),
                ft.dropdown.Option("FNAHS"),
                ft.dropdown.Option("FGBM"),
            ],
        )
        program_dropdown = ft.Dropdown(
            label="Program",
            width=1000,
            border_width="1",
            tooltip="Choose your Program",
        )
        password_field = ft.TextField(label="Password", password="True", can_reveal_password=True,
                                      border_width="1")
        cnfrm_password_field = ft.TextField(label="Password (Confirm)", password="True", can_reveal_password=True,
                                            border_width="1")
        button = ft.FilledButton(text="SIGNUP", on_click=handle_signup,
                                 width="500", height="40")
        pr = ft.ProgressRing(width=32, height=32,
                             stroke_width=4, visible=False)

        self.controls = [
            ft.Container(height=30),
            ft.Image(
                src="icon.png",
                width=100,
                height=100,
                fit=ft.ImageFit.CONTAIN,
            ),

            ft.Column(
                spacing=50,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        spacing=15,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(value="Sign Up",
                                    weight=ft.FontWeight.BOLD, size=30),
                            email_field,
                            fname_field,
                            s_id_field,
                            institute_dropdown,
                            program_dropdown,
                            password_field,
                            cnfrm_password_field,
                        ]
                    ),
                    button,
                    pr,
                    ft.Row(
                        spacing=5,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text(value="Already have an Account?"),
                            ft.TextButton(
                                "Login",
                                on_click=lambda _: self.page.go("/login")
                            )
                        ]
                    ),
                    ft.Container(height=30),

                ]
            )
        ]
