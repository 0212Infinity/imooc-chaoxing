# 导入库
from selenium.webdriver.common.by import By


class Login:
    def __init__(self, browser, url):
        self.browser = browser
        self.url = url

    def handle(self):
        self.browser.get(self.url)
        self.browser.implicitly_wait(3)

        # input.id="phone" 手机号输入框
        phoneElement = self.browser.find_element(By.XPATH, '//input[@id="phone"]')
        # input.id="pwd" 手机号输入框
        pwdElement = self.browser.find_element(By.XPATH, '//input[@id="pwd"]')
        # button.id="loginBtn" 登录按钮
        loginBtnElement = self.browser.find_element(By.XPATH, '//button[@id="loginBtn"]')
        # 监听用户输入账号密码, 空格隔开
        phone, pwd = map(str, input('输入账号密码,空格隔开:\n').split(' '))
        phoneElement.send_keys(phone)
        pwdElement.send_keys(pwd)
        # 点击登录按钮
        loginBtnElement.click()
