from pathlib import Path
import pytest
from playwright.sync_api import (
    sync_playwright
)
from utils.artifact_manager import (
    artifact_manager
)
from utils.config_reader import (
    load_config
)
from utils.logger import (
    get_logger
)


logger = get_logger()


REPORT_DIR = (
    Path(__file__)
    .resolve()
    .parent.parent
    / "reports"
)

VIDEO_DIR = (
    REPORT_DIR
    / "videos"
)

VIDEO_DIR.mkdir(
    parents=True,
    exist_ok=True
)


@pytest.fixture(scope="function")
def page(request):

    config = load_config()

    enable_video = (
        config["debug"]["video"]
    )

    enable_trace = (
        config["debug"]["trace"]
    )

    browser_channel = (
        config["browser"]["channel"]
    )

    headless = (
        config["browser"]["headless"]
    )

    device_name = (
        config["browser"]["device"]
    )

    logger.info(
        f"Starting Test: "
        f"{request.node.name}"
    )

    logger.info(
        f"Browser Channel: "
        f"{browser_channel}"
    )

    logger.info(
        f"Headless Mode: "
        f"{headless}"
    )

    logger.info(
        f"Device: "
        f"{device_name}"
    )

    with sync_playwright() as p:

        browser = p.chromium.launch(
            channel=browser_channel,
            headless=headless
        )

        device = p.devices[
            device_name
        ]

        context_options = {
            **device
        }

        # Video Recording
        if enable_video:

            context_options[
                "record_video_dir"
            ] = str(VIDEO_DIR)

            logger.info(
                "Video Recording Enabled"
            )

        context = browser.new_context(
            **context_options
        )

        # Trace Viewer
        if enable_trace:
            context.tracing.start(
                screenshots=True,
                snapshots=True,
                sources=True
            )

            logger.info(
                "Trace Recording Started"
            )

        page = context.new_page()

        yield page

        # Test Result
        test_failed = (
            hasattr(
                request.node,
                "rep_call"
            )
            and request.node.rep_call.failed
        )

        logger.info(
            f"Test Failed: "
            f"{test_failed}"
        )

        # Screenshot on Failure
        if test_failed:

            screenshot_path = (
                artifact_manager
                .screenshot_path(
                    request.node.name
                )
            )

            try:

                page.screenshot(
                    path=screenshot_path,
                    full_page=True
                )

                logger.info(
                    f"Screenshot Saved: "
                    f"{screenshot_path}"
                )

            except Exception as exc:

                logger.error(
                    f"Screenshot Error: "
                    f"{exc}"
                )

        # Trace on Failure
        if enable_trace:
            try:
                if test_failed:
                    trace_path = (
                        artifact_manager
                        .trace_path(
                            request.node.name
                        )
                    )
                    context.tracing.stop(
                        path=trace_path
                    )
                    logger.info(
                        f"Trace Saved: "
                        f"{trace_path}"
                    )
                else:
                    context.tracing.stop()
                    logger.info(
                        "Trace Discarded "
                        "(Test Passed)"
                    )

            except Exception as exc:
                logger.error(
                    f"Trace Error: "
                    f"{exc}"
                )

        # Save Video
        video = page.video

        # Close Context
        context.close()
        if enable_video and video:
            try:
                video_path = video.path()
                logger.info(
                    f"Video Saved: "
                    f"{video_path}"
                )

            except Exception as exc:

                logger.error(
                    f"Video Error: "
                    f"{exc}"
                )

        browser.close()

        logger.info(
            f"Finished Test: "
            f"{request.node.name}"
        )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
    item,
    call
):

    outcome = yield

    rep = outcome.get_result()

    setattr(
        item,
        f"rep_{rep.when}",
        rep
    )