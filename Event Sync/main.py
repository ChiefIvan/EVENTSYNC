import flet as ft

from components.login import Login
from components.signup import Signup
from components.admin import Admin
from components.user import User
from components.otp import Otp
from components.students import Students
from components.selected_user import SelectedUser

def main(page: ft.Page):
    page.window.width = 400
    page.scroll = ft.ScrollMode.HIDDEN
    page.title = "EventSync"
    page.description = "Nothing Special"
    page.route = "/login"
    page.theme_mode = "light"
    page.fonts = {
        "Poppins": "/fonts/Poppins-Medium.ttf",
        "Poppins-Bold": "/fonts/Poppins-Bold.ttf"
    }

    page.scroll = True
    page.theme = ft.Theme(color_scheme_seed="blue",
                          font_family="Poppins")

    def route_change(e):
        page.views.clear()

        if page.route == "/login":
            page.views.append(
                Login(page)
            )

        if page.route == "/otp":
            page.views.append(
                Otp(page)
        )
            

        if page.route == "/selected_user":
            page.views.append(
                SelectedUser(page)
        )   
        

        if page.route == "/signup":
            page.views.append(
                Signup(page)
            )

        if page.route == "/admin":
            page.views.append(
                Admin(page)
            )

        if page.route == "/view_reg_users":
            page.views.append(
                Students(page)
        )

        if page.route == "/user":
            page.views.append(
                User(page)
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
