from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

'''this test checks valid input for zip code field'''


def get_driver():
    # location of chrome driver for windows
    chromedriver = "D:/Selenium-Drivers/Chrome-Driver/chromedriver_win32/chromedriver"
    return webdriver.Chrome(chromedriver)


def clear(field_list):
    for field in field_list:
        field.clear()


def distance_valid_test():
    driver = get_driver()  # web driver component
    sleep(5)  # wait 5 seconds for elements to load on page before searching for them
    driver.maximize_window()
    driver.get("https://skudar.pythonanywhere.com/")  # launch web app
    sleep(5)

    # grab field components
    field_list = driver.find_elements_by_tag_name('input')
    clear(field_list)  # clear field inputs
    field_list[1].send_keys('1')  # distance input
    sleep(3)
    field_list[0].send_keys('90242')  # zipcode input
    field_list[2].send_keys('water bottle')  # item input
    sleep(3)  # pause for 3 seconds to show inputs in fields

    # click search button
    search_btn = driver.find_element_by_xpath("//button")
    search_btn.click()

    sleep(6)
    driver.close()  # close window


if __name__ == "__main__":
    distance_valid_test()
