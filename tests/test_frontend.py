import pytest
from playwright.sync_api import Page

FRONTEND_URL = "http://localhost:3001"

# Page loads and shows the right heading
def test_page_loads_and_shows_title(page: Page):
    page.goto(FRONTEND_URL)
    heading = page.locator("h1")
    assert heading.inner_text() == "Legal Assistant"

# Typed "Data Protection" and saw the result appear
def test_search_returns_results(page: Page):
    page.goto(FRONTEND_URL)
    page.get_by_placeholder("Search for legal documents...").fill("Data Protection")
    page.get_by_role("button", name="Search").click()
    page.wait_for_selector("h3")
    assert page.get_by_role("heading", name="Data Protection and Privacy Act").is_visible()

# Search "Hello" UI shows a no results message
def test_search_with_unknown_query_shows_no_results_message(page: Page):
    page.goto(FRONTEND_URL)
    page.get_by_placeholder("Search for legal documents...").fill("xyzunknown123")
    page.get_by_role("button", name="Search").click()
    page.wait_for_selector("text=No documents found")
    assert page.get_by_text("No documents found matching").is_visible()

# Pressing Enter with empty input fires an API call but the UI shows nothing
# SearchBar.tsx onKeyUp has no empty string check
def test_empty_query_via_enter_key_gives_no_feedback(page: Page):
    page.goto(FRONTEND_URL)
    page.get_by_placeholder("Search for legal documents...").press("Enter")
    page.wait_for_timeout(2000)
    assert page.get_by_text("No documents found").is_visible() == False
    assert page.get_by_text("Please provide").is_visible() == False

# Button should disabled when input is empty
def test_search_button_disabled_when_empty(page: Page):
    page.goto(FRONTEND_URL)
    button = page.get_by_role("button", name="Search")
    assert button.is_disabled() == True

# Button becomes clickable once user typing
def test_search_button_enabled_when_text_entered(page: Page):
    page.goto(FRONTEND_URL)
    page.get_by_placeholder("Search for legal documents...").fill("Contract")
    button = page.get_by_role("button", name="Search")
    assert button.is_disabled() == False

# "act" appears in multiple, checking all results render
def test_multiple_results_returned(page: Page):
    page.goto(FRONTEND_URL)
    page.get_by_placeholder("Search for legal documents...").fill("act")
    page.get_by_role("button", name="Search").click()
    page.wait_for_selector("h3")
    headings = page.locator("h3").all()
    assert len(headings) > 1