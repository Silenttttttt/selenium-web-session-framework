# Web Automation Framework

This framework provides a set of tools for automating web interactions using Selenium. It includes methods for navigating to URLs, interacting with web elements, extracting data, and performing various actions such as clicking, typing, and scrolling.

## Getting Started

### Installation

1. **Install Selenium**: Make sure you have Selenium installed. You can install it using pip:
   ```
   pip install selenium
   ```

2. **WebDriver**: Download the appropriate WebDriver for your browser (e.g., ChromeDriver for Chrome) and ensure it's in your system's PATH.

### Initialization

To start using the framework, you need to initialize a `WebSession` object. You can choose to run the browser in headless mode or not.

### Example:
```python
# Import the WebSession class
from web_actions import WebSession

# Initialize the WebSession object
session = WebSession(headless=False)

# Navigate to Google
session.go_to("https://www.google.com")

# Get the page title
page_title = session.get_page_title()
print(page_title)

# Close the browser session
session.close()
```

## Methods Overview

### Navigation

- **go_to(url: str) -> bool**: Navigate to a specified URL.
  - `url`: The URL to navigate to.
  - Returns `True` if navigation is successful.

### Waiting for Elements

- **wait_for_element(selector_type: SelectorType, selector: str, timeout: int = 10) -> Optional[WebElement]**: Wait for an element to be present in the DOM.
  - `selector_type`: The type of selector (XPATH or CSS).
  - `selector`: The selector string.
  - `timeout`: The maximum time to wait for the element.
  - Returns the found element, or `None` if not found.

- **wait_for_elements(selector_type: SelectorType, selector: str, timeout: int = 10) -> List[WebElement]**: Wait for multiple elements to be present in the DOM.
  - `selector_type`: The type of selector (XPATH or CSS).
  - `selector`: The selector string.
  - `timeout`: The maximum time to wait for the elements.
  - Returns a list of found elements, or an empty list if none are found.

### Finding Elements

- **find_element(selector_type: SelectorType, selector: str, skip_wait: bool = False, timeout: int = 10) -> Optional[WebElement]**: Find a single element in the DOM.
  - `selector_type`: The type of selector (XPATH or CSS).
  - `selector`: The selector string.
  - `skip_wait`: Whether to skip waiting for the element.
  - `timeout`: The maximum time to wait for the element.
  - Returns the found element, or `None` if not found.

- **find_elements(selector_type: SelectorType, selector: str, skip_wait: bool = False, timeout: int = 10) -> List[WebElement]**: Find multiple elements in the DOM.
  - `selector_type`: The type of selector (XPATH or CSS).
  - `selector`: The selector string.
  - `skip_wait`: Whether to skip waiting for the elements.
  - `timeout`: The maximum time to wait for the elements.
  - Returns a list of found elements, or an empty list if none are found.

### Interacting with Elements

- **click(selector_type: SelectorType, selector: str, skip_wait: bool = False, timeout: int = 10) -> bool**: Click an element.
  - `selector_type`: The type of selector (XPATH or CSS).
  - `selector`: The selector string.
  - `skip_wait`: Whether to skip waiting for the element.
  - `timeout`: The maximum time to wait for the element.
  - Returns `True` if the click is successful, `False` otherwise.

- **right_click(selector_type: SelectorType, selector: str, skip_wait: bool = False, timeout: int = 10) -> bool**: Right-click an element.
  - `selector_type`: The type of selector (XPATH or CSS).
  - `selector`: The selector string.
  - `skip_wait`: Whether to skip waiting for the element.
  - `timeout`: The maximum time to wait for the element.
  - Returns `True` if the right-click is successful, `False` otherwise.

- **type_text(selector_type: SelectorType, selector: str, text: str, skip_wait: bool = False, timeout: int = 10, interactable_timeout: int = 10) -> bool**: Type text into an element.
  - `selector_type`: The type of selector (XPATH or CSS).
  - `selector`: The selector string.
  - `text`: The text to type.
  - `skip_wait`: Whether to skip waiting for the element.
  - `timeout`: The maximum time to wait for the element.
  - `interactable_timeout`: The maximum time to wait for the element to be interactable.
  - Returns `True` if the text is successfully typed, `False` otherwise.

- **clear(selector_type: SelectorType, selector: str, skip_wait: bool = False, timeout: int = 10, interactable_timeout: int = 10) -> bool**: Clear the text in an element.
  - `selector_type`: The type of selector (XPATH or CSS).
  - `selector`: The selector string.
  - `skip_wait`: Whether to skip waiting for the element.
  - `timeout`: The maximum time to wait for the element.
  - `interactable_timeout`: The maximum time to wait for the element to be interactable.
  - Returns `True` if the element is successfully cleared, `False` otherwise.

- **hover(selector_type: SelectorType, selector: str, skip_wait: bool = False, timeout: int = 10) -> bool**: Hover over an element.
  - `selector_type`: The type of selector (XPATH or CSS).
  - `selector`: The selector string.
  - `skip_wait`: Whether to skip waiting for the element.
  - `timeout`: The maximum time to wait for the element.
  - Returns `True` if the hover is successful, `False` otherwise.

### Extracting Data

- **extract(selector_type: SelectorType, selector: str, attribute: Optional[str] = None, skip_wait: bool = False, timeout: int = 10) -> Optional[str]**: Extract data from an element.
  - `selector_type`: The type of selector (XPATH or CSS).
  - `selector`: The selector string.
  - `attribute`: The attribute to extract. Use `"__text__"` to extract the text content.
  - `skip_wait`: Whether to skip waiting for the element.
  - `timeout`: The maximum time to wait for the element.
  - Returns the extracted data, or `None` if extraction fails.

### Getting Page Information

- **get_page_title() -> Optional[str]**: Get the title of the page.
  - Returns the page title, or `None` if retrieval fails.

- **get_page_source() -> Optional[str]**: Get the source code of the page.
  - Returns the page source, or `None` if retrieval fails.

- **get_current_url() -> Optional[str]**: Get the current URL of the page.
  - Returns the current URL, or `None` if retrieval fails.

### Closing the Session

- **close() -> bool**: Close the browser session.
  - Returns `True` if the session is successfully closed.

### Scrolling

- **scroll(direction: str = "down", amount: Optional[int] = None, selector_type: Optional[SelectorType] = None, selector: Optional[str] = None, x: Optional[int] = None, y: Optional[int] = None, to_end: bool = False, timeout: int = 10) -> bool**: Scroll the page or an element.
  - `direction`: The direction to scroll ("down", "up", "to_element").
  - `amount`: The amount to scroll (used for "down" and "up" directions).
  - `selector_type`: The type of selector (XPATH or CSS) for the element to scroll to.
  - `selector`: The selector string for the element to scroll to.
  - `x`: The x-coordinate to scroll to.
  - `y`: The y-coordinate to scroll to.
  - `to_end`: If `True`, scrolls to the bottom of the element or the entire page. If `False`, scrolls to the top.
  - `timeout`: The maximum time to wait for the element.
  - Returns `True` if the scroll is successful, `False` otherwise.


## The up to date, and complete documentation can be found in the Docstrings

## Examples

Refer to the `script_tests.py` file for example usage of the framework. The file contains various examples demonstrating how to use the methods provided by the `WebSession` class/
