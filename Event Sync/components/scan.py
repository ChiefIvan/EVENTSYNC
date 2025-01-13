import flet as ft

class Scan(ft.View):
    def __init__(self, page):
        super().__init__(route="/scan")
        self.page = page

        wv = ft.WebView(
            url="https://jocular-figolla-efd785.netlify.app/?token=1234567890",
            on_page_started=lambda _: print("Page started"),
            on_page_ended=lambda _: print("Page ended"),
            on_web_resource_error=lambda e: print("Page error:", e.data),
            expand=True,
        )

        self.page.add(wv)
        self.page.update()