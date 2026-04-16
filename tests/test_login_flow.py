import pytest
from selenium.webdriver.common.by import By # <--- Don't forget this!
from pages.login_page import LoginPage
from utils.data_loader import load_test_data

# Load the data once for the file
data = load_test_data()

def test_successful_login(driver):
    login_page = LoginPage(driver)
    user = data["valid_user"] 
    
    driver.get("https://the-internet.herokuapp.com/login")
    login_page.enter_username(user["username"])
    login_page.enter_password(user["password"])
    login_page.click_login()
    
    assert "Secure Area" in driver.page_source

def test_failed_login(driver):
    login_page = LoginPage(driver)
    user = data["invalid_user"] 
    
    driver.get("https://the-internet.herokuapp.com/login")
    login_page.enter_username(user["username"])
    login_page.enter_password(user["password"])
    login_page.click_login()
    
    # Using the 'flash' element for the error message
    assert "invalid" in driver.find_element(By.ID, "flash").text.lower()