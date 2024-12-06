import flet as ft

from components.login import Login
from components.signup import Signup
from components.container import Dashboard


def main(page: ft.Page):
    page.scroll = ft.ScrollMode.AUTO
    page.title = "EventSync"
    page.description = "Nothing Special"
    page.route = "/dashboard"
    page.fonts = {
        "Poppins": "/fonts/Poppins-Medium.ttf",
        "Poppins-Bold": "/fonts/Poppins-Bold.ttf"
    }

    page.scroll = True

    page.theme = ft.Theme(color_scheme_seed="blue",
                          font_family="Poppins")
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def route_change(e):
        page.views.clear()

        if page.route == "/login":
            page.views.append(
                Login(page)
            )

        if page.route == "/signup":
            page.views.append(
                Signup(page)
            )

        if page.route == "/dashboard":
            page.views.append(
                Dashboard(page)
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
