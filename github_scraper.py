# Import the WebSession class
from web_actions import WebSession
from web_actions import SelectorType
import time
import json

# Define the options for the WebSession
options = {
    "headless": False,
    "incognito": False,
    "disable-gpu": False,
    "window-size": "1920,1080",
    "user-data-dir": "userdata"
}

# Initialize the WebSession object with options
session = WebSession(options=options)

selectors = {
    "name": '/html/body/div[1]/div[4]/main/div[2]/div/div[1]/div/div[2]/div[1]/div[2]/h1/span[1]',
    "username": '/html/body/div[1]/div[4]/main/div[2]/div/div[1]/div/div[2]/div[1]/div[2]/h1/span[2]',
    "bio": '/html/body/div[1]/div[4]/main/div[2]/div/div[1]/div/div[2]/div[3]/div[2]/div[1]',
    "repositories": '//*[@id="js-pjax-container"]/div[2]/div[1]/div[2]/div[1]/div[1]/div/h2/a/span',
    "repo_name": "repo",
    "repo_description": 'pinned-item-desc color-fg-muted text-small mt-2 mb-0',
    "repo_language": 'd-inline-block mr-3',
    "repo_stars": 'pinned-item-meta Link--muted',
    "repo_forks": '//a[contains(@href,"/fork")]',
    "repo_container": "mb-3 d-flex flex-content-stretch col-12 col-md-6 col-lg-6"
}



# Navigate to the GitHub profile
profile_url = "https://github.com/Silenttttttt"
session.go_to(profile_url)

#time.sleep(3)

repo_description_selector = session.class_to_css_selector(selectors["repo_description"])
repo_selector = session.class_to_css_selector(selectors["repo_container"])
repo_language_selector = session.class_to_css_selector(selectors["repo_language"])
repo_stars_selector = session.class_to_css_selector(selectors["repo_stars"])
repo_elements = session.find_elements(SelectorType.CSS, repo_selector)


# Wait for the profile name element to be present
name = session.extract(selector_type=SelectorType.XPATH, selector=selectors["name"], timeout=5)
username = session.extract(selector_type=SelectorType.XPATH, selector=selectors["username"], timeout=5)
try:
    bio = session.extract(selector_type=SelectorType.XPATH, selector=selectors["bio"], timeout=5, raise_exc=True)
except Exception:
    bio = ""

# Extract and organize the repository information
repositories = []
for element in repo_elements:
    repo_name = session.extract(element=element, selector_type=SelectorType.CLASS_NAME, selector=selectors["repo_name"], skip_wait=True)
    repo_description = session.extract(element=element, selector_type=SelectorType.CSS, selector=repo_description_selector, skip_wait=True)
    repo_language = session.extract(element=element, selector_type=SelectorType.CSS, selector=repo_language_selector, skip_wait=True)
    repo_stars = session.extract(element=element, selector_type=SelectorType.CSS, selector=repo_stars_selector, skip_wait=True)
  #  fork_element = session.find_element(SelectorType.XPATH, selectors["repo_forks"])
 #   session.modify_element(fork_element, text="69")
    repo_forks = session.extract(element=element, selector_type=SelectorType.XPATH, selector=selectors["repo_forks"], skip_wait=True)
    
    repository = {
        "name": repo_name,
        "description": repo_description,
        "language": repo_language,
        "stars": repo_stars,
        "forks": repo_forks
    }
    repositories.append(repository)

data = {
    "profile_name": name,
    "bio": bio,
    "repositories": repositories
}

# Save data to json
with open('github_profile.json', 'w') as f:
    json.dump(data, f, indent=4)

# Uncomment the following line to enter debug mode
# session.debug()

# Close the browser session
session.close()