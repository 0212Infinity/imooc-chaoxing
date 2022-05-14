# 导入库
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from clazz import Answer, Video
import re
import os
import urllib


class Course:
    def __init__(self, browser):
        self.browser = browser

    def download_and_extract(self, url):
        """根据给定的URL地址下载文件

        Parameter:
            filepath: list 文件的URL路径地址
            save_dir: str  保存路径
        Return:
            None
        """
        filename = url.split('/')[-1]
        save_path = os.path.join(r'font-cxsecret.ttf')
        urllib.request.urlretrieve(url, save_path)
        print('Successfully downloaded')

    def handle(self, url):
        while True:
            try:
                # 获取当前进度
                titleElement = self.browser.find_element(By.XPATH,
                                                         '//div[@class="units"][1]/div[@class="leveltwo"]//input[@class="knowledgeJobCount"]/parent::span/parent::a')
                titleElement.click()
            except NoSuchElementException as e:
                print('找不到下一个视频,程序结束')
                break
            # 进去iframe, 确认节点是否已经完成
            iframe1 = self.browser.find_element(By.XPATH, '//iframe[@id="iframe"]')
            self.browser.switch_to.frame(iframe1)
            # 视频 已完成(ans-attach-ct ans-job-finished) 未完成(ans-attach-ct)
            # 默认就是视频标签,这行忽略 video = self.browser.find_element(By.XPATH, '//div[@class="tabtags"]/span[1]')
            attach = self.browser.find_element(By.XPATH, '//div[@class="wrap"]/div[@class="ans-cc"]/p/div')
            # print(attach.get_attribute('class'))
            if 'ans-attach-ct' == attach.get_attribute('class'):
                print('开始视频==================')
                Video.Video(self.browser).handle()
            # 回到主框架页
            self.browser.switch_to.default_content()
            # 章节测试
            test = self.browser.find_element(By.XPATH, '//div[@class="tabtags"]/span[2]')
            test.click()
            # 进去iframe, 确认节点是否已经完成
            iframe1 = self.browser.find_element(By.XPATH, '//iframe[@id="iframe"]')
            self.browser.switch_to.frame(iframe1)
            attach = self.browser.find_element(By.XPATH, '//div[@class="wrap"]/div[@class="ans-cc"]/p/div')
            # print(attach.get_attribute('class'))
            if 'ans-attach-ct' == attach.get_attribute('class'):
                print('开始答题==================')
                # 用frame的index来定位，第一个是0
                self.browser.switch_to.frame(0)
                # 用id来定位
                self.browser.switch_to.frame("frame_content")
                # 寻找字体
                page_source = self.browser.page_source
                # print(page_source)
                # [\s\S]* 或 [\w\W]* 或 [\d\D]*
                # .* 匹配除了换行符之外的所有字符（所以作为文档中所有内容匹配的话不合适，因为文档中一定会有 '\n')
                results = re.findall(r'<style[\s\S]*?</style>', page_source)
                target_string = ''
                for result in results:
                    text = result.split('</style>')
                    # 多个style.text中筛选目标
                    if '@font-face' in text[0]:
                        target_string = text
                        break
                target_string = target_string[0]
                target_string = target_string[target_string.find('src:url(\'') + len('src:url(\''):]
                target_string = target_string[:target_string.find('\'')]
                print(target_string)
                # 执行答题
                Answer.Answer(self.browser).handle()
            # 重新进入课程页
            self.browser.get(url)
