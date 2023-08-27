from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_dropdown_options(driver, dropdown_div_id):
    # Find the dropdown and click on it
    dropdown_div = driver.find_element(By.ID, dropdown_div_id)
    dropdown_div.click()

    # Wait for the dropdown options to load (might need to adjust the waiting conditions)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[id^='option-']"))
        # This is a guess for the CSS selector; you'll need to check the actual options in the HTML.
    )

    # Fetch the dropdown options
    options = driver.find_elements(By.CSS_SELECTOR,
                                   "[id^='option-']")  # Again, adjust this selector based on actual HTML
    return [option.text for option in options if option.text]


def main():
    url = "https://www.carsales.com.au/"
    options = webdriver.ChromeOptions()
    options.headless = False

    with webdriver.Chrome(options=options) as driver:
        driver.get(url)

        # Assuming there's a possible delay for loading, waiting for the dropdown to be clickable
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'search-field-make'))
        )

        makes = get_dropdown_options(driver, "search-field-make")
        print(makes)  # For testing, later save to file or return


main()
