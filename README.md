# Selenium Web Session Framework

A Python framework for web automation using Selenium, providing easy-to-use methods for common web interactions with support for explicit waits and organized selectors.

## Features

- Easy-to-use methods for common web interactions (click, type, clear, hover, etc.)
- Support for explicit waits to ensure elements are present before interacting
- Organized selectors using a dictionary for cleaner and more maintainable scripts
- Ability to skip waits and specify timeouts for element interactions
- Methods to retrieve session information (current URL, page title, page source)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Silenttttttt/selenium-web-session-framework.git
    ```

2. Install the required dependencies:
    ```sh
    pip install selenium
    ```

## Usage

### Define Selectors

Define your selectors in a dictionary at the top of your script.

### Perform Actions

Use the framework to perform actions on the web page.

### Example Script

The `script_tests.py` file contains a few examples of how to use the framework. Below is a brief overview of what the script does:

- Navigates to YouTube
- Clears the search box
- Types a search query into the search box
- Clicks the search button
- Waits for search results to load and clicks the first video thumbnail
- Extracts the video title
- Hovers over the video title
- Retrieves session information (current URL, page title, page source)
- Runs a JavaScript command to scroll down

For detailed examples, please refer to the `script_tests.py` file in the repository.

### Explanation of Methods

- `go_to(url)`: Navigate to the specified URL.
- `clear(selector_type, selector, skip_wait=False, timeout=10)`: Clear the text in the specified element.
- `type_text(selector_type, selector, text, skip_wait=False, timeout=10)`: Type the specified text into the specified element.
- `click(selector_type, selector, skip_wait=False, timeout=10)`: Click the specified element.
- `hover(selector_type, selector, skip_wait=False, timeout=10)`: Hover over the specified element.
- `extract(selector_type, selector, attribute=None, skip_wait=False, timeout=10)`: Extract the specified attribute (or text) from the specified element.
- `run_js(selector_type, selector, script, skip_wait=False, timeout=10)`: Run the specified JavaScript code on the specified element.
- `get_current_url()`: Get the current URL of the browser.
- `get_page_title()`: Get the title of the current page.
- `get_page_source()`: Get the source code of the current page.
- `close()`: Close the browser session.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.