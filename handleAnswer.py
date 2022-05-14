from fontTools.ttLib import TTFont
from bs4 import BeautifulSoup


def parseFont():
    '''
    解析字体文件，获取字体映射关系
    '''
    font1 = TTFont(r'font-cxsecret.ttf')
    keys, values = [], []
    for k, v in font1.getBestCmap().items():
        if v.startswith('uni'):
            keys.append(eval("u'\\u{:x}".format(k) + "'"))
            values.append(chr(int(v[3:], 16)))
        else:
            keys.append("&#x{:x}".format(k))
            values.append(v)
    return keys, values


def handeleHtml(content):
    with open('index.html', 'r', encoding='utf-8') as fr:
        soup = BeautifulSoup(fr, features='html.parser')
        contentElement = soup.select_one(('div#content'))
        contentElement.string = content
        html = str(soup.contents[0])
    with open('index.html', 'w', encoding='utf-8') as fw:
        fw.write(html)


def getFontDict():
    keys, values = parseFont()
    # ttf文件内没能找到原值,进行人工处理
    ttfStr = ''.join(keys)
    # 把值传入index.html文件 需要时打开注解
    # handeleHtml(ttfStr)
    # 把index.html文件中的值进行某词典识图翻译,拿到值放入 ttfValues
    ttfKeys = list(ttfStr)
    ttfValues = list('园角主公中规常为的宽三五八一以是下路道误错描需述性明有向分次制宜设须置因必锐口交应叉线曲追面求广可大积使则七市城计地基原流平了确度')
    return dict(zip(ttfKeys, ttfValues))


def handleAnswerSet():
    '''
    过滤、抽取原答案集数据
    '''
    datas = []
    with open(r'orginalanswer.txt', 'r', encoding='utf-8') as fr:
        datas = fr.readlines()
    # datas[:] python为切片列表创建了新对象， 迭代副本
    for index, item in enumerate(datas[:]):
        str1 = item.strip()
        if len(str1) == 0:
            datas.remove(item)
    with open(r'answer.txt', 'w', encoding='utf-8') as fw:
        fw.writelines(datas)
