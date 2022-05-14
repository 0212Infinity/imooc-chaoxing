# 导入库
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from clazz import Login, Course
from selenium.common.exceptions import UnexpectedAlertPresentException

if __name__ == '__main__':
    try:
        # 设置浏览器参数
        # options = webdriver.ChromeOptions()
        # 无头模式
        # options.add_argument('headless')
        # 设置浏览器驱动位置
        # 当前谷歌浏览器版本101.0.4951.41, chromedriver版本101.0.4951.41
        browser = webdriver.Chrome(service=Service(r"chromedriver.exe"))
        # 业务逻辑处理
        # 进行登录 TODO 请替换真实地址
        url = 'url'
        Login.Login(browser, url).handle()
        Course.Course(browser).handle(url)
    except UnexpectedAlertPresentException as e:
        browser.switch_to.alert.accept()
        print('UnexpectedAlertPresentException', e)
    except Exception as r:
        print('未知错误', r)
    finally:
        # 关闭浏览器
        browser.close()
