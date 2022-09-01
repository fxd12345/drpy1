#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : htmlParser.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/8/25

from pyquery import PyQuery as pq
from urllib.parse import urljoin
import re

class jsoup:
    def __init__(self,MY_URL=''):
        self.MY_URL = MY_URL

    def test(self, text, string):
        searchObj = re.search(rf'{text}', string, re.M | re.I)
        test_ret = True if searchObj else False
        return test_ret

    def pdfh(self,html,parse,pd=False):
        if not parse:
            return ''
        doc = pq(html)
        option = None
        if parse.find('&&') > -1:
            option = parse.split('&&')[-1]
            parse = parse.split('&&')[:-1]  # 如果只有一个&& 取的就直接是0
            if len(parse) > 1:  # 如果不大于1可能就是option操作,不需要拼eq
                parse = ' '.join([i if self.test(':eq|:lt|:gt',i) else f'{i}:eq(0)' for i in parse])
            else:
                parse = parse[0] if self.test(':eq|:lt|:gt',parse[0]) else f'{parse[0]}:eq(0)'

        if option:
            # print(f'parse:{parse}=>(option:{option})')
            ret = doc(parse)
            # FIXME 解析出来有多个的情况应该自动取第一个
            if option == 'Text':
                ret = ret.text()
            elif option == 'Html':
                ret = ret.html()
            else:
                ret = ret.attr(option)
                if pd and option in ['url','src','href','data-original','data-src']:
                    ret = urljoin(self.MY_URL,ret)
        else:
            # ret = doc(parse+':first')
            ret = doc(parse) # 由于是生成器,直接转str就能拿到第一条数据,不需要next
            # ret = ret.next()  # 取第一条数据
            # ret = doc(parse) # 下面注释的写法不对的
            # ret = ret.find(':first')
            # ret = ret.children(':first')
            ret = str(ret)
        return ret

    def pdfa(self,html,parse):
        if not parse:
            return []
        if parse.find('&&') > -1:
            parse = parse.split('&&')  # 带&&的重新拼接
            # print(f"{parse[0]},{self.test(':eq|:lt|:gt', parse[0])}")
            parse = ' '.join([parse[i] if self.test(':eq|:lt|:gt', parse[i]) or i>=len(parse)-1 else f'{parse[i]}:eq(0)' for i in range(len(parse))])
        # print(f'pdfa:{parse}')
        doc = pq(html)
        # return [item.html() for item in doc(parse).items()]
        return [str(item) for item in doc(parse).items()]

    def pd(self,html,parse):
        return self.pdfh(html,parse,True)

    def pq(self,html):
        return pq(html)