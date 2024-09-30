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
    "name": '//*[@id="ember41"]',
    "headline": '//*[@id="profile-content"]/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[2]',
    "about": '//*[@id="profile-content"]/div/div[2]/div/div/main/section[4]/div[3]/div/div/div/span[1]',
    "experience": '//*[@id="profile-content"]/div/div[2]/div/div/main/section[8]/div[3]/ul/li[1]',
    "experience_title": '//*[@id="profile-content"]/div/div[2]/div/div/main/section[8]/div[3]/ul/li[1]/div/div[2]/div[1]/div/div/div/div/div/span[1]',
    "experience_company": '//*[@id="profile-content"]/div/div[2]/div/div/main/section[8]/div[3]/ul/li[2]/div/div[2]/div[1]/div/span[1]/span[1]',
    "experience_date_range": '//*[@id="profile-content"]/div/div[2]/div/div/main/section[8]/div[3]/ul/li[1]/div/div[2]/div[1]/div/span[2]/span[1]',
    "experience_location": '//*[@id="profile-content"]/div/div[2]/div/div/main/section[8]/div[3]/ul/li[2]/div/div[2]/div[1]/div/span[3]/span[1]',
    "experience_description": '//*[@id="profile-content"]/div/div[2]/div/div/main/section[8]/div[3]/ul/li[1]/div/div[2]/div[2]/ul/li[1]/div/ul/li/div/div/div/div/span[1]',
    "experiences_container": '//*[@id="profile-content"]/div/div[2]/div/div/main/section[8]/div[3]/ul',
    "repo_container": '//*[@id="user-profile-frame"]/div/div[2]/div/ol/li[1]/div'
}

# Navigate to the LinkedIn profile
# profile_url = "https://www.linkedin.com/in/muni-besen/"
# session.go_to(profile_url)
# time.sleep(5)

# # Wait for the profile name element to be present
# name = session.extract(SelectorType.XPATH, selectors["name"], timeout=5)
# headline = session.extract(SelectorType.XPATH, selectors["headline"], timeout=5)
# about = session.extract(SelectorType.XPATH, selectors["about"], timeout=5)
# first_experience_element = session.find_element(SelectorType.XPATH, selectors["experiences_container"], timeout=5)

# Use the new method to find all similar experience elements
#experience_elements = session.find_similar_elements(element=first_experience_element)

#xpath = session.get_xpath(first_experience_element)
#print(xpath)

session.go_to("https://github.com/Silenttttttt")

#repo_elements = session.find_elements_by_attributes('class="Box d-flex p-3 width-full public source"')


#body = session.find_elements_by_tag('body')
elements_selector = session.class_to_css_selector("mb-3 d-flex flex-content-stretch sortable-button-item pinned-item-list-item js-pinned-item-list-item col-12 col-md-6 col-lg-6")

# elements = session.find_elements(SelectorType.CSS, elements_selector)

# for element in elements:
#     print(element.text)


#session.generate_structure_html(body, file_path="body_structure.html")


elements = session.find_elements(SelectorType.CSS, elements_selector)

session.generate_structure_html(elements)

for element in elements:
    text = element.text
    if text:
        print(element.text)
#session.generate_structure_html(selector_type=SelectorType.XPATH, selector=selectors["repo_container"], file_path="experience_structure.html")

#session.show_structure(first_experience_element, save_to_file=True)

session.debug()
# Extract and organize the experience information
experiences = []
for element in experience_elements:
    print(element.text if "freelance" not in element.text.lower() else "")
    title = session.extract(element=element, selector_type=SelectorType.XPATH, selector=selectors["experience_title"], skip_wait=True)
    company = session.extract(element=element, selector_type=SelectorType.XPATH, selector=selectors["experience_company"], skip_wait=True)
    date_range = session.extract(element=element, selector_type=SelectorType.XPATH, selector=selectors["experience_date_range"], skip_wait=True)
    location = session.extract(element=element, selector_type=SelectorType.XPATH, selector=selectors["experience_location"], skip_wait=True)
    description = session.extract(element=element, selector_type=SelectorType.XPATH, selector=selectors["experience_description"], skip_wait=True)
    
    experience = {
        "title": title,
        "company": company,
        "date_range": date_range,
        "location": location,
        "description": description
    }
    experiences.append(experience)
    print(element.text)

# Print the extracted information
print(f"Profile Name: {name}")
print(f"Headline: {headline}")
print(f"About: {about}")
print("Experience:")
for idx, exp in enumerate(experiences, start=1):
    print(f"{idx}. Title: {exp['title']}")
    print(f"   Company: {exp['company']}")
    print(f"   Date Range: {exp['date_range']}")
    print(f"   Location: {exp['location']}")
    print(f"   Description: {exp['description']}\n")

# Save the extracted information to a JSON file
with open('linkedin_profile.json', 'w') as f:
    json.dump({
        "name": name,
        "headline": headline,
        "about": about,
        "experiences": experiences
    }, f, indent=4)

# Uncomment the following line to enter debug mode
# session.debug()

# Close the browser session
session.close()