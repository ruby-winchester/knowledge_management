#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import shutil
import imp

# imp.reload(sys)
# sys.setdefaultencoding("utf-8")

sys.path.append('../')
from config import configs
from model import model
import web
import util
from model.orm import *
from config_default import remind_source
from config_default import exampage_source
import time
import string
import pymysql

urls = (
    'Login', 'Login',
    'AddKnowledgePoint', 'AddKnowledgePoint',
    'UpdateKnowledgePoint', 'UpdateKnowledgePoint',
    'RequestKnowledgePoint', 'RequestKnowledgePoint',
    'DeleteKnowledgePoint', 'DeleteKnowledgePoint',
    'SelectKnowledge', 'SelectKnowledge',
)


class DeleteKnowledgePoint:
    def POST(self):
        print("删除知识点信息")
        web.header("Access-Control-Allow-Origin", "*")
        # 接收参数
        params = web.input()
        print(params)
        Knowledge = model.Knowledge_model(**params)
        if Knowledge.delete():
            # response = util.Response(status=util.Status.__success__, )
            # return util.objtojson(response)
            return 1
        else:
            # response = util.Response(status=util.Status.__error__, )
            # return util.objtojson(response)
            return 0


class AddKnowledgePoint:
    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        # 接收参数
        params = web.input()
        print(params)
        Knowledge = model.Knowledge_model(**params)
        if Knowledge.insert():
            response = util.Response(status=util.Status.__success__, )
            return 1
        else:
            response = util.Response(status=util.Status.__error__, )
            return 0

#
class Login:
    def GET(self):
        return web.seeother('/static/KnowledgeManagement.html', True)


class SelectKnowledge:
    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        # 接收参数
        Knowledge = model.Knowledge_model.query('select * from knowledge')
        Knowledge = [model.Teacher_model(**item) for item in Knowledge]
        response = util.Response(status=util.Status.__success__, body=Knowledge)
        print(util.objtojson(response))
        return util.objtojson(response)



class UpdateKnowledgePoint:
    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        params = web.input()
        print(params)
        klid = int(params['kl_id'])
        klname = params['kl_name']
        klnode = params['kl_node']
        id = int(params["id"])
        print(klid, klname, klnode, id)
        db = pymysql.connect("localhost", port=3306, user="root", passwd="123456", db="examdb", charset='utf8')
        cursor = db.cursor()
        cursor2 = db.cursor()
        sql = '''select * from knowledge '''
        sql2 = '''update knowledge set kl_id=%d, kl_name='%s',kl_node='%s' where kl_id = %d''' % \
                (klid, klname, klnode,  id)
        print("update knowledge set  kl_id=%d, kl_name='%s',kl_node='%s' where kl_id = %d" % (klid, klname, klnode,  id))

        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            print(results)
            flag = 1
            for row in results:
                x = row[0]
                y = row[1]
                print(x, y)
                if x == klid and x != id:
                    flag = 0

            if flag == 1:
                print("正在执行修改")
                cursor2.execute(sql2)
                print("修改成功")
                db.commit()
                return 1
            else:
                return 0
        except:
            print("ERROR")
            db.rollback()
        cursor.close()
        db.close()


app = web.application(urls, globals())
render = web.template.render('template')
# if __name__ == '__main__':
#     if len(urls) & 1 == 1:
#         print "urls error, the size of urls must be even."
#     else:
#         app.run()
