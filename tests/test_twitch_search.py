import pytest
from pages.home_page import (
    HomePage
)
from pages.search_page import (
    SearchPage
)
from pages.streamer_page import (
    StreamerPage
)
from utils.config_reader import (
    load_config
)


@pytest.mark.smoke
@pytest.mark.flaky(reruns=2)
def test_twitch_streamer_flow(page):

    config = load_config()
    base_url = config["base_url"]
    home_page = HomePage(page)
    search_page = SearchPage(page)
    streamer_page = StreamerPage(page)

    home_page.open(base_url)
    streamer_page.handle_popup()
    home_page.click_search()

    search_page.search_game(config["search_name"])
    search_page.scroll_multiple(2)
    search_page.select_first_streamer()

    streamer_page.handle_popup()
    streamer_page.wait_video_loaded()
