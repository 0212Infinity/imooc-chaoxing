import time
from selenium.webdriver.common.by import By
from handleAnswer import getFontDict


class Answer:
    def __init__(self, browser):
        self.browser = browser
        self.dic = getFontDict()

    def getReadValue(self, title):
        for key in self.dic:
            title = title.replace(key, self.dic[key])
        return title

    def setAnswer(self, index, title):
        '''
        找到答案, 页面进行选择
        '''
        value = self.getReadValue(title)
        # print(value)
        # 单选, 多选, 判断
        with open(r'answer.txt', 'r', encoding='utf-8') as fr:
            datas = fr.read()
        datas = datas[datas.find(value):]
        answerKey = datas.find('答案：')
        answerValue = datas[answerKey + 3:answerKey + datas[answerKey:].find('\n')]
        if answerValue not in ['√', 'X']:
            # 选择题, 返回答案字符进行页面匹配
            subjects = []
            for i in answerValue:
                subjectKey = datas.find(str(i) + '、')
                subjectValue = datas[subjectKey + 2: subjectKey + datas[subjectKey:].find('\n')]
                subjects.append(subjectValue)
            # print(self.browser.page_source)
            # 点击页面对应的值
            selectList = self.browser.find_elements(By.XPATH, '//div[@class="TiMu"]['
                                                    + str(index + 1) +
                                                    ']/div[@class="clearfix"]/ul/li/a')
            for select in selectList:
                readSelectVal = self.getReadValue(select.text)
                if readSelectVal in subjects:
                    select.click()
        else:
            # 判断题
            if '√' == answerValue:
                # 相等选第一个, 否则第二个
                rightSelect = self.browser.find_element(By.XPATH, '//div[@class="TiMu"]['
                                                        + str(index + 1) +
                                                        ']/div[@class="clearfix"]//ul/li[1]/label')
                rightSelect.click()
            else:
                wrongSelect = self.browser.find_element(By.XPATH, '//div[@class="TiMu"]['
                                                        + str(index + 1) +
                                                        ']/div[@class="clearfix"]//ul/li[2]/label')
                wrongSelect.click()

    def handle(self):
        titles = self.browser.find_elements(By.XPATH, '//div[@class="TiMu"]/div[@class="Zy_TItle clearfix"]/div')
        for index in range(len(titles)):
            title = titles[index]
            titleStr = title.text
            # print(titleStr[titleStr.find('】') + 1:])
            self.setAnswer(index, titleStr[titleStr.find('】') + 1:])
        while True:
            # 点击提交按钮
            self.browser.find_element(By.XPATH, '//div[@class="ZY_sub clearfix"]/a[last()]/span').click()
            # 查看文本文字 太快文本框还没加载出来,这里进行等待
            time.sleep(5)
            tipContent = self.browser.find_element(By.XPATH, '//p[@id="tipContent"]').text
            if '未做完' in tipContent:
                print('题目未完成或者题库有误!')
                self.browser.find_element(By.XPATH, '//div[@id="confirmSubWin"]/div/div/a[2]').click()
                time.sleep(50)
                continue
            break
        # 点击'确认提交'框
        self.browser.find_element(By.XPATH, '//div[@id="confirmSubWin"]/div/div/a[1]').click()
