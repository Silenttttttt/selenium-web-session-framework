from web_actions import SelectorType, WebSession
import time
from selenium.webdriver.common.by import By

# Define selectors in a dictionary for easy access and readability
selectors = {
    "video_title": '//*[@id="title"]/h1/yt-formatted-string',
    "search_box": '/html[1]/body[1]/ytd-app[1]/div[1]/div[1]/ytd-masthead[1]/div[4]/div[2]/ytd-searchbox[1]/form[1]/div[1]/div[1]/input[1]',
    "search_button": '//*[@id="search-icon-legacy"]',
    "video_thumbnail": '//*[@id="thumbnail"]/yt-image/img',
    "subscribe_button": '//*[@id="subscribe-button"]/ytd-subscribe-button-renderer',
    "channel_name": '//*[@id="text"]/a',
    "github_footer": '/html/body/div[1]/footer'
}

def example_navigation(session):
    """Example of navigating to a URL and retrieving session information."""
    # Navigate to YouTube
    session.go_to("https://www.youtube.com")

    # Get page source
    print(session.get_page_source())
    # Print the current URL
    print(f"Current URL: {session.get_current_url()}")
    # Print the page title
    print(f"Page Title: {session.get_page_title()}")

def example_search(session):
    """Example of performing a search on YouTube."""
    # Navigate to YouTube
    session.go_to("https://www.youtube.com")
    # Clear the search box with interactable timeout
    session.clear(SelectorType.XPATH, selectors["search_box"], timeout=10, interactable_timeout=10)
    # Type a search query into the search box with interactable timeout
    session.type_text(SelectorType.XPATH, selectors["search_box"], "Selenium Python", timeout=10, interactable_timeout=10)
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
    # Type a search query into the search box with interactable timeout
    session.type_text(SelectorType.XPATH, selectors["search_box"], "Selenium Python", timeout=10, interactable_timeout=10)
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
    session.hover(SelectorType.XPATH, selectors["channel_name"], timeout=10)
    # Print a message indicating the hover action
    print("Hovered over the channel name.")

def example_run_js(session):
    """Example of running JavaScript to scroll down the page."""
    # Navigate to a specific YouTube video
    session.go_to("https://www.youtube.com/watch?v=e3BrJUXxFSY")
    time.sleep(5)
    # Run JavaScript to scroll down the page
    session.run_js(SelectorType.XPATH, selectors["video_title"], "window.scrollTo(0, document.body.scrollHeight);", timeout=10)
    # Print a message indicating the JavaScript execution
    print("Ran JavaScript to scroll down the page.")


def example_run_js_scroll(session):
    """Example of running JavaScript to console log a message."""
    # Navigate to a specific YouTube video
    session.go_to("https://www.youtube.com/watch?v=e3BrJUXxFSY")
    time.sleep(5)
    # Run JavaScript to console log a message
    result = session.driver.execute_script("console.log('JavaScript executed'); return 'JavaScript executed';")
    # Print the return value of the JavaScript execution
    print(f"Value returned: {result}")
  


def example_direct_driver_access(session):
    """Example of accessing the WebDriver directly."""
    # Navigate to YouTube
    session.go_to("https://www.youtube.com")
    # Find the search box using direct WebDriver access
    search_box = session.driver.find_element(By.XPATH, selectors["search_box"])
    # Clear the search box
    search_box.clear()
    # Type a search query into the search box
    search_box.send_keys("Selenium Python")
    # Find the search button using direct WebDriver access
    search_button = session.driver.find_element(By.XPATH, selectors["search_button"])
    # Click the search button
    search_button.click()
    # Wait for search results to load
   # time.sleep(5)
    # Print a message indicating the search action
    print("Performed search using direct WebDriver access.")

def example_find_multiple_elements(session):
    """Example of finding multiple elements."""
    # Navigate to YouTube
    session.go_to("https://www.youtube.com")
    # Type a search query into the search box with interactable timeout
    session.type_text(SelectorType.XPATH, selectors["search_box"], "Selenium Python", timeout=10, interactable_timeout=10)
    # Click the search button
    session.click(SelectorType.XPATH, selectors["search_button"], timeout=10)
    # Wait for search results to load
    time.sleep(5)
    # Find multiple video thumbnails
    video_thumbnails = session.find_elements(SelectorType.XPATH, selectors["video_thumbnail"], timeout=10)
    # Print the number of video thumbnails found
    print(f"Number of video thumbnails found: {len(video_thumbnails)}")
    # Click the first video thumbnail if available
    if video_thumbnails:
        video_thumbnails[0].click()
        print("Clicked the first video thumbnail.")



def example_scroll_to_element(session):
    """Example of scrolling to a specific element."""
    # Navigate to a specific YouTube video
    session.go_to("https://github.com/Silenttttttt")
    time.sleep(5)
    # Scroll to the channel name element
    session.scroll(direction="to_element", selector_type=SelectorType.XPATH, selector=selectors["github_footer"])
    # Print a message indicating the scroll action
    print("Scrolled to the github footer element.")

def example_scroll_to_coords(session):
    """Example of scrolling to specific coordinates."""
    # Navigate to a specific YouTube video
    session.go_to("https://github.com/Silenttttttt")
    time.sleep(5)
    # Scroll to specific coordinates
    session.scroll(x=0, y=1000)
    # Print a message indicating the scroll action
    print("Scrolled to coordinates (0, 1000).")

def example_scroll_to_bottom_of_page(session):
    """Example of scrolling to the bottom of the page."""
    # Navigate to a specific YouTube video
    session.go_to("https://github.com/Silenttttttt")
    time.sleep(5)
    # Scroll to the bottom of the page
    session.scroll(direction="down", to_end=True)
    # Print a message indicating the scroll action
    print("Scrolled to the bottom of the page.")



def main():
    # Define options for the browser
    options = {
        "headless": False
    }

    # Initialize the web session
    session = WebSession(options)
    # Perform navigation example
    example_navigation(session)
    time.sleep(5)
    # Perform search example
    example_search(session)
    time.sleep(5)
    # Perform click and extract example
    example_click_and_extract(session)
    time.sleep(5)
    # Perform hover example
    example_hover(session)
    time.sleep(5)
    # Perform JavaScript execution example
    example_run_js(session)
    time.sleep(5)
    # Perform scroll to element example
    example_scroll_to_element(session)
    time.sleep(5)
    # Perform scroll to coordinates example
    example_scroll_to_coords(session)
    time.sleep(5)
    # Perform scroll to bottom of page example
    example_scroll_to_bottom_of_page(session)
    time.sleep(5)
    # Perform direct WebDriver access example
    example_direct_driver_access(session)
    time.sleep(5)
    # Perform find multiple elements example
    example_find_multiple_elements(session)
    # Wait for 10 seconds to observe the actions
    time.sleep(10)
    # Close the session
    session.close()

if __name__ == "__main__":
   main()
