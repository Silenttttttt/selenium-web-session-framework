import atexit
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, InvalidSelectorException
from selenium.webdriver.remote.webelement import WebElement
from enum import Enum
from typing import List, Optional, Any, Dict, Union
import re
import time

try:
    from tqdm import tqdm
    tqdm_installed = True
except ImportError:
    tqdm_installed = False


class SelectorType(Enum):
    """Enum for selector types."""
    XPATH = 'xpath'
    CSS = 'css'

def clean_traceback(tb: str) -> str:
    """
    Clean the traceback by removing unhelpful parts and add a divider.
    
    Args:
        tb (str): The original traceback string.
    
    Returns:
        str: The cleaned traceback string.
    """
    lines = tb.splitlines()
    cleaned_lines = ["-----------------------"]
    stacktrace_found = False

    for line in lines:
        if stacktrace_found:
            if re.match(r"#\d+\s0x[0-9a-fA-F]+", line.strip()):
                continue
            else:
                stacktrace_found = False  # Stop skipping lines once we encounter a non-matching line
        if "Stacktrace:" in line:
            stacktrace_found = True
            continue  # Skip the "Stacktrace:" line itself
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)

def format_deeper_traceback() -> str:
    """
    Format a deeper traceback by combining the current stack trace with the exception traceback.
    
    Returns:
        str: The formatted deeper traceback string.
    """
    current_stack = traceback.format_stack()[:-1]  # Exclude the current function call
    exception_traceback = traceback.format_exc().splitlines()
    combined_traceback = current_stack + exception_traceback
    return "\n".join(combined_traceback)

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
                # Add more specific handling as needed
        self.driver = webdriver.Chrome(options=chrome_options)
        atexit.register(self.close)

    def close(self) -> bool:
        """
        Close the browser session.
        
        Returns:
            bool: True if the session is successfully closed.
        """
        if self.driver:
            self.driver.quit()
        return True

    def debug(self) -> None:
        """
        Open the browser and wait indefinitely for debugging purposes.
        """
        print("Debug mode: Browser is open and waiting indefinitely.")
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("Debug mode: Exiting on keyboard interrupt.")
        finally:
            self.close()

    def wait_for_element(self, selector_type: SelectorType, selector: str, timeout: int = 10, suppress_traceback: bool = False, raise_exc: bool = False) -> Optional[WebElement]:
        """
        Wait for an element to be present in the DOM.
        
        Args:
            selector_type (SelectorType): The type of selector (XPATH or CSS).
            selector (str): The selector string.
            timeout (int): The maximum time to wait for the element.
            suppress_traceback (bool): Whether to suppress the traceback print.
            raise_exc (bool): Whether to re-raise the exception.
        
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
        except Exception:
            if raise_exc:
                raise
            if not suppress_traceback:
                error_traceback = format_deeper_traceback()
                print(clean_traceback(error_traceback))
            return None

    def wait_for_elements(self, selector_type: SelectorType, selector: str, timeout: int = 10, suppress_traceback: bool = False, raise_exc: bool = False) -> List[WebElement]:
        """
        Wait for multiple elements to be present in the DOM.
        
        Args:
            selector_type (SelectorType): The type of selector (XPATH or CSS).
            selector (str): The selector string.
            timeout (int): The maximum time to wait for the elements.
            suppress_traceback (bool): Whether to suppress the traceback print.
            raise_exc (bool): Whether to re-raise the exception.
        
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
        except Exception:
            if raise_exc:
                raise
            if not suppress_traceback:
                error_traceback = format_deeper_traceback()
                print(clean_traceback(error_traceback))
            return []

    def find_element(self, selector_type: SelectorType, selector: str, skip_wait: bool = False, timeout: int = 10, suppress_traceback: bool = False, raise_exc: bool = False) -> Optional[WebElement]:
        """
        Find a single element in the DOM.
        
        Args:
            selector_type (SelectorType): The type of selector (XPATH or CSS).
            selector (str): The selector string.
            skip_wait (bool): Whether to skip waiting for the element.
            timeout (int): The maximum time to wait for the element.
            suppress_traceback (bool): Whether to suppress the traceback print.
            raise_exc (bool): Whether to re-raise the exception.
        
        Returns:
            WebElement: The found element, or None if not found.
        """
        try:
            if skip_wait:
                if selector_type == SelectorType.XPATH:
                    return self.driver.find_element(By.XPATH, selector,)
                elif selector_type == SelectorType.CSS:
                    return self.driver.find_element(By.CSS_SELECTOR, selector)
                else:
                    raise ValueError(f"Unsupported selector type: {selector_type}")
            else:
                return self.wait_for_element(selector_type, selector, timeout, suppress_traceback, raise_exc)
        except Exception:
            if raise_exc:
                raise
            if not suppress_traceback:
                error_traceback = format_deeper_traceback()
                print(clean_traceback(error_traceback))
            return None

    def find_elements(self, selector_type: SelectorType, selector: str, skip_wait: bool = False, timeout: int = 10, suppress_traceback: bool = False, raise_exc: bool = False) -> List[WebElement]:
        """
        Find multiple elements in the DOM.
        
        Args:
            selector_type (SelectorType): The type of selector (XPATH or CSS).
            selector (str): The selector string.
            skip_wait (bool): Whether to skip waiting for the elements.
            timeout (int): The maximum time to wait for the elements.
            suppress_traceback (bool): Whether to suppress the traceback print.
            raise_exc (bool): Whether to re-raise the exception.
        
        Returns:
            list: A list of found elements, or an empty list if none are found.
        """
        try:
            if skip_wait:
                if selector_type == SelectorType.XPATH:
                    return self.driver.find_elements(By.XPATH, selector)
                elif selector_type == SelectorType.CSS:
                    return self.driver.find_elements(By.CSS_SELECTOR, selector)
                else:
                    raise ValueError(f"Unsupported selector type: {selector_type}")
            else:
                return self.wait_for_elements(selector_type, selector, timeout, suppress_traceback, raise_exc)
        except Exception:
            if raise_exc:
                raise
            if not suppress_traceback:
                error_traceback = format_deeper_traceback()
                print(clean_traceback(error_traceback))
            return []


    def find_similar_elements(self, element: Optional[WebElement] = None, selector_type: Optional[SelectorType] = None, selector: Optional[str] = None, suppress_traceback: bool = False, reraise_exception: bool = False) -> List[WebElement]:
        """
        Find similar elements in the DOM based on a given element or selector.
        
        Args:
            element (WebElement): The reference element to find similar elements.
            selector_type (SelectorType): The type of selector (XPATH or CSS).
            selector (str): The selector string.
            suppress_traceback (bool): Whether to suppress the traceback print.
            reraise_exception (bool): Whether to re-raise the exception.
        
        Returns:
            list: A list of similar elements, or an empty list if none are found.
        """
        try:
            if element:
                # Find the parent container that holds all similar elements
                parent = element.find_element(By.XPATH, "..")
                # Use a specific XPath to find all child elements within that container
                similar_elements = parent.find_elements(By.XPATH, f".//{element.tag_name}")
            elif selector_type and selector:
                # Find the reference element using the selector
                reference_element = self.find_element(selector_type, selector)
                if reference_element:
                    # Find the parent container that holds all similar elements
                    parent = reference_element.find_element(By.XPATH, "..")
                    # Use a specific XPath to find all child elements within that container
                    similar_elements = parent.find_elements(By.XPATH, f".//{reference_element.tag_name}")
                else:
                    similar_elements = []
            else:
                raise ValueError("Either element or selector_type and selector must be provided.")
            
            # Filter out the reference element itself if it's included in the results
            if element:
                similar_elements = [el for el in similar_elements if el != element]
            elif reference_element:
                similar_elements = [el for el in similar_elements if el != reference_element]
            
            return similar_elements
        except Exception:
            if reraise_exception:
                raise
            if not suppress_traceback:
                error_traceback = format_deeper_traceback()
                print(clean_traceback(error_traceback))
            return []

    def click(self, selector_type: SelectorType, selector: str, skip_wait: bool = False, timeout: int = 10, suppress_traceback: bool = False, raise_exc: bool = False) -> bool:
        """
        Click an element.
        
        Args:
            selector_type (SelectorType): The type of selector (XPATH or CSS).
            selector (str): The selector string.
            skip_wait (bool): Whether to skip waiting for the element.
            timeout (int): The maximum time to wait for the element.
            suppress_traceback (bool): Whether to suppress the traceback print.
            raise_exc (bool): Whether to re-raise the exception.
        
        Returns:
            bool: True if the click is successful, False otherwise.
        """
        try:
            element = self.find_element(selector_type, selector, skip_wait, timeout, suppress_traceback, raise_exc)
            if element:
                return self.safe_click(element)
            return False
        except Exception:
            if raise_exc:
                raise
            if not suppress_traceback:
                error_traceback = format_deeper_traceback()
                print(clean_traceback(error_traceback))
            return False

    def safe_click(self, element: WebElement, suppress_traceback: bool = False, raise_exc: bool = False) -> bool:
        """
        Safely click an element, handling potential interceptors.
        
        Args:
            element (WebElement): The element to click.
            suppress_traceback (bool): Whether to suppress the traceback print.
            raise_exc (bool): Whether to re-raise the exception.
        Returns:
            bool: True if the click is successful, False otherwise.
        
        Note:
            This method is experimental.
        """
        try:
            element.click()
            return True
        except ElementClickInterceptedException:
            error_traceback = format_deeper_traceback()
            print(clean_traceback(error_traceback))
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
                except Exception:   
                    if raise_exc:
                        raise
                    if not suppress_traceback:
                        error_traceback = format_deeper_traceback()
                        print(clean_traceback(error_traceback))
            return False

    def right_click(self, selector_type: SelectorType, selector: str, skip_wait: bool = False, timeout: int = 10, suppress_traceback: bool = False, raise_exc: bool = False) -> bool:
        """
        Right-click an element.
        
        Args:
            selector_type (SelectorType): The type of selector (XPATH or CSS).
            selector (str): The selector string.
            skip_wait (bool): Whether to skip waiting for the element.
            timeout (int): The maximum time to wait for the element.
            suppress_traceback (bool): Whether to suppress the traceback print.
            raise_exc (bool): Whether to re-raise the exception.
        
        Returns:
            bool: True if the right-click is successful, False otherwise.
        """
        try:
            element = self.find_element(selector_type, selector, skip_wait, timeout, suppress_traceback, raise_exc)
            if element:
                actions = ActionChains(self.driver)
                actions.context_click(element).perform()
                return True
            return False
        except Exception:
            if raise_exc:
                raise
            if not suppress_traceback:
                error_traceback = format_deeper_traceback()
                print(clean_traceback(error_traceback))
            return False

    def type_text(self, selector_type: SelectorType, selector: str, text: str, skip_wait: bool = False, timeout: int = 10, interactable_timeout: int = 10, suppress_traceback: bool = False, raise_exc: bool = False) -> bool:
        """
        Type text into an element.
        
        Args:
            selector_type (SelectorType): The type of selector (XPATH or CSS).
            selector (str): The selector string.
            text (str): The text to type.
            skip_wait (bool): Whether to skip waiting for the element.
            timeout (int): The maximum time to wait for the element.
            interactable_timeout (int): The maximum time to wait for the element to be interactable.
            suppress_traceback (bool): Whether to suppress the traceback print.
            raise_exc (bool): Whether to re-raise the exception.
        Returns:
            bool: True if the text is successfully typed, False otherwise.
        """
        try:
            element = self.find_element(selector_type, selector, skip_wait, timeout, suppress_traceback, raise_exc)
            if element:
                if interactable_timeout != -1:
                    WebDriverWait(self.driver, interactable_timeout).until(EC.element_to_be_clickable((By.XPATH, selector)))
                element.send_keys(text)
                return True
            return False
        except Exception:
            if raise_exc:
                raise
            if not suppress_traceback:
                error_traceback = format_deeper_traceback()
                print(clean_traceback(error_traceback))
            return False

    def clear(self, selector_type: SelectorType, selector: str, skip_wait: bool = False, timeout: int = 10, interactable_timeout: int = 10, suppress_traceback: bool = False, raise_exc: bool = False) -> bool:
        """
        Clear the text in an element.
        
        Args:
            selector_type (SelectorType): The type of selector (XPATH or CSS).
            selector (str): The selector string.
            skip_wait (bool): Whether to skip waiting for the element.
            timeout (int): The maximum time to wait for the element.
            interactable_timeout (int): The maximum time to wait for the element to be interactable.
            suppress_traceback (bool): Whether to suppress the traceback print.
            raise_exc (bool): Whether to re-raise the exception.
        Returns:
            bool: True if the element is successfully cleared, False otherwise.
        """
        try:
            element = self.find_element(selector_type, selector, skip_wait, timeout, suppress_traceback, raise_exc)
            if element:
                if interactable_timeout != -1:
                    WebDriverWait(self.driver, interactable_timeout).until(EC.element_to_be_clickable((By.XPATH, selector)))
                element.clear()
                return True
            return False
        except Exception:
            if raise_exc:
                raise
            if not suppress_traceback:
                error_traceback = format_deeper_traceback()
                print(clean_traceback(error_traceback))
            return False

    def hover(self, selector_type: SelectorType, selector: str, skip_wait: bool = False, timeout: int = 10, suppress_traceback: bool = False, raise_exc: bool = False) -> bool:
        """
        Hover over an element.
        
        Args:
            selector_type (SelectorType): The type of selector (XPATH or CSS).
            selector (str): The selector string.
            skip_wait (bool): Whether to skip waiting for the element.
            timeout (int): The maximum time to wait for the element.
            suppress_traceback (bool): Whether to suppress the traceback print.
            raise_exc (bool): Whether to re-raise the exception.

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
        except Exception:
            if raise_exc:
                raise
            if not suppress_traceback:
                error_traceback = format_deeper_traceback()
                print(clean_traceback(error_traceback))
            return False

    def extract(self, selector_type: Optional[SelectorType] = None, selector: Optional[str] = None, element: Optional[WebElement] = None, attribute: Optional[str] = None, skip_wait: bool = False, timeout: int = 10, suppress_traceback: bool = False, raise_exc: bool = False) -> Optional[str]:
        """
        Extract data from an element.
        
        Args:
            selector_type (SelectorType): The type of selector (XPATH or CSS).
            selector (str): The selector string.
            element (WebElement): The WebElement object to extract data from.
            attribute (str): The attribute to extract. Use "__text__" to extract the text content.
            skip_wait (bool): Whether to skip waiting for the element.
            timeout (int): The maximum time to wait for the element.
            suppress_traceback (bool): Whether to suppress the traceback print.
            raise_exc (bool): Whether to re-raise the exception.
        
        Returns:
            str: The extracted data, or False if extraction does not succeed, and None if extraction errors.
        """
        try:
            if element and selector_type and selector:
                if selector_type == SelectorType.XPATH: 
                    sub_element = element.find_element(By.XPATH, selector)
                elif selector_type == SelectorType.CSS:
                    sub_element = element.find_element(By.CSS_SELECTOR, selector)
                else:
                    raise ValueError(f"Unsupported selector type: {selector_type}")
            else:
                sub_element = element or self.find_element(selector_type, selector, skip_wait, timeout, suppress_traceback, raise_exc)
            
            if sub_element:
                if attribute == "__text__":
                    return sub_element.text
                elif attribute:
                    return sub_element.get_attribute(attribute)
                else:
                    return sub_element.text
            return False
        except Exception:
            if raise_exc:
                raise
            if not suppress_traceback:
                error_traceback = format_deeper_traceback()
                print(clean_traceback(error_traceback))
            return None

    def run_js(self, selector_type: SelectorType, selector: str, script: str, skip_wait: bool = False, timeout: int = 10, suppress_traceback: bool = False, raise_exc: bool = False) -> Optional[Any]:
        """
        Run JavaScript on an element.
        
        Args:
            selector_type (SelectorType): The type of selector (XPATH or CSS).
            selector (str): The selector string.
            script (str): The JavaScript code to run.
            skip_wait (bool): Whether to skip waiting for the element.
            timeout (int): The maximum time to wait for the element.
            suppress_traceback (bool): Whether to suppress the traceback print.
            raise_exc (bool): Whether to re-raise the exception.
        
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
        except Exception:
            if raise_exc:
                raise
            if not suppress_traceback:
                error_traceback = format_deeper_traceback()
                print(clean_traceback(error_traceback))
            return None

    def get_page_title(self, suppress_traceback: bool = False, raise_exc: bool = False) -> Optional[str]:
        """
        Get the title of the page.
        
        Returns:
            str: The page title, or None if retrieval fails.
        """
        try:
            return self.driver.title
        except Exception:
            if raise_exc:
                raise
            if not suppress_traceback:
                error_traceback = format_deeper_traceback()
                print(clean_traceback(error_traceback))
            return None

    def get_page_source(self, suppress_traceback: bool = False, raise_exc: bool = False) -> Optional[str]:
        """
        Get the source code of the page.
        
        Returns:
            str: The page source, or None if retrieval fails.
        """
        try:
            return self.driver.page_source
        except Exception:
            if raise_exc:
                raise
            if not suppress_traceback:
                error_traceback = format_deeper_traceback()
                print(clean_traceback(error_traceback))
            return None

    def get_current_url(self, suppress_traceback: bool = False, raise_exc: bool = False) -> Optional[str]:
        """
        Get the current URL of the page.
        
        Returns:
            str: The current URL, or None if retrieval fails.
        """
        try:
            return self.driver.current_url
        except Exception:
            if raise_exc:
                raise
            if not suppress_traceback:
                error_traceback = format_deeper_traceback()
                print(clean_traceback(error_traceback))
            return None

    def scroll(self, direction: str = "down", amount: Optional[int] = None, selector_type: Optional[SelectorType] = None, selector: Optional[str] = None, x: Optional[int] = None, y: Optional[int] = None, to_end: bool = False, timeout: int = 10, suppress_traceback: bool = False, raise_exc: bool = False) -> bool:
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
            suppress_traceback (bool): Whether to suppress the traceback print.
            raise_exc (bool): Whether to re-raise the exception.
        
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
                    element = self.find_element(selector_type, selector, timeout=timeout, suppress_traceback=suppress_traceback, raise_exc=raise_exc)
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
                    element = self.find_element(selector_type, selector, timeout=timeout, suppress_traceback=suppress_traceback, raise_exc=raise_exc)
                    if element:
                        if to_end:
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                        else:
                            self.driver.execute_script("arguments[0].scrollIntoView();", element)
                else:
                    self.driver.execute_script("window.scrollTo(0, 0);")
            elif direction == "to_element" and selector_type and selector:
                element = self.find_element(selector_type, selector, timeout=timeout, suppress_traceback=suppress_traceback, raise_exc=raise_exc)
                if element:
                    self.driver.execute_script("arguments[0].scrollIntoView();", element)
            else:
                raise ValueError("Invalid scroll parameters")
            return True
        except Exception:
            if raise_exc:
                raise
            if not suppress_traceback:
                error_traceback = format_deeper_traceback()
                print(clean_traceback(error_traceback))
            return False

    def go_to(self, url: str, suppress_traceback: bool = False, raise_exc: bool = False) -> None:
        """
        Navigate to a URL.
        
        Args:
            url (str): The URL to navigate to.
            suppress_traceback (bool): Whether to suppress the traceback print.
            raise_exc (bool): Whether to re-raise the exception.
        """
        try:
            self.driver.get(url)
        except Exception:
            if raise_exc:
                raise
            if not suppress_traceback:
                error_traceback = format_deeper_traceback()
                print(clean_traceback(error_traceback))

    def refresh(self, suppress_traceback: bool = False, raise_exc: bool = False) -> None:
        """
        Refresh the current page.
        
        Args:
            suppress_traceback (bool): Whether to suppress the traceback print.
            raise_exc (bool): Whether to re-raise the exception.
        """
        try:
            self.driver.refresh()
        except Exception:
            if raise_exc:
                raise
            if not suppress_traceback:
                error_traceback = format_deeper_traceback()
                print(clean_traceback(error_traceback))

    def back(self, suppress_traceback: bool = False, raise_exc: bool = False) -> None:
        """
        Navigate back in the browser history.
        
        Args:
            suppress_traceback (bool): Whether to suppress the traceback print.
            raise_exc (bool): Whether to re-raise the exception.
        """
        try:
            self.driver.back()
        except Exception:
            if raise_exc:
                raise
            if not suppress_traceback:
                error_traceback = format_deeper_traceback()
                print(clean_traceback(error_traceback))

    def forward(self, suppress_traceback: bool = False, raise_exc: bool = False) -> None:
        """
        Navigate forward in the browser history.
        
        Args:
            suppress_traceback (bool): Whether to suppress the traceback print.
            raise_exc (bool): Whether to re-raise the exception.
        """
        try:
            self.driver.forward()
        except Exception:
            if raise_exc:
                raise
            if not suppress_traceback:
                error_traceback = format_deeper_traceback()
                print(clean_traceback(error_traceback))

    def show_structure(self, element: Optional[WebElement] = None, selector_type: Optional[SelectorType] = None, selector: Optional[str] = None, indent: int = 0, suppress_traceback: bool = False, raise_exc: bool = False, save_to_file: bool = False, file_path: str = "structure_output.html") -> None:
        """
        Recursively print the structure of the DOM starting from the given element or selector.
        
        Args:
            element (WebElement): The root element to start the structure display.
            selector_type (SelectorType): The type of selector (XPATH or CSS).
            selector (str): The selector string.
            indent (int): The current indentation level for nested elements.
            suppress_traceback (bool): Whether to suppress the traceback print.
            raise_exc (bool): Whether to re-raise the exception.
            save_to_file (bool): Whether to save the output to a file.
            file_path (str): The file path to save the output if save_to_file is True.
        """
        try:
            output = []

            def _show_structure(element, indent):
                indent_str = ' ' * (indent * 2)
                tag_name = element.tag_name
                attributes = ' '.join([f'{attr["name"]}="{attr["value"]}"' for attr in element.get_property('attributes')])
                text = element.text.strip()
                line = f"{indent_str}<{tag_name} {attributes}> {text}"
                output.append(line)
                print(line)

                children = element.find_elements(By.XPATH, './*')
                for child in children:
                    _show_structure(child, indent + 1)

            # Determine the root element to start from
            if element and selector_type and selector:
                if selector_type == SelectorType.XPATH:
                    root_element = element.find_element(By.XPATH, selector)
                elif selector_type == SelectorType.CSS:
                    root_element = element.find_element(By.CSS_SELECTOR, selector)
                else:
                    raise ValueError(f"Unsupported selector type: {selector_type}")
            else:
                root_element = element or self.find_element(selector_type, selector)
            
            if not root_element:
                print("Root element not found.")
                return

            _show_structure(root_element, indent)

            if save_to_file:
                with open(file_path, 'w') as file:
                    file.write("\n".join(output))

        except Exception as e:
            if raise_exc:
                raise
            if not suppress_traceback:
                error_traceback = format_deeper_traceback()
                print(clean_traceback(error_traceback))
                print(f"Error displaying structure: {e}")





    def generate_structure_html(self, elements: Union[WebElement, List[WebElement]], file_path: str = "structure_visualization.html", suppress_traceback: bool = False, raise_exc: bool = False) -> None:
        """
        Generate a dynamic HTML page to visualize the DOM structure starting from the given element or selector.
        
        Args:
            elements (Union[WebElement, List[WebElement]]): The root element(s) to start the structure display.
            file_path (str): The file path to save the output HTML file.
            suppress_traceback (bool): Whether to suppress the traceback print.
            raise_exc (bool): Whether to re-raise the exception.
        """
        try:
            output = []
            element_id = 0

            def _generate_structure(element, indent):
                nonlocal element_id
                indent_str = ' ' * (indent * 2)
                tag_name = element.tag_name
                attributes = ' '.join([f'{attr["name"]}="{attr["value"]}"' for attr in element.get_property('attributes')])
                text = element.text.strip()
                element_id += 1
                element_id_str = f"element-{element_id}"
                children_id_str = f"{element_id_str}-children"
                divider_id_str = f"{element_id_str}-divider"
                line = f"""
                {indent_str}<div class='element' id='{element_id_str}' data-tag='{tag_name}' data-attributes='{attributes}' data-text='{text}'>
                    <span class='toggle' onclick="toggleVisibility('{children_id_str}', '{divider_id_str}', this)">&#9660;</span>
                    <span class='tag'>&lt;{tag_name} {attributes}&gt;</span> {text}
                    <div class='selectors'>
                        <button onclick="copyCssSelector('{element_id_str}')">Copy CSS Selector</button>
                        <button onclick="copyAttributes('{element_id_str}')">Copy Attributes</button>
                    </div>
                    <div id='{children_id_str}' class='children'>
                """
                output.append(line)

                children = element.find_elements(By.XPATH, './*')
                for child in children:
                    _generate_structure(child, indent + 1)

                closing_tag = f"{indent_str}</div>\n{indent_str}&lt;/{tag_name}&gt;</div><hr class='divider' id='{divider_id_str}'>"
                output.append(closing_tag)

            # Determine the root elements to start from
            if isinstance(elements, list):
                root_elements = elements
            else:
                root_elements = [elements]

            # Initialize tqdm progress bar if installed
            if tqdm_installed:
                progress_bar = tqdm(total=len(root_elements), desc="Generating structure", unit="element")
            else:
                progress_bar = None

            for root_element in root_elements:
                if not root_element:
                    print("Root element not found.")
                    return

                # Generate structure for the root element and its immediate children
                _generate_structure(root_element, 0)

                # Update progress bar if tqdm is installed
                if progress_bar:
                    progress_bar.update(1)

            # Close the progress bar if tqdm is installed
            if progress_bar:
                progress_bar.close()

            # HTML template for the visualization
            html_template = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>DOM Structure Visualization</title>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    .element {{ margin-left: 20px; position: relative; }}
                    .tag {{ color: blue; cursor: pointer; }}
                    .tag:hover {{ text-decoration: underline; }}
                    .attributes {{ color: red; }}
                    .text {{ color: green; }}
                    .hidden {{ display: none; }}
                    .highlight {{ background-color: yellow; }}
                    .code-container {{ border-bottom: 1px solid #ccc; padding-bottom: 10px; }}
                    .real-dom-container {{ padding-top: 10px; }}
                    .selectors {{ position: absolute; right: 0; top: 0; }}
                    .selectors button {{ margin-left: 5px; }}
                    .children {{ margin-left: 20px; }}
                    .toggle {{ cursor: pointer; font-weight: bold; }}
                    .divider {{ border-top: 1px solid #ccc; margin: 10px 0; }}
                    .search-bar {{ margin-bottom: 20px; }}
                </style>
                <script>
                    function copyToClipboard(text) {{
                        navigator.clipboard.writeText(text).then(() => {{
                            alert('Copied to clipboard: ' + text);
                        }}, (err) => {{
                            console.error('Could not copy text: ', err);
                        }});
                    }}

                    function copyCssSelector(elementId) {{
                        const element = document.getElementById(elementId);
                        const classList = element.getAttribute('data-attributes').match(/class="([^"]*)"/);
                        if (classList) {{
                            const cssSelector = '.' + classList[1].split(' ').join('.');
                            copyToClipboard(cssSelector);
                        }} else {{
                            alert('No class attribute found.');
                        }}
                    }}

                    function copyAttributes(elementId) {{
                        const element = document.getElementById(elementId);
                        const attributes = element.getAttribute('data-attributes');
                        copyToClipboard(attributes);
                    }}

                    function toggleVisibility(childrenId, dividerId, toggleElement) {{
                        const children = document.getElementById(childrenId);
                        const divider = document.getElementById(dividerId);
                        if (children && divider) {{
                            if (children.style.display === 'none') {{
                                children.style.display = 'block';
                                divider.style.display = 'block';
                                toggleElement.innerHTML = '&#9660;';
                            }} else {{
                                children.style.display = 'none';
                                divider.style.display = 'none';
                                toggleElement.innerHTML = '&#9654;';
                            }}
                        }} else {{
                            console.error('Children or divider not found for IDs:', childrenId, dividerId);
                        }}
                    }}

                    function filterElements() {{
                        const searchTerm = document.getElementById('search-input').value.toLowerCase();
                        document.querySelectorAll('.element').forEach(element => {{
                            const text = element.getAttribute('data-text').toLowerCase();
                            const tag = element.getAttribute('data-tag').toLowerCase();
                            const attributes = element.getAttribute('data-attributes').toLowerCase();
                            if (text.includes(searchTerm) || tag.includes(searchTerm) || attributes.includes(searchTerm)) {{
                                element.style.display = 'block';
                            }} else {{
                                element.style.display = 'none';
                            }}
                        }});
                    }}

                    document.addEventListener('DOMContentLoaded', () => {{
                        document.querySelectorAll('.tag').forEach(tag => {{
                            tag.addEventListener('mouseover', () => {{
                                const elementId = tag.parentElement.id;
                                const realElement = document.querySelector(`[data-element-id='${{elementId}}']`);
                                if (realElement) {{
                                    realElement.classList.add('highlight');
                                }}
                            }});
                            tag.addEventListener('mouseout', () => {{
                                const elementId = tag.parentElement.id;
                                const realElement = document.querySelector(`[data-element-id='${{elementId}}']`);
                                if (realElement) {{
                                    realElement.classList.remove('highlight');
                                }}
                            }});
                        }});
                    }});
                </script>
            </head>
            <body>
                <h1>DOM Structure Visualization</h1>
                <div class="search-bar">
                    <input type="text" id="search-input" onkeyup="filterElements()" placeholder="Search for elements...">
                </div>
                <div class="code-container">{''.join(output)}</div>
                <div class="real-dom-container">
                    {''.join([root_element.get_attribute('outerHTML') for root_element in root_elements])}
                </div>
            </body>
            </html>
            """

            # Save the HTML to a file
            with open(file_path, 'w') as file:
                file.write(html_template)

            print(f"Structure visualization saved to {file_path}")

        except Exception as e:
            if raise_exc:
                raise
            if not suppress_traceback:
                error_traceback = format_deeper_traceback()
                print(clean_traceback(error_traceback))
            print(f"Error generating structure HTML: {e}")





    def get_xpath(self, element: WebElement, timeout: int = 10, suppress_traceback: bool = False, raise_exc: bool = False) -> str:
        """
        Generate the XPath for a given element.
        
        Args:
            element (WebElement): The element to generate the XPath for.
            timeout (int): The maximum time to attempt generating the XPath.
            suppress_traceback (bool): Whether to suppress the traceback print.
            raise_exc (bool): Whether to re-raise the exception.
        
        Returns:
            str: The XPath of the element.
        """
        start_time = time.time()
        try:
            components = []
            child = element
            while child is not None:
                if time.time() - start_time > timeout:
                    raise TimeoutError("Timeout while generating XPath.")
                parent = child.find_element(By.XPATH, '..')
                children = parent.find_elements(By.XPATH, './*')
                index = 1
                for i, sibling in enumerate(children):
                    if sibling == child:
                        index = i + 1
                        break
                components.append(f"{child.tag_name}[{index}]")
                child = parent if parent.tag_name.lower() != 'html' else None
            components.reverse()
            return '/' + '/'.join(components)
        except Exception as e:
            if raise_exc:
                raise
            if not suppress_traceback:
                error_traceback = format_deeper_traceback()
                print(clean_traceback(error_traceback))
            print(f"Error generating XPath: {e}")
            return ""
        

    def get_css_selector(self, element: WebElement, suppress_traceback: bool = False, raise_exc: bool = False) -> str:
        """
        Generate the CSS selector for a given element.
        
        Args:
            element (WebElement): The element to generate the CSS selector for.
        
        Returns:
            str: The CSS selector of the element.
        """
        try:
            path = []
            while element:
                sub_selector = element.tag_name
                if element.get_attribute('id'):
                    sub_selector += f"#{element.get_attribute('id')}"
                elif element.get_attribute('class'):
                    sub_selector += f".{'.'.join(element.get_attribute('class').split())}"
                siblings = element.find_elements(By.XPATH, f"./preceding-sibling::{element.tag_name}")
                if len(siblings) > 0:
                    sub_selector += f":nth-of-type({len(siblings) + 1})"
                path.insert(0, sub_selector)
                element = element.find_element(By.XPATH, '..') if element.tag_name.lower() != 'html' else None
            return ' > '.join(path)
        except Exception as e:
            if raise_exc:
                raise
            if not suppress_traceback:
                error_traceback = format_deeper_traceback()
                print(clean_traceback(error_traceback))
            print(f"Error generating CSS selector: {e}")
            return ""


    def class_to_css_selector(self, class_attr: str) -> str:
        """
        Convert a space-separated class attribute string to a CSS selector format.
        
        Args:
            class_attr (str): The class attribute string from the browser.
        
        Returns:
            str: The CSS selector format of the class attribute.
        """
        classes = class_attr.split()
        css_selector = '.' + '.'.join(classes)
        return css_selector




    def find_elements_by_attributes(self, attributes: str, suppress_traceback: bool = False, raise_exc: bool = False) -> List[WebElement]:
        """
        Find elements by their attributes.
        
        Args:
            attributes (str): The attributes string in either Selenium's format or browser format.
            suppress_traceback (bool): Whether to suppress the traceback print.
            raise_exc (bool): Whether to re-raise the exception.
        
        Returns:
            List[WebElement]: A list of elements matching the attributes.
        """
        try:
            # Convert browser format to Selenium format if necessary
            if '=' in attributes and '"' in attributes:
                attributes = self._convert_browser_format_to_selenium(attributes, raise_exc, suppress_traceback)
            
            # Build the XPath expression
            xpath_expression = self._build_xpath_from_attributes(attributes, raise_exc, suppress_traceback)
            
            # Find elements using the XPath expression
            elements = self.driver.find_elements(By.XPATH, xpath_expression)
            return elements
        except InvalidSelectorException as e:
            if raise_exc:
                raise
            if not suppress_traceback:
                error_traceback = format_deeper_traceback()
                print(clean_traceback(error_traceback))
            print(f"Error finding elements by attributes: {e}")
            return []



    def _convert_browser_format_to_selenium(self, attributes: str, raise_exc: bool = False, suppress_traceback: bool = False) -> str:
        """
        Convert browser format attributes to Selenium format.
        
        Args:
            attributes (str): The attributes string in browser format.
            raise_exc (bool): Whether to re-raise the exception.
            suppress_traceback (bool): Whether to suppress the traceback print.
        
        Returns:
            str: The attributes string in Selenium format.
        """
        try:
            # Split the attributes string by spaces
            parts = attributes.split('" ')
            selenium_attributes = []
            for part in parts:
                if '=' in part:
                    key, value = part.split('=', 1)
                    value = value.strip('"')
                    selenium_attributes.append(f'{key}="{value}"')
            return ' '.join(selenium_attributes)
        except Exception as e:
            if raise_exc:
                raise
            if not suppress_traceback:
                error_traceback = format_deeper_traceback()
                print(clean_traceback(error_traceback))
            print(f"Error converting browser format to Selenium format: {e}")
            return ""

    def _build_xpath_from_attributes(self, attributes: str, raise_exc: bool = False, suppress_traceback: bool = False) -> str:
        """
        Build an XPath expression from the attributes string.
        
        Args:
            attributes (str): The attributes string in Selenium format.
            raise_exc (bool): Whether to re-raise the exception.
            suppress_traceback (bool): Whether to suppress the traceback print.
        
        Returns:
            str: The XPath expression.
        """
        try:
            # Split the attributes string by spaces
            parts = attributes.split(' ')
            conditions = []
            for part in parts:
                if '=' in part:
                    key, value = part.split('=', 1)
                    # Handle quotes in the value
                    if '"' in value:
                        conditions.append(f'contains(@{key}, "{value.replace("\"", "")}")')
                    else:
                        conditions.append(f'@{key}="{value}"')
            xpath_expression = f'//*[{ " and ".join(conditions) }]'
            return xpath_expression
        except Exception as e:
            if raise_exc:
                raise
            if not suppress_traceback:
                error_traceback = format_deeper_traceback()
                print(clean_traceback(error_traceback))
            print(f"Error building XPath from attributes: {e}")
            return ""
        

    def find_elements_by_tag(self, tag: str, suppress_traceback: bool = False, raise_exc: bool = False) -> List[WebElement]:
        """
        Find an elements by its tag name.
        
        Args:
            tag (str): The tag name of the element.
        
        Returns:
            List[WebElement]: The elements with the specified tag name.
        """
        try:
            elements = self.driver.find_elements(By.TAG_NAME, tag)
            return elements
        except Exception as e:
            if raise_exc:
                raise
            if not suppress_traceback:
                error_traceback = format_deeper_traceback()
                print(clean_traceback(error_traceback))
                print(f"Error finding element by tag: {e}")
            return []

