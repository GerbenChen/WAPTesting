from pages.base_page import BasePage


class HomePage(BasePage):

    SEARCH_TEXTS = [
        "Search",
        "搜尋",
        "瀏覽",
        "Browse"
    ]

    def open(self, url: str):

        self.page.goto(
            url,
            wait_until="domcontentloaded"
        )

        # Wait complete rendering
        self.page.wait_for_load_state(
            "networkidle"
        )

        self.page.wait_for_timeout(
            3000
        )

    def remove_popup(self):
        popup_selectors = [
            "button[aria-label='Close']",
            "[data-a-target='consent-banner-accept']"
        ]
        for selector in popup_selectors:
            try:
                popup = (
                    self.page
                    .locator(selector)
                    .first
                )
                if popup.is_visible():
                    popup.click()

            except Exception:
                pass

    def click_search(self):
        for text in self.SEARCH_TEXTS:
            try:
                link = self.page.get_by_role(
                    "link",
                    name=text
                )
                if link.first.is_visible():
                    link.first.click()
                    return
            except Exception:
                pass
            try:
                button = self.page.get_by_role(
                    "button",
                    name=text
                )
                if button.first.is_visible():
                    button.first.click()
                    return

            except Exception:
                pass

        raise AssertionError(
            "Search/Browse button not found."
        )