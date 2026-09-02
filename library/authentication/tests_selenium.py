import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "http://127.0.0.1:8000/"

VALID_EMAIL = "librarian1@test.com"
VALID_PASSWORD = "testpass123"
INVALID_EMAIL = "incorrect.email@test.com"
INVALID_PASSWORD = "wrongpassword"


class LoginPage:
    EMAIL_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    LOGIN_LINK = (By.LINK_TEXT, "LogIn")
    LOGOUT_LINK = (By.LINK_TEXT, "LogOut")
    USER_EMAIL_LINK = (By.CSS_SELECTOR, "nav a[href='/profile/']")
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success")
    ERROR_ALERT = (By.CSS_SELECTOR, ".alert-error")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout=10)

    def login_as(self, email, password):
        self.driver.get(BASE_URL)
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_LINK)).click()
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT)).send_keys(email)
        self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT)).send_keys(password)
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click()
        return self

    def logout(self):
        self.wait.until(EC.element_to_be_clickable(self.LOGOUT_LINK)).click()
        return self

    def get_alert_text(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator)).text

    def logged_in_as(self, email):
        self.wait.until(EC.element_to_be_clickable(self.LOGOUT_LINK))
        email_el = self.driver.find_element(*self.USER_EMAIL_LINK)
        assert email_el.text.strip() == email

    def logged_out(self):
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_LINK))
        assert self.driver.find_elements(*self.USER_EMAIL_LINK) == []


class LoginLogoutTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    def setUp(self):
        self.login_page = LoginPage(self.driver)

    def test_1_valid_login(self):
        self.login_page.login_as(VALID_EMAIL, VALID_PASSWORD)
        self.login_page.logged_in_as(VALID_EMAIL)
        text = self.login_page.get_alert_text(LoginPage.SUCCESS_ALERT)
        self.assertIn("Congratulation", text)

    def test_2_logout(self):
        self.login_page.logged_in_as(VALID_EMAIL)
        self.login_page.logout()
        text = self.login_page.get_alert_text(LoginPage.SUCCESS_ALERT)
        self.assertIn("Logged out", text)
        self.login_page.logged_out()

    def test_3_invalid_login(self):
        self.login_page.login_as(INVALID_EMAIL, INVALID_PASSWORD)
        text = self.login_page.get_alert_text(LoginPage.ERROR_ALERT)
        self.assertIn("Invalid email or password", text)
        self.login_page.logged_out()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()