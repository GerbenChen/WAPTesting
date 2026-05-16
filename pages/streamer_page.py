from pages.base_page import BasePage


class StreamerPage(BasePage):

    POPUPS = [
        "button[data-a-target='ms-proceed-button']",
        "button[aria-label='Proceed']",
        "button[aria-label='Continue']",
        "button:has-text('Proceed')",
        "[data-test-selector='proceed-button']",
        "[data-a-target='consent-banner-accept']",
        "text='Proceed'",
        "button:has-text('Proceed')",
        "span:has-text('Proceed')",
        "div[role='button']:has-text('Proceed')",
        "div.consent-banner button",
        "div[role='dialog'] button:last-child",
        ".overlay-container button",
        "#root .video-player__overlay button"
    ]
    VIDEO = "video"

    def handle_popup(self):

        for popup in self.POPUPS:
            try:
                locator = (
                    self.page.locator(popup)
                )
                if locator.is_visible(timeout=1000):
                    locator.dispatch_event("click")

            except Exception:
                pass

    def wait_video_loaded(self):

        self.page.locator(
            self.VIDEO
        ).wait_for()

        self.wait(5000)