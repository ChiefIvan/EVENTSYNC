import flet as ft

from base64 import b64encode

class SelectedUser(ft.View):
    def __init__(self, page):
        super().__init__(scroll=ft.ScrollMode.HIDDEN, route="/selected_user")
        self.page = page

        self.appbar = ft.AppBar(
            leading=ft.IconButton(
                ft.Icons.ARROW_BACK_OUTLINED, icon_color=ft.Colors.GREY_700, on_click=lambda _: self.page.go("/admin")),
            leading_width=40,
            center_title=False,
            bgcolor="#52a3ff",
        )

        user_img = ft.Image(src="../assets/img/user-icon.webp", width=250, height=250, border_radius=ft.border_radius.all(1000))
        name = ft.Text(self.page.client_storage.get("full_name") ,size=20)
        privilege = ft.Text("User", text_align=ft.TextAlign.CENTER, size=10, italic=True)
        email = ft.Text(self.page.client_storage.get("email"))
        institute = ft.Text(self.page.client_storage.get("institue"))
        program = ft.Text(self.page.client_storage.get("program"))
        bar_code = ft.Text(self.page.client_storage.get("code"))
        code = ft.Image(src_base64="", width=250, height=200)


        self.controls = [
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    user_img,
                    name,
                    privilege,
                    ft.Divider(thickness=2),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text("Email"),
                            email,
                        ]
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text("Institute"),
                            institute,
                        ]
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text("Program"),
                            program,
                        ]
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text("Code"),
                            bar_code,
                        ]
                    ),
                    code,
                ]
            )
        ]

        if isinstance(self.page.client_storage.get("img"), str):
            base64_string = b64encode(self.page.client_storage.get("img")).decode('utf-8')
            user_img.src_base64 = base64_string

        code.src_base64 = self.page.client_storage.get("barcode")