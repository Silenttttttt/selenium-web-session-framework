import time
from collections import defaultdict
from tqdm import tqdm
from web_actions import WebSession, SelectorType

options = {
    "headless": False,
    "incognito": False,
    "disable-gpu": False,
    "window-size": "1920,1080",
    "user-data-dir": "userdata"
}

session = WebSession(options=options)

profile_url = "https://www.linkedin.com/in/muni-besen/"
session.go_to(profile_url)
time.sleep(3)

first_experience_element = session.find_element(SelectorType.XPATH, '//*[@id="profile-content"]/div/div[2]/div/div/main/section[8]/div[3]/ul')

# Define the comparison methods
comparison_methods = ["tag", "class", "css_selector", "xpath", "attribute:class", "text"]

# Initialize results storage
results = defaultdict(lambda: {"similar": [], "differentish": [], "very_different": [], "same": []})

# Run comparisons 20 times
for i in tqdm(range(20)):
    # Re-fetch the elements to avoid stale element issues
    experience_elements = session.find_similar_elements(element=first_experience_element, match_all_classes=True)
    element_different = session.find_element(SelectorType.XPATH, '//*[@id="ember41"]')

    base_element = experience_elements[0]
    similar_element = experience_elements[1]
    differentish_element = experience_elements[2]
    very_different_element = element_different

    for method in comparison_methods:
        # Compare with similar element
        start_time = time.time()
        result_simple_similar = session.compare_elements(base_element, similar_element, comparison_method=method)
        time_simple_similar = time.time() - start_time
        results[method]["similar"].append((result_simple_similar, time_simple_similar))

        # Compare with different-ish element
        start_time = time.time()
        result_simple_differentish = session.compare_elements(base_element, differentish_element, comparison_method=method)
        time_simple_differentish = time.time() - start_time
        results[method]["differentish"].append((result_simple_differentish, time_simple_differentish))

        # Compare with very different element
        start_time = time.time()
        result_simple_very_different = session.compare_elements(base_element, very_different_element, comparison_method=method)
        time_simple_very_different = time.time() - start_time
        results[method]["very_different"].append((result_simple_very_different, time_simple_very_different))

        # Compare with the same element
        start_time = time.time()
        result_simple_same = session.compare_elements(base_element, base_element, comparison_method=method)
        time_simple_same = time.time() - start_time
        results[method]["same"].append((result_simple_same, time_simple_same))

    # Comprehensive comparison without CSS
    start_time = time.time()
    result_comprehensive_similar = session.comprehensive_comparison(base_element, similar_element, compare_css=False)
    time_comprehensive_similar = time.time() - start_time
    results["comprehensive"]["similar"].append((result_comprehensive_similar, time_comprehensive_similar))

    start_time = time.time()
    result_comprehensive_differentish = session.comprehensive_comparison(base_element, differentish_element, compare_css=False)
    time_comprehensive_differentish = time.time() - start_time
    results["comprehensive"]["differentish"].append((result_comprehensive_differentish, time_comprehensive_differentish))

    start_time = time.time()
    result_comprehensive_very_different = session.comprehensive_comparison(base_element, very_different_element, compare_css=False)
    time_comprehensive_very_different = time.time() - start_time
    results["comprehensive"]["very_different"].append((result_comprehensive_very_different, time_comprehensive_very_different))

    start_time = time.time()
    result_comprehensive_same = session.comprehensive_comparison(base_element, base_element, compare_css=False)
    time_comprehensive_same = time.time() - start_time
    results["comprehensive"]["same"].append((result_comprehensive_same, time_comprehensive_same))

    # Comprehensive comparison with CSS
    start_time = time.time()
    result_comprehensive_css_similar = session.comprehensive_comparison(base_element, similar_element, compare_css=True)
    time_comprehensive_css_similar = time.time() - start_time
    results["comprehensive_css"]["similar"].append((result_comprehensive_css_similar, time_comprehensive_css_similar))

    start_time = time.time()
    result_comprehensive_css_differentish = session.comprehensive_comparison(base_element, differentish_element, compare_css=True)
    time_comprehensive_css_differentish = time.time() - start_time
    results["comprehensive_css"]["differentish"].append((result_comprehensive_css_differentish, time_comprehensive_css_differentish))

    start_time = time.time()
    result_comprehensive_css_very_different = session.comprehensive_comparison(base_element, very_different_element, compare_css=True)
    time_comprehensive_css_very_different = time.time() - start_time
    results["comprehensive_css"]["very_different"].append((result_comprehensive_css_very_different, time_comprehensive_css_very_different))

    start_time = time.time()
    result_comprehensive_css_same = session.comprehensive_comparison(base_element, base_element, compare_css=True)
    time_comprehensive_css_same = time.time() - start_time
    results["comprehensive_css"]["same"].append((result_comprehensive_css_same, time_comprehensive_css_same))

# Calculate averages and generate markdown table
markdown_table = "| Method            | Different Accuracy (%) | Same Accuracy (%) | Avg Time (s) |\n"
markdown_table += "|-------------------|------------------------|-------------------|--------------|\n"

for method, data in results.items():
    different_accuracy = (
        sum(1 for result, _ in data["similar"] if not result) +
        sum(1 for result, _ in data["differentish"] if not result) +
        sum(1 for result, _ in data["very_different"] if not result)
    ) / (len(data["similar"]) + len(data["differentish"]) + len(data["very_different"])) * 100

    same_accuracy = (sum(1 for result, _ in data["same"] if result) / len(data["same"])) * 100

    avg_time = (
        sum(time for _, time in data["similar"]) +
        sum(time for _, time in data["differentish"]) +
        sum(time for _, time in data["very_different"]) +
        sum(time for _, time in data["same"])
    ) / (len(data["similar"]) + len(data["differentish"]) + len(data["very_different"]) + len(data["same"]))

    markdown_table += f"| {method} | {different_accuracy:.2f} | {same_accuracy:.2f} | {avg_time:.6f} |\n"

print(markdown_table)