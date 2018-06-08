#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import requests
import json
import re
from lxml import html
#m.weibo.cn，先登录再退出

'''
uid:1239246050
type:uid
value:1944477663
containerid:1005051239246050
'''

class Weibo(object):
    def get_weibo(self,id,page):  #指定博主的所有微博 ，id：个人id
        #Request URL:https://m.weibo.cn/api/container/getIndex?uid=1239246050&luicode=10000011&lfid=102803_ctg1_8999_-_ctg1_8999_home&featurecode=20000320&type=uid&value=1239246050&containerid=1076031239246050
        #有用的是https://m.weibo.cn/api/container/getIndex?uid=1239246050&type=uid&value=1239246050&containerid=1076031239246050
        url = 'https://m.weibo.cn/api/container/getIndex?uid={}&type=uid&value={}&containerid=107603{}&page={}'.format(id,id,id,page) #微博是动态加载，滑下去会加载出page=2,3,4.。页的信息
        response = requests.get(url)
        #response.content.decode('utf-8')和response.text是一样的
        ob_json = json.loads(response.text) #转换为字典
        list_cards = ob_json.get('cards')
        return list_cards

    def get_comments(self,id,page):  #获取微博下的评论，id：微博id
        url = 'https://m.weibo.cn/api/comments/show?id={}&page={}'.format(id,page)
        response = requests.get(url)
        ob_json = json.loads(response.text)
        list_comments = ob_json.get('hot_data')
        return list_comments

    def main(self, uid):
        page = 1
        list_list_cards = []
        while(True):             #搜索所有微博            #可以优化成边搜索边打印
        #while(page< 5):         #搜索前4页微博
            print('加载第{}页'.format( page))
            list_cards = self.get_weibo(uid,page)       #是一个list
            if(list_cards == []):
                break
            page += 1
            list_list_cards.append(list_cards)
        count_hotweibo = 1
        for list_cards in list_list_cards:
            for card in list_cards:
                if(card.get('card_type') == 9): #只有等于9是个人发的微博,其他的是广告等
                    id = card.get('mblog').get('id')    #微博id
                    text = card.get('mblog').get('text')    #微博内容
                    tree = html.fromstring(text)
                    text = tree.xpath('string(.)')
                    print('第{}条微博：'.format(count_hotweibo) +  text+  '\n')                 #修改控制台编码格式为utf-8 ， chcp 65001
                    count_hotweibo += 1
                    list_comments = self.get_comments(id,1)
                    count_hotcomments = 1           #第几条微博
                    if(list_comments != None):      #有评论
                        for comment in list_comments:
                            created_at = comment.get('created_at')  #获取时间
                            like_counts = comment.get('like_counts')    #点赞数
                            text = comment.get('text')
                            tree = html.fromstring(text)
                            text = tree.xpath('string(.)')      #用string函数过滤多余标签  （表情等）         ？？？？？？？？？
                            name_user = comment.get('user').get('screen_name')
                            source = comment.get('source')
                            if source == '':
                                source = '未知'
                            print(str(count_hotcomments), ': ',name_user,'  ','发表于：'+created_at,'点赞：'+str(like_counts),'来自：'+source )
                            print(text + '\n')
                            count_hotcomments += 1
                    print('-----------------------------------------')

if __name__ == '__main__':
    wb = Weibo()
    #wb.main(1239246050)        #多
    wb.main(1971411445)         #少