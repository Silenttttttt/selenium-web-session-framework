from web_actions import SelectorType, WebSession
import time

# Define selectors in a dictionary
selectors = {
    "video_title": '//*[@id="title"]/h1/yt-formatted-string',
    "search_box": '//*[@id="search"]',
    "search_button": '//*[@id="search-icon-legacy"]',
    "video_thumbnail": '(//*[@id="thumbnail"])[1]',
    "subscribe_button": '//*[@id="subscribe-button"]/ytd-subscribe-button-renderer'
}

def example_navigation(session):
    """Example of navigating to a URL and retrieving session information."""
    # Navigate to YouTube
    session.go_to("https://www.youtube.com")
    # Print the current URL
    print(f"Current URL: {session.get_current_url()}")
    # Print the page title
    print(f"Page Title: {session.get_page_title()}")

def example_search(session):
    """Example of performing a search on YouTube."""
    # Navigate to YouTube
    session.go_to("https://www.youtube.com")
    # Clear the search box
    session.clear(SelectorType.XPATH, selectors["search_box"], timeout=10)
    # Type a search query into the search box
    session.type_text(SelectorType.XPATH, selectors["search_box"], "Selenium Python", timeout=10)
    # Click the search button
    session.click(SelectorType.XPATH, selectors["search_button"], timeout=10)
    # Wait for search results to load
    time.sleep(5)
    # Print the current URL after search
    print(f"Search completed. Current URL: {session.get_current_url()}")

def example_click_and_extract(session):
    """Example of clicking a video thumbnail and extracting the video title."""
    # Navigate to YouTube
    session.go_to("https://www.youtube.com")
    # Type a search query into the search box
    session.type_text(SelectorType.XPATH, selectors["search_box"], "Selenium Python", timeout=10)
    # Click the search button
    session.click(SelectorType.XPATH, selectors["search_button"], timeout=10)
    # Wait for search results to load
    time.sleep(5)
    # Click the first video thumbnail
    session.click(SelectorType.XPATH, selectors["video_thumbnail"], timeout=10)
    # Extract the video title
    video_title = session.extract(SelectorType.XPATH, selectors["video_title"], "__text__", timeout=10)
    # Print the video title
    print(f"Video title: {video_title}")

def example_hover(session):
    """Example of hovering over an element."""
    # Navigate to a specific YouTube video
    session.go_to("https://www.youtube.com/watch?v=e3BrJUXxFSY")
    # Hover over the video title
    session.hover(SelectorType.XPATH, selectors["video_title"], timeout=10)
    # Print a message indicating the hover action
    print("Hovered over the video title.")

def example_run_js(session):
    """Example of running JavaScript to scroll down the page."""
    # Navigate to a specific YouTube video
    session.go_to("https://www.youtube.com/watch?v=e3BrJUXxFSY")
    # Run JavaScript to scroll down the page
    session.run_js(SelectorType.XPATH, selectors["video_title"], "window.scrollTo(0, document.body.scrollHeight);", timeout=10)
    # Print a message indicating the JavaScript execution
    print("Ran JavaScript to scroll down the page.")

def example_direct_driver_access(session):
    """Example of accessing the WebDriver directly."""
    # Navigate to YouTube
    session.go_to("https://www.youtube.com")
    # Find the search box using direct WebDriver access
    search_box = session.driver.find_element_by_xpath(selectors["search_box"])
    # Clear the search box
    search_box.clear()
    # Type a search query into the search box
    search_box.send_keys("Selenium Python")
    # Find the search button using direct WebDriver access
    search_button = session.driver.find_element_by_xpath(selectors["search_button"])
    # Click the search button
    search_button.click()
    # Wait for search results to load
    time.sleep(5)
    # Print a message indicating the search action
    print("Performed search using direct WebDriver access.")

def main():
    # Initialize the web session
    session = WebSession(headless=False)
    # Perform navigation example
    example_navigation(session)
    # Perform search example
    example_search(session)
    # Perform click and extract example
    example_click_and_extract(session)
    # Perform hover example
    example_hover(session)
    # Perform JavaScript execution example
    example_run_js(session)
    # Perform direct WebDriver access example
    example_direct_driver_access(session)
    # Wait for 10 seconds to observe the actions
    time.sleep(10)
    # Close the session
    session.close()

if __name__ == "__main__":
    main()