from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import datetime


class Video:
    def __init__(self, browser):
        self.browser = browser

    def handle(self):
        # 用frame的index来定位，第一个是0
        self.browser.switch_to.frame(0)
        playerBtn = self.browser.find_element(By.XPATH, '//div[@id="video"]/button')
        playerBtn.click()
        time.sleep(3)
        muteBtn = self.browser.find_element(By.XPATH, '//div[@id="video"]//button[contains(@class,"vjs-mute-control")]')
        muteBtn.click()
        while True:
            # print(self.browser.page_source)
            # videoWin = self.browser.find_element(By.XPATH, '//div[@id="video"]')
            # 鼠标悬停
            ActionChains(self.browser).move_to_element(muteBtn).perform()
            # 每十秒获取一次,是否结束
            time.sleep(10)
            beginTime = self.browser.find_element(By.XPATH,
                                                  '//div[@id="video"]//span[@class="vjs-current-time-display"]')
            endTime = self.browser.find_element(By.XPATH,
                                                '//div[@id="video"]//span[@class="vjs-duration-display"]')
            # print(beginTime.is_displayed()) False说明被隐藏了
            # print(endTime.is_displayed()) False说明被隐藏了
            print('{} / {}'.format(beginTime.get_attribute('innerText'), endTime.get_attribute('innerText')))
            beginStrptime = datetime.datetime.strptime(beginTime.get_attribute('innerText'), '%M:%S')
            endStrptime = datetime.datetime.strptime(endTime.get_attribute('innerText'), '%M:%S')
            if (endStrptime - beginStrptime).seconds <= 0:
                break
