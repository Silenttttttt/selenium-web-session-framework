from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.remote.webelement import WebElement
from enum import Enum
import traceback
from typing import List, Optional, Any, Dict

class SelectorType(Enum):
    """Enum for selector types."""
    XPATH = 'xpath'
    CSS = 'css'

class WebSession:
    def __init__(self, options: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the WebSession.
        
        Args:
            options (dict): A dictionary of options to configure the browser.
        """
        chrome_options = webdriver.ChromeOptions()
        if options:
            for key, value in options.items():
                if isinstance(value, bool) and value:
                    chrome_options.add_argument(f"--{key}")
                elif isinstance(value, str):
                    chrome_options.add_argument(f"--{key}={value}")
        self.driver = webdriver.Chrome(options=chrome_options)


    def go_to(self, url: str) -> bool:
        """
        Navigate to a URL.
        
        Args:
            url (str): The URL to navigate to.
        
        Returns:
            bool: True if navigation is successful.
        """
        self.driver.get(url)
        return True

    def wait_for_element(self, selector_type: SelectorType, selector: str, timeout: int = 10) -> Optional[WebElement]:
        """
        Wait for an element to be present in the DOM.
        
        Args:
            selector_type (SelectorType): The type of selector (XPATH or CSS).
            selector (str): The selector string.
            timeout (int): The maximum time to wait for the element.
        
        Returns:
            WebElement: The found element, or None if not found.
        """
        try:
            if selector_type == SelectorType.XPATH:
                return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, selector)))
            elif selector_type == SelectorType.CSS:
                return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            else:
                raise ValueError(f"Unsupported selector type: {selector_type}")
        except Exception as e:
            print(f"Error waiting for element: {e}")
            traceback.print_exc()
            return None

    def wait_for_elements(self, selector_type: SelectorType, selector: str, timeout: int = 10) -> List[WebElement]:
        """
        Wait for multiple elements to be present in the DOM.
        
        Args:
            selector_type (SelectorType): The type of selector (XPATH or CSS).
            selector (str): The selector string.
            timeout (int): The maximum time to wait for the elements.
        
        Returns:
            list: A list of found elements, or an empty list if none are found.
        """
        try:
            if selector_type == SelectorType.XPATH:
                return WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located((By.XPATH, selector)))
            elif selector_type == SelectorType.CSS:
                return WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
            else:
                raise ValueError(f"Unsupported selector type: {selector_type}")
        except Exception as e:
            print(f"Error waiting for elements: {e}")
            traceback.print_exc()
            return []

    def find_element(self, selector_type: SelectorType, selector: str, skip_wait: bool = False, timeout: int = 10) -> Optional[WebElement]:
        """
        Find a single element in the DOM.
        
        Args:
            selector_type (SelectorType): The type of selector (XPATH or CSS).
            selector (str): The selector string.
            skip_wait (bool): Whether to skip waiting for the element.
            timeout (int): The maximum time to wait for the element.
        
        Returns:
            WebElement: The found element, or None if not found.
        """
        if skip_wait:
            if selector_type == SelectorType.XPATH:
                return self.driver.find_element(By.XPATH, selector)
            elif selector_type == SelectorType.CSS:
                return self.driver.find_element(By.CSS_SELECTOR, selector)
            else:
                raise ValueError(f"Unsupported selector type: {selector_type}")
        else:
            return self.wait_for_element(selector_type, selector, timeout)

    def find_elements(self, selector_type: SelectorType, selector: str, skip_wait: bool = False, timeout: int = 10) -> List[WebElement]:
        """
        Find multiple elements in the DOM.
        
        Args:
            selector_type (SelectorType): The type of selector (XPATH or CSS).
            selector (str): The selector string.
            skip_wait (bool): Whether to skip waiting for the elements.
            timeout (int): The maximum time to wait for the elements.
        
        Returns:
            list: A list of found elements, or an empty list if none are found.
        """
        if skip_wait:
            if selector_type == SelectorType.XPATH:
                return self.driver.find_elements(By.XPATH, selector)
            elif selector_type == SelectorType.CSS:
                return self.driver.find_elements(By.CSS_SELECTOR, selector)
            else:
                raise ValueError(f"Unsupported selector type: {selector_type}")
        else:
            return self.wait_for_elements(selector_type, selector, timeout)

    def click(self, selector_type: SelectorType, selector: str, skip_wait: bool = False, timeout: int = 10) -> bool:
        """
        Click an element.
        
        Args:
            selector_type (SelectorType): The type of selector (XPATH or CSS).
            selector (str): The selector string.
            skip_wait (bool): Whether to skip waiting for the element.
            timeout (int): The maximum time to wait for the element.
        
        Returns:
            bool: True if the click is successful, False otherwise.
        """
        try:
            element = self.find_element(selector_type, selector, skip_wait, timeout)
            if element:
                return self.safe_click(element)
            return False
        except Exception as e:
            print(f"Error clicking element: {e}")
            traceback.print_exc()
            return False

    def safe_click(self, element: WebElement) -> bool:
        """
        Safely click an element, handling potential interceptors.
        
        Args:
            element (WebElement): The element to click.
            timeout (int): The maximum time to wait for the element to be clickable.
        
        Returns:
            bool: True if the click is successful, False otherwise.
        
        Note:
            This method is experimental.
        """
        try:
            element.click()
            return True
        except ElementClickInterceptedException as e:
            print(f"Element click intercepted: {e}")
            traceback.print_exc()
            # Find the element that intercepted the click
            interceptor_element = self.driver.execute_script("""
                var elem = arguments[0];
                var rect = elem.getBoundingClientRect();
                var x = rect.left + (rect.width / 2);
                var y = rect.top + (rect.height / 2);
                return document.elementFromPoint(x, y);
            """, element)
            if interceptor_element:
                try:
                    print(f"Clicking interceptor element: {interceptor_element}")
                    interceptor_element.click()
                    return True
                except Exception as e:
                    print(f"Error clicking interceptor element: {e}")
                    traceback.print_exc()
            return False

    def right_click(self, selector_type: SelectorType, selector: str, skip_wait: bool = False, timeout: int = 10) -> bool:
        """
        Right-click an element.
        
        Args:
            selector_type (SelectorType): The type of selector (XPATH or CSS).
            selector (str): The selector string.
            skip_wait (bool): Whether to skip waiting for the element.
            timeout (int): The maximum time to wait for the element.
        
        Returns:
            bool: True if the right-click is successful, False otherwise.
        """
        try:
            element = self.find_element(selector_type, selector, skip_wait, timeout)
            if element:
                actions = ActionChains(self.driver)
                actions.context_click(element).perform()
                return True
            return False
        except Exception as e:
            print(f"Error right-clicking element: {e}")
            traceback.print_exc()
            return False

    def type_text(self, selector_type: SelectorType, selector: str, text: str, skip_wait: bool = False, timeout: int = 10, interactable_timeout: int = 10) -> bool:
        """
        Type text into an element.
        
        Args:
            selector_type (SelectorType): The type of selector (XPATH or CSS).
            selector (str): The selector string.
            text (str): The text to type.
            skip_wait (bool): Whether to skip waiting for the element.
            timeout (int): The maximum time to wait for the element.
            interactable_timeout (int): The maximum time to wait for the element to be interactable.
        
        Returns:
            bool: True if the text is successfully typed, False otherwise.
        """
        try:
            element = self.find_element(selector_type, selector, skip_wait, timeout)
            if element:
                if interactable_timeout != -1:
                    WebDriverWait(self.driver, interactable_timeout).until(EC.element_to_be_clickable((By.XPATH, selector)))
                element.send_keys(text)
                return True
            return False
        except Exception as e:
            print(f"Error typing in element: {e}")
            traceback.print_exc()
            return False

    def clear(self, selector_type: SelectorType, selector: str, skip_wait: bool = False, timeout: int = 10, interactable_timeout: int = 10) -> bool:
        """
        Clear the text in an element.
        
        Args:
            selector_type (SelectorType): The type of selector (XPATH or CSS).
            selector (str): The selector string.
            skip_wait (bool): Whether to skip waiting for the element.
            timeout (int): The maximum time to wait for the element.
            interactable_timeout (int): The maximum time to wait for the element to be interactable.
        
        Returns:
            bool: True if the element is successfully cleared, False otherwise.
        """
        try:
            element = self.find_element(selector_type, selector, skip_wait, timeout)
            if element:
                if interactable_timeout != -1:
                    WebDriverWait(self.driver, interactable_timeout).until(EC.element_to_be_clickable((By.XPATH, selector)))
                element.clear()
                return True
            return False
        except Exception as e:
            print(f"Error clearing element: {e}")
            traceback.print_exc()
            return False

    def hover(self, selector_type: SelectorType, selector: str, skip_wait: bool = False, timeout: int = 10) -> bool:
        """
        Hover over an element.
        
        Args:
            selector_type (SelectorType): The type of selector (XPATH or CSS).
            selector (str): The selector string.
            skip_wait (bool): Whether to skip waiting for the element.
            timeout (int): The maximum time to wait for the element.
        
        Returns:
            bool: True if the hover is successful, False otherwise.
        """
        try:
            element = self.find_element(selector_type, selector, skip_wait, timeout)
            if element:
                actions = ActionChains(self.driver)
                actions.move_to_element(element).perform()
                return True
            return False
        except Exception as e:
            print(f"Error hovering over element: {e}")
            traceback.print_exc()
            return False

    def extract(self, selector_type: SelectorType, selector: str, attribute: Optional[str] = None, skip_wait: bool = False, timeout: int = 10) -> Optional[str]:
        """
        Extract data from an element.
        
        Args:
            selector_type (SelectorType): The type of selector (XPATH or CSS).
            selector (str): The selector string.
            attribute (str): The attribute to extract. Use "__text__" to extract the text content.
            skip_wait (bool): Whether to skip waiting for the element.
            timeout (int): The maximum time to wait for the element.
        
        Returns:
            str: The extracted data, or None if extraction fails.
        """
        try:
            element = self.find_element(selector_type, selector, skip_wait, timeout)
            if element:
                if attribute == "__text__":
                    return element.text
                elif attribute:
                    return element.get_attribute(attribute)
                else:
                    return element.text
            return None
        except Exception as e:
            print(f"Error extracting data: {e}")
            traceback.print_exc()
            return None

    def run_js(self, selector_type: SelectorType, selector: str, script: str, skip_wait: bool = False, timeout: int = 10) -> Optional[Any]:
        """
        Run JavaScript on an element.
        
        Args:
            selector_type (SelectorType): The type of selector (XPATH or CSS).
            selector (str): The selector string.
            script (str): The JavaScript code to run.
            skip_wait (bool): Whether to skip waiting for the element.
            timeout (int): The maximum time to wait for the element.
        
        Returns:
            Any: The result of the JavaScript execution, or None if execution fails.
        """
        try:
            element = self.find_element(selector_type, selector, skip_wait, timeout)
            if element:
                result = self.driver.execute_script(script, element)
                print(f"JavaScript execution result: {result}")
                return result
            return None
        except Exception as e:
            print(f"Error running JavaScript: {e}")
            traceback.print_exc()
            return None

    def get_page_title(self) -> Optional[str]:
        """
        Get the title of the page.
        
        Returns:
            str: The page title, or None if retrieval fails.
        """
        try:
            return self.driver.title
        except Exception as e:
            print(f"Error getting page title: {e}")
            traceback.print_exc()
            return None

    def get_page_source(self) -> Optional[str]:
        """
        Get the source code of the page.
        
        Returns:
            str: The page source, or None if retrieval fails.
        """
        try:
            return self.driver.page_source
        except Exception as e:
            print(f"Error getting page source: {e}")
            traceback.print_exc()
            return None

    def get_current_url(self) -> Optional[str]:
        """
        Get the current URL of the page.
        
        Returns:
            str: The current URL, or None if retrieval fails.
        """
        try:
            return self.driver.current_url
        except Exception as e:
            print(f"Error getting current URL: {e}")
            traceback.print_exc()
            return None

    def close(self) -> bool:
        """
        Close the browser session.
        
        Returns:
            bool: True if the session is successfully closed.
        """
        self.driver.quit()
        return True

    def scroll(self, direction: str = "down", amount: Optional[int] = None, selector_type: Optional[SelectorType] = None, selector: Optional[str] = None, x: Optional[int] = None, y: Optional[int] = None, to_end: bool = False, timeout: int = 10) -> bool:
        """
        Scroll the page or an element.
        
        Args:
            direction (str): The direction to scroll ("down", "up", "to_element").
            amount (int): The amount to scroll (used for "down" and "up" directions).
            selector_type (SelectorType): The type of selector (XPATH or CSS) for the element to scroll to.
            selector (str): The selector string for the element to scroll to.
            x (int): The x-coordinate to scroll to.
            y (int): The y-coordinate to scroll to.
            to_end (bool): If True, scrolls to the bottom of the element or the entire page. If False, scrolls to the top.
            timeout (int): The maximum time to wait for the element.
        
        Returns:
            bool: True if the scroll is successful, False otherwise.
        """
        try:
            if x is not None and y is not None:
                self.driver.execute_script(f"window.scrollTo({x}, {y});")
            elif direction == "down":
                if amount:
                    self.driver.execute_script(f"window.scrollBy(0, {amount});")
                elif selector_type and selector:
                    element = self.find_element(selector_type, selector, timeout=timeout)
                    if element:
                        if to_end:
                            self.driver.execute_script("arguments[0].scrollIntoView(false);", element)
                        else:
                            self.driver.execute_script("arguments[0].scrollIntoView();", element)
                else:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            elif direction == "up":
                if amount:
                    self.driver.execute_script(f"window.scrollBy(0, -{amount});")
                elif selector_type and selector:
                    element = self.find_element(selector_type, selector, timeout=timeout)
                    if element:
                        if to_end:
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                        else:
                            self.driver.execute_script("arguments[0].scrollIntoView();", element)
                else:
                    self.driver.execute_script("window.scrollTo(0, 0);")
            elif direction == "to_element" and selector_type and selector:
                element = self.find_element(selector_type, selector, timeout=timeout)
                if element:
                    self.driver.execute_script("arguments[0].scrollIntoView();", element)
            else:
                raise ValueError("Invalid scroll parameters")
            return True
        except Exception as e:
            print(f"Error scrolling: {e}")
            traceback.print_exc()
            return False