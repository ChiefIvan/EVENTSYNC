import flet as ft
from re import compile, search

from requests import post, RequestException


class Signup(ft.View):
    def __init__(self, page):
        super().__init__(scroll=ft.ScrollMode.HIDDEN, route="/signup")

        self.page = page
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.addr = "https://chiefban.pythonanywhere.com/"
        self.spacing = 50
        self.dropdownOpt = {
            "FaCET": [
                "BS Information Technology",
                "BS Mathematics",
                "BS in Civil Engineering",
                "BI Technology Management",
            ],
            "FNAHS": [
                "BS Nursing"
            ],
            "FBM": [
                "BS Business Administration",
                "BS Hospitality Management"
                ,
            ],
            "FCJE": [
                "BS Criminology",
            ],
            "FHUSOCOM": [
                "BS Psychology",
                "AB Political Science",
                "BS Development Communication",
            ],
            "FALS": [
                "BS Biology",
                "BS Agriculture",
                "BS Agribusiness Management",
                "BS Environmental Science",
            ],
            "FTED": [
                "Bachelor of Elementary Education",
                "Bachelor of Early Childhood Education",
                "Bachelor of Physical Education",
                "Bachelor of Special Needs Education",
                "BS-English",
                "BS-Mathematics",
                "BS-Filipino",
                "BS-Science",
                "Bachelor of Technology Livelihood Education",
            ],
        }

        def handle_email_change(e):
            value = email_field.value
            regex = compile(r"@")

            if search(regex, value):
                email_field.border_color = "red"
                email_msg.visible = True
                self.update()
                return True

            email_field.border_color = None
            email_msg.visible = False
            self.update()

        def handle_fname_change(e):
            if fname_field.value and len(fname_field.value) < 2:
                fname_field.border_color = "red"
                fname_msg.visible = True
                self.update()
                return True
            
            fname_field.border_color = None
            fname_msg.visible = False
            self.update()

        
        def handle_s_id_change(e):
            value = s_id_field.value
            regex = compile("^[0-9]{4}-[0-9]{4}$")

            if value and not search(regex, value):
                s_id_field.border_color = "red"
                s_id_msg.visible = True
                self.update()
                return True
            
            s_id_field.border_color = None
            s_id_msg.visible = False
            self.update()

        def handle_password_change(e):
            value = password_field.value
            regex = compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).*$")

            if value and not search(regex, value):
                password_field.border_color = "red"
                password_msg.visible = True
                self.update()
                return True
            
            password_field.border_color = None
            password_msg.visible = False
            self.update()

        def handle_cnfrm_password_change(e):
            if cnfrm_password_field.value and password_field.value != cnfrm_password_field.value:
                cnfrm_password_field.border_color = "red"
                cnfrm_password_msg.visible = True
                self.update()
                return True
            
            cnfrm_password_field.border_color = None
            cnfrm_password_msg.visible = False
            self.update()

        def handle_institute_dropdown(e):
            if institute_dropdown.border_color == "red":
                institute_dropdown.border_color = None

            selected_institute = institute_dropdown.value
            program_options = self.dropdownOpt.get(selected_institute, [])
            program_dropdown.options = [ft.dropdown.Option(
                program) for program in program_options]
            self.update()

        def handle_program_dropdown(e):
            if program_dropdown.border_color == "red":
                program_dropdown.border_color = None
                self.update()

        def handle_signup(event):
            index = 0
            
            for field in [
                email_field,
                fname_field,
                s_id_field,
                institute_dropdown,
                program_dropdown,
                password_field,
                cnfrm_password_field
            ]:
                if not field.value:
                    field.border_color = "red"
                    index += 1
                    self.update()

            if index > 1:
                return
            
            for entry_validation in [
                handle_email_change,
                handle_fname_change,
                handle_s_id_change,
                handle_password_change,
                handle_cnfrm_password_change,
            ]:
                if entry_validation(None):
                    return
                
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

                self.update()

                request = post(f"{self.addr}/auth/signup",
                                json={
                                    "email": f"{email_field.value}@gmail.com",
                                    "fname": fname_field.value,
                                    "s_id": s_id_field.value,
                                    "i_drp": institute_dropdown.value,
                                    "p_drp": program_dropdown.value,
                                    "psw": password_field.value,
                                    "pswcfrm": cnfrm_password_field.value
                                })

                response = request.json()

                if not request.ok:
                    self.page.snack_bar = ft.SnackBar(content=ft.Text(
                        value=response["msg"]),
                        action="Okay",
                    )

                    self.page.snack_bar.open = True
                    self.page.update()

                    return

                self.page.snack_bar = ft.SnackBar(content=ft.Text(
                    value="Please check your email for confirmation"),
                    action="Okay",
                )

                self.page.snack_bar.open = True
                self.page.update()

                self.page.client_storage.set("email", email_field.value)
                self.page.go("/otp")

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
                email_field.disabled = False
                fname_field.disabled = False
                password_field.disabled = False
                s_id_field.disabled = False
                institute_dropdown.disabled = False
                program_dropdown.disabled = False
                password_field.disabled = False
                cnfrm_password_field.disabled = False
                self.update()

        email_msg = ft.Text(value="Invalid Email, please dont include an extension!", visible=False, size=10, italic=True)
        fname_msg = ft.Text(value="Your fullname must be greater than 1 charater!", visible=False, size=10, italic=True)
        s_id_msg = ft.Text(value="Invalid ID format, valid sample ID: 1234-4567", visible=False, size=10, italic=True)
        password_msg = ft.Text(value="Password must contain 1 Uppercase, 1 Lowercase and a Number!", visible=False, size=10, italic=True)
        cnfrm_password_msg = ft.Text(value="Password and Password (Confirm) must be the same", visible=False, size=10, italic=True)

        email_field = ft.TextField(
            label="Email", suffix_text="@gmail.com", border_width="0", on_change=handle_email_change, color="#4c4c4c", bgcolor="#03f8fc", border_radius=ft.border_radius.all(100))
        fname_field = ft.TextField(
            label="Fullname", border_width="0", on_change=handle_fname_change, color="#4c4c4c", bgcolor="#03f8fc", border_radius=ft.border_radius.all(100))
        s_id_field = ft.TextField(
            label="Student ID", suffix_text="Ex. 2020-2110", border_width="0", on_change=handle_s_id_change, color="#4c4c4c", bgcolor="#03f8fc", border_radius=ft.border_radius.all(100))
        institute_dropdown = ft.Dropdown(
            label="Institute",
            width=1000,
            border_width="0",
            tooltip="Choose your Institute",
            on_change=handle_institute_dropdown,
            color="#4c4c4c",
            bgcolor="#03f8fc",
            border_radius=ft.border_radius.all(25),
            options=[
                ft.dropdown.Option(
                    "FaCET"),
                ft.dropdown.Option("FNAHS"),
                ft.dropdown.Option("FBM"),
                ft.dropdown.Option("FCJE"),
                ft.dropdown.Option("FHUSOCOM"),
                ft.dropdown.Option("FALS"),
                ft.dropdown.Option("FTED"),
            ],
        )
        program_dropdown = ft.Dropdown(
            label="Program",
            width=1000,
            border_width="0",
            color="#4c4c4c",
            bgcolor="#03f8fc",
            border_radius=ft.border_radius.all(25),
            on_change=handle_program_dropdown,
            tooltip="Choose your Program",
        )
        password_field = ft.TextField(label="Password", password="True", can_reveal_password=True,
                                      border_width="0", on_change=handle_password_change, color="#4c4c4c", bgcolor="#03f8fc", border_radius=ft.border_radius.all(100))
        cnfrm_password_field = ft.TextField(label="Password (Confirm)", password="True", can_reveal_password=True,
                                            border_width="0", on_change=handle_cnfrm_password_change, color="#4c4c4c", bgcolor="#03f8fc", border_radius=ft.border_radius.all(100))
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
                            email_msg,
                            fname_field,
                            fname_msg,
                            s_id_field,
                            s_id_msg,
                            institute_dropdown,
                            program_dropdown,
                            password_field,
                            password_msg,
                            cnfrm_password_field,
                            cnfrm_password_msg,
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
