# Import the WebSession class
from web_actions import WebSession
from web_actions import SelectorType
import time
import json
import requests
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
    "name2": 'p-name vcard-fullname d-block overflow-hidden',
    "username": '/html/body/div[1]/div[4]/main/div[2]/div/div[1]/div/div[2]/div[1]/div[2]/h1/span[2]',
    "username2": 'p-nickname vcard-username d-block',
    "bio": '/html/body/div[1]/div[4]/main/div[2]/div/div[1]/div/div[2]/div[3]/div[2]/div[1]',
    "repositories": '//*[@id="js-pjax-container"]/div[2]/div[1]/div[2]/div[1]/div[1]/div/h2/a/span',
    "repo_name": "repo",
    "repo_description": 'pinned-item-desc color-fg-muted text-small mt-2',
    "repo_language": 'd-inline-block mr-3',
    "repo_stars": 'pinned-item-meta Link--muted',
    "repo_forks": '//a[contains(@href,"/fork")]',
    "repo_container": "mb-3 d-flex flex-content-stretch col-12 col-md-6 col-lg-6",
    "repo_container2": '//*[@id="user-profile-frame"]/div/div[2]/div/ol/li[1]'
}



# Navigate to the GitHub profile
profile_url = "https://github.com/nguyenvanhuan243"

session.go_to(profile_url)
# Extract the username from the profile URL
username = profile_url.split('/')[-1]
readme_content = ""

branches = ["main", "master"]
for branch in branches:
    readme_url = f"https://raw.githubusercontent.com/{username}/{username}/refs/heads/{branch}/README.md"
   
    response = requests.get(readme_url)
    if response.status_code == 200:
        readme_content = response.text
        break

# save readme content to file
with open("README.md", "w") as f:
    f.write(readme_content)

#time.sleep(3)

# convert class name to css selector
name2_selector = session.class_to_css_selector(selectors["name2"])
username2_selector = session.class_to_css_selector(selectors["username2"])

repo_description_selector = session.class_to_css_selector(selectors["repo_description"])
repo_selector = session.class_to_css_selector(selectors["repo_container"])
#repo2_selector = session.class_to_css_selector(selectors["repo_container2"])

repo_language_selector = session.class_to_css_selector(selectors["repo_language"])
repo_stars_selector = session.class_to_css_selector(selectors["repo_stars"])



try:
    repo_elements = session.find_elements(SelectorType.CSS, repo_selector, timeout=5, raise_exc=True)
    if not repo_elements:
        raise Exception("No repository elements found")
except Exception:
    repo_elements = session.find_elements(SelectorType.XPATH, selectors["repo_container2"], timeout=5, raise_exc=True)



# Wait for the profile name element to be present

try:
    name = session.extract(selector_type=SelectorType.XPATH, selector=selectors["name"], timeout=5, raise_exc=True)
except Exception:
    try:
        name = session.extract(selector_type=SelectorType.CSS, selector=name2_selector, timeout=5, raise_exc=True)
    except Exception:
        name = ""

try:
    username = session.extract(selector_type=SelectorType.XPATH, selector=selectors["username"], timeout=5, raise_exc=True)
except Exception:
    try:
        username = session.extract(selector_type=SelectorType.CSS, selector=username2_selector, timeout=5, raise_exc=True)
    except Exception:
        username = ""


try:
    bio = session.extract(selector_type=SelectorType.XPATH, selector=selectors["bio"], timeout=5, raise_exc=True)
except Exception:
    bio = ""

# Extract and organize the repository information
repositories = []
for element in repo_elements:
    repo_name = session.extract(element=element, selector_type=SelectorType.CLASS_NAME, selector=selectors["repo_name"], skip_wait=True)
    repo_description = session.extract(element=element, selector_type=SelectorType.CSS, selector=repo_description_selector, skip_wait=True)
    try:
        repo_language = session.extract(element=element, selector_type=SelectorType.CSS, selector=repo_language_selector, skip_wait=True, raise_exc=True)
    except Exception:
        repo_language = ""
    repo_stars = session.extract(element=element, selector_type=SelectorType.CSS, selector=repo_stars_selector, skip_wait=True)
   # fork_element = session.find_element(SelectorType.XPATH, selectors["repo_forks"])
   #text = fork_element.text
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