from pages.base_page import BasePage


class SearchPage(BasePage):

    SEARCH_INPUT = ("input[type='search']")

    STREAMER_SELECTORS = [
        # Twitch live preview card
        "a[data-a-id='preview-card-image-link']",
        # Fallback
        "article a",
        # Generic fallback
        "main a[href^='/']"
    ]

    def search_game(self, keyword: str):

        search_input = (
            self.page.locator(
                self.SEARCH_INPUT
            )
        )
        search_input.wait_for(state="visible")
        search_input.click()
        search_input.clear()
        search_input.press_sequentially(keyword, delay=150)
        self.wait(3000)
        self.select_first_suggestion(keyword)

    def select_first_suggestion(self, keyword: str):

        suggestion = (
            self.page.locator(
                f"a:has-text('{keyword}')"
            ).first
        )
        suggestion.wait_for()
        suggestion.click()
        self.wait(5000)

    def scroll_twice(self):

        self.scroll_down()
        self.wait(2000)
        self.scroll_down()
        self.wait(2000)

    def select_first_streamer(self):

        for selector in (self.STREAMER_SELECTORS):
            try:
                streamers = (
                    self.page.locator(
                        selector
                    )
                )
                count = streamers.count()
                for index in range(count):
                    streamer = (
                        streamers.nth(index)
                    )
                    try:

                        href = (
                            streamer.get_attribute("href")
                        )
                        if not href:
                            continue

                        # Skip invalid paths
                        invalid_keywords = [
                            "directory",
                            "search",
                            "login",
                            "signup",
                            "downloads"
                        ]

                        if any(
                            keyword in href
                            for keyword in invalid_keywords
                        ):
                            continue

                        if streamer.is_visible():
                            streamer.click()
                            self.wait(5000)
                            return

                    except Exception:
                        continue

            except Exception:
                continue

        raise AssertionError(
            "Streamer not found."
        )