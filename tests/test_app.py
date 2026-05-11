import pytest

BASE_URL = "http://127.0.0.1:8051"


@pytest.fixture
def dashboard(dash_server, page):
    page.goto(BASE_URL)
    page.wait_for_selector(".dash-graph", timeout=30000)
    return page


def test_header_present(dashboard):
    h1 = dashboard.wait_for_selector("h1", timeout=10000)
    assert "Pink Morsel Sales Dashboard" in h1.inner_text()


def test_visualisations_present(dashboard):
    dashboard.wait_for_function(
        "document.querySelectorAll('.dash-graph').length >= 2",
        timeout=30000,
    )


def test_region_picker_present(dashboard):
    dashboard.wait_for_selector("#region-filter", timeout=10000)
