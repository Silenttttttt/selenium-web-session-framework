from web_actions import SelectorType, WebSession
import time

# Define selectors in a dictionary
selectors = {
    "video_title": '//*[@id="title"]/h1/yt-formatted-string'
}

def perform_actions(session):
    session.go_to("https://www.youtube.com/watch?v=e3BrJUXxFSY")
   
    # Use the selectors from the dictionary
    video_title = session.extract(SelectorType.XPATH, selectors["video_title"], "__text__", timeout=10)
    print(f"Video title: {video_title}")

    # Get session information
    current_url = session.get_current_url()
    page_title = session.get_page_title()
    page_source = session.get_page_source()

    print(f"Current URL: {current_url}")
    print(f"Page Title: {page_title}")
    # Optionally, print the page source (it can be very large)
    # print(f"Page Source: {page_source}")

def main():
    # Initialize the web session
    session = WebSession(headless=False)

    # Perform actions
    perform_actions(session)

    # Wait for 10 seconds to observe the actions
    time.sleep(10)

    # Close the session
    session.close()

if __name__ == "__main__":
    main()