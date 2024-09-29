from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from enum import Enum

class SelectorType(Enum):
    XPATH = 'xpath'
    CSS = 'css'

class WebSession:
    def __init__(self, headless=False):
        options = webdriver.ChromeOptions()
        options.headless = headless
        self.driver = webdriver.Chrome(options=options)

    def go_to(self, url):
        self.driver.get(url)
        return True

    def wait_for_element(self, selector_type, selector, timeout=10):
        try:
            if selector_type == SelectorType.XPATH:
                return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, selector)))
            elif selector_type == SelectorType.CSS:
                return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            else:
                raise ValueError(f"Unsupported selector type: {selector_type}")
        except Exception as e:
            print(f"Error waiting for element: {e}")
            return None

    def find_element(self, selector_type, selector, skip_wait=False, timeout=10):
        if skip_wait:
            if selector_type == SelectorType.XPATH:
                return self.driver.find_element(By.XPATH, selector)
            elif selector_type == SelectorType.CSS:
                return self.driver.find_element(By.CSS_SELECTOR, selector)
            else:
                raise ValueError(f"Unsupported selector type: {selector_type}")
        else:
            return self.wait_for_element(selector_type, selector, timeout)

    def click(self, selector_type, selector, skip_wait=False, timeout=10):
        try:
            element = self.find_element(selector_type, selector, skip_wait, timeout)
            if element:
                element.click()
                return True
            return False
        except Exception as e:
            print(f"Error clicking element: {e}")
            return False

    def right_click(self, selector_type, selector, skip_wait=False, timeout=10):
        try:
            element = self.find_element(selector_type, selector, skip_wait, timeout)
            if element:
                actions = ActionChains(self.driver)
                actions.context_click(element).perform()
                return True
            return False
        except Exception as e:
            print(f"Error right-clicking element: {e}")
            return False

    def type_text(self, selector_type, selector, text, skip_wait=False, timeout=10):
        try:
            element = self.find_element(selector_type, selector, skip_wait, timeout)
            if element:
                element.send_keys(text)
                return True
            return False
        except Exception as e:
            print(f"Error typing in element: {e}")
            return False

    def clear(self, selector_type, selector, skip_wait=False, timeout=10):
        try:
            element = self.find_element(selector_type, selector, skip_wait, timeout)
            if element:
                element.clear()
                return True
            return False
        except Exception as e:
            print(f"Error clearing element: {e}")
            return False

    def hover(self, selector_type, selector, skip_wait=False, timeout=10):
        try:
            element = self.find_element(selector_type, selector, skip_wait, timeout)
            if element:
                actions = ActionChains(self.driver)
                actions.move_to_element(element).perform()
                return True
            return False
        except Exception as e:
            print(f"Error hovering over element: {e}")
            return False

    def extract(self, selector_type, selector, attribute=None, skip_wait=False, timeout=10):
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
            return None

    def run_js(self, selector_type, selector, script, skip_wait=False, timeout=10):
        try:
            element = self.find_element(selector_type, selector, skip_wait, timeout)
            if element:
                result = self.driver.execute_script(script, element)
                print(f"JavaScript execution result: {result}")
                return result
            return None
        except Exception as e:
            print(f"Error running JavaScript: {e}")
            return None

    def get_current_url(self):
        try:
            return self.driver.current_url
        except Exception as e:
            print(f"Error getting current URL: {e}")
            return None

    def get_page_title(self):
        try:
            return self.driver.title
        except Exception as e:
            print(f"Error getting page title: {e}")
            return None

    def get_page_source(self):
        try:
            return self.driver.page_source
        except Exception as e:
            print(f"Error getting page source: {e}")
            return None

    def close(self):
        self.driver.quit()
        return True