import flet as ft

from components.login import Login
from components.signup import Signup


def main(page):
    page.title = "EventSync"
    page.description = "Nothing Special"
    page.fonts = {
        "Poppins": "/fonts/Poppins-Medium.ttf",
        "Poppins-Bold": "/fonts/Poppins-Bold.ttf"
    }

    page.theme = ft.Theme(color_scheme_seed="blue",
                          font_family="Poppins")
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def route_change(e):
        page.views.clear()

        page.views.append(
            ft.View(
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                route="/",
                controls=[
                    Login(page),
                ]
            )
        )

        if page.route == "/signup":
            page.views.append(
                ft.View(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    route="/signup",
                    controls=[
                        Signup(page)
                    ]
                )
            )

        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == "__main__":
    ft.app(main)
