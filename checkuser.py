# -*- coding: UTF-8 -*-
import urllib
import json
import httplib2
import sys
import time
import ConfigParser
import urllib3
import re
from datetime import datetime
import logging
from logging import handlers


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
reload(sys)
sys.setdefaultencoding("utf-8")


class splunk_spl:
    def __init__(self, base_url=None):
        db_cfg = "./config.conf"
        config_raw = ConfigParser.RawConfigParser()
        config_raw.read(db_cfg)
        self.base_url = config_raw.get('SPLUNK', 'ROOT_URL')
        self.username = config_raw.get('SPLUNK', 'USER_NAME')
        self.password = config_raw.get('SPLUNK', 'PASSWORD')
        self.maintainer_list=config_raw.get("MAINTAINER","MAINTAINER_LIST")
        self.receiver=config_raw.get("CASE5","RECEIVER")
        self.csv_question=config_raw.get("CASE5","QUESTION_LIST")
        self.csv_answer=config_raw.get("CASE5","ANSWER_LIST")        
        self.subject=config_raw.get("CASE5","SUBJECT")
        self.title=config_raw.get("CASE5","TITLE")
        self.error_message = ''
        self.splunk_error_case4=config_raw.get("ERROR_TEXT","SPLUNK_ERROR_CASE4")
        self.splunk_error=config_raw.get("ERROR_TEXT","SPLUNK_ERROR")
        self.input_project_error=config_raw.get("ERROR_TEXT","INPUT_PROJECT_ERROR")  
        self.net_error=config_raw.get("ERROR_TEXT","NET_ERROR")
        self.permission_error=config_raw.get("ERROR_TEXT","PERMISSION_ERROR")
        self.date_error=config_raw.get("ERROR_TEXT","DATE_ERROR")
        self.jira_error=config_raw.get("ERROR_TEXT","JIRA_ERROR")
    def query_usecase1(self, search_query):
        """
            调Splunk接口

        args：
            搜索命令
        returns：
            res 查询结果
        """
        print(search_query)
        result_dic = {}
        try:
            # 1. Login and get the session key
            http = httplib2.Http("/tmp/.cache", disable_ssl_certificate_validation=True)
            url = self.base_url + '/servicesNS/' + self.username + '/search/auth/login?output_mode=json'
            params = urllib.urlencode({

                'username': self.username,
                'password': self.password
            })
            print(url)
            response, content = http.request(url, 'GET', params,
                                             headers={
                                                 "Accept": "text/html,application/xhtml+xml,application/xml",
                                                 "Accept-Encoding": ""
                                             })
            print(response)
            content = json.loads(content)
            authToken = content.get("sessionKey")
            print("authToken")
            # 2. get sid
            # if not search_query.startswith('search'):
            #    search_query = 'search ' + search_query
            # print search_query

            sid_body = \
                http.request(self.base_url + '/servicesNS/aiops/DCtrlChatBot/search/jobs?output_mode=json', 'POST',
                             headers={'Authorization': 'Splunk %s' % authToken},
                             body=urllib.urlencode({'search': search_query}))[1]
            sid = json.loads(sid_body)['sid']
            print sid

            # 3. find job result because the SPL run cost time . So it is an Async Job.
            count = 1
            while True:
                url = self.base_url + '/servicesNS/aiops/DCtrlChatBot/search/jobs/%s/results?output_mode=json' % sid
                response, content = http.request(
                    uri=url,
                    method='GET',
                    headers={'Authorization': 'Splunk ' + authToken}
                )
                count = count + 1
                time.sleep(2)
                if content:
                    break
                if count > 10:
                    break
            print("22222" + content)
            if content:
                content = json.loads(content)
                result_dic = content["results"]
            # print result_dic
            return result_dic
        except(Exception):
            return "splunk_broken"


    def query(self, search_query):
        """
            调Splunk接口

        args：
            搜索命令
        returns：
            res 查询结果
        """
        print(search_query)
        result_dic = {}
        try:
            # 1. Login and get the session key
            http = httplib2.Http("/tmp/.cache", disable_ssl_certificate_validation=True)
            url = self.base_url + '/servicesNS/' + self.username + '/search/auth/login?output_mode=json'
            params = urllib.urlencode({

                'username': self.username,
                'password': self.password
            })
            print(url)
            response, content = http.request(url, 'GET', params,
                                             headers={
                                                 "Accept": "text/html,application/xhtml+xml,application/xml",
                                                 "Accept-Encoding": ""
                                             })
            print("#JOB_RESULT response 111=%s" % response)
            content = json.loads(content)
            authToken = content.get("sessionKey")
            print("authToken")
            # 2. get sid
            # if not search_query.startswith('search'):
            #    search_query = 'search ' + search_query
            # print search_query

            sid_body = \
                http.request(self.base_url + '/services/search/jobs?output_mode=json', 'POST',
                             headers={'Authorization': 'Splunk %s' % authToken},
                             body=urllib.urlencode({'search': search_query}))[1]
            sid = json.loads(sid_body)['sid']
            print sid

            # 3. find job result because the SPL run cost time . So it is an Async Job.
            count = 1
            while True:
                url = self.base_url + '/services/search/jobs/%s/results?output_mode=json' % sid
                response, content = http.request(
                    uri=url,
                    method='GET',
                    headers={'Authorization': 'Splunk ' + authToken}
                )
                count = count + 1
                time.sleep(2)
                if content:
                    break
                if count > 10:
                    break
            print("22222" + content)
            if content:
                content = json.loads(content)
                result_dic = content["results"]
            # print result_dic
            return result_dic
        except(Exception):
            return "splunk_broken"

    def query_by_app(self, search_query,app_name):
        """
            调Splunk接口

        args：
            搜索命令
        returns：
            res 查询结果
        """
        print(search_query)
        result_dic = {}
        try:
            # 1. Login and get the session key
            http = httplib2.Http("/tmp/.cache", disable_ssl_certificate_validation=True)
            url = self.base_url + '/servicesNS/' + self.username + '/search/auth/login?output_mode=json'
            params = urllib.urlencode({

                'username': self.username,
                'password': self.password
            })
            print(url)
            response, content = http.request(url, 'GET', params,
                                             headers={
                                                 "Accept": "text/html,application/xhtml+xml,application/xml",
                                                 "Accept-Encoding": ""
                                             })
            print("#JOB_RESULT response by app=%s" % response)
            content = json.loads(content)
            authToken = content.get("sessionKey")
            print(authToken)
            # 2. get sid
            # if not search_query.startswith('search'):
            #    search_query = 'search ' + search_query
            # print search_query
            sid_body = \
                http.request(self.base_url + '/servicesNS/aiops/'+app_name+'/search/jobs?output_mode=json', 'POST',
                             headers={'Authorization': 'Splunk %s' % authToken},
                             body=urllib.urlencode({'search': search_query}))[1]
            print(sid_body)
            sid = json.loads(sid_body)['sid']
            print(sid)

            # 3. find job result because the SPL run cost time . So it is an Async Job.
            count = 1
            while True:
                url = self.base_url + '/servicesNS/aiops/'+app_name+'/search/jobs/%s/results?output_mode=json' % sid
                print(url)
                response, content = http.request(
                    uri=url,
                    method='GET',
                    headers={'Authorization': 'Splunk ' + authToken}
                )
                count = count + 1
                time.sleep(2)
                if content:
                    break
                if count > 99999:
                    break
            print("22222" + content)
            if content:
                content = json.loads(content)
                result_dic = content["results"]
            # print result_dic
            return result_dic
        except(Exception):
            return "splunk_broken"

    def search_user_list_case11(self):
        """
            查询case1展示的项目

        args：
            
        returns：
            res 查询结果
        """

        query = '|inputlookup AssetLinkInfo.csv | dedup Category | fields Category'
        result = self.query_usecase1(query)

      
        print("#JOB_RESULT result=%s" % result)
        return result

    def search_user_list_case12(self, assigned_to):
        """
            查询case1所选项目的详情

        args：
            assigned_to 项目名
        returns：
            res 查询结果
        """
        query = '|inputlookup AssetLinkInfo.csv where Category =%s' % assigned_to
        print("#JOB_RESULT query=%s" % query)
        result = self.query_usecase1(query)
        print("#JOB_RESULT result_pp=%s" % result)

        if result == "":
            result = "no value"

        print("#JOB_RESULT result=%s" % result)
        return result

    def search_user_list_case21(self, eid):
        """
            查询eid所拥有的项目权限

        args：
            EID 使用bot人的eid
        returns：
            res 查询结果
        """
        res=[]
        role_app=[]
        label=[]
        query='|`searchProjectsByUserChatbot("%s")`' % eid[:-14]
        #query='|`searchProjectsByUserChatbot("%s")`' % "yin.yang"
        result_user_rights = self.query_by_app(query,"DCtrlChatBot")
        if result_user_rights==[]:
            print("#JOB_RESULT result=%s" % self.permission_error)
            return
        print("#JOB_RESULT result_user_rights=%s" % result_user_rights)
        for j in range(len(result_user_rights)):
            User_Pname=result_user_rights[j]["ProjectName"]
            print("#JOB_RESULT User_Pname=%s" % User_Pname)
            label.append(User_Pname)
        for j in range(len(result_user_rights)):
            AppName=result_user_rights[j]["AppName"]
            print("#JOB_RESULT AppName=%s" % AppName)
            role_app.append(AppName)  
        res.append(role_app)
        res.append(label)
        if res:
              print("#JOB_RESULT result=%s" % res)
        else:
              print("#JOB_RESULT result=%s" % "no data")
        

    def search_user_list_case22(self, eid, app_name,decide_list):
        """
            查询case2项目进度详情

        args：
            eid EID
            app_name 项目名
            decide_list 项目名和查询所需APPname对应字典
            
        returns：
            res 查询结果
        """
        try:
          n_time=datetime.now()
          n_time=n_time.strftime('%Y-%m-%d')
          print("#JOB_RESULT raaaaaaa=%s" % decide_list)
          decide_list=eval(decide_list)
          print("#JOB_RESULT raaaaaaa=%s" % decide_list)
          a=decide_list[app_name]
          print("#JOB_RESULT raaaaaaa=%s" % a)
        except NameError:
          result=self.net_error
          print("#JOB_RESULT result=%s" % result)
          return result
        print("#JOB_RESULT app_name=%s" % app_name)
        query_title='| rest splunk_server=local  /services/apps/local | rename eai:acl.perms.read as roles| fields title | where lower(title) = "%s"' % a
        result_title = self.query(query_title)
        print("#JOB_RESULT result_title=%s" % result_title)
        print("#JOB_RESULT aqdqqqqqqqqqqqqqq=%s" % a)
        query = '|search `getEVM4Chatbot(%s)` ' % n_time
        print("#JOB_RESULT aqdqqqqqqqqqqqqqq=%s" % a)
        result = self.query_by_app(query,a)#需要改成变量
        if not result or result=="splunk_broken":
            result=self.input_project_error
        print("#JOB_RESULT result=%s" % result)
        return ""


    def search_user_list_case32(self, eid, date,decide_list,decide_name):
        """
            判断case3输入日期和项目名是否正确 并查询splunk

        args：
            eid EID
            date 日期
            decide_list 项目名和appname的字典
            decide_name 项目名
        returns：
            res splunk中的查询数据
        """  
        try:
          decide_list=eval(decide_list)
          #a project name
          a=decide_list[decide_name]
          print("#JOB_RESULT aaaaaaa=%s" % a)
          # d 判断格式是否合法
          d = re.search(r"(^\d{4}-[0-9][0-9]-[0-9][0-9]$)", date)
          #b 判断日期是否合法
          b = time.strptime(date, "%Y-%m-%d")
          n_time=datetime.now()
          n_time=n_time.strftime("%Y-%m-%d")
          d_value=(datetime.strptime(n_time,"%Y-%m-%d")-datetime.strptime(date,"%Y-%m-%d"))
          d_value=str(d_value)
          if d_value[0] =="-":
            result=self.date_error
            print("#JOB_RESULT result=%s" % result)
            return result
        except NameError:
          result=self.net_error
          print("#JOB_RESULT result=%s" % result)
          return result

        query_title='| rest splunk_server=local  /services/apps/local | rename eai:acl.perms.read as roles| fields title | where lower(title) = "%s"' % a
        result_title = self.query(query_title)
        print("#JOB_RESULT result_title=%s" % result_title)
        query = '|search `getRemainingTasks4Chatbot("%s", "%s")`  '% ("yin.yang",date)
        #result = self.query_by_app(query,result_title[0]['title'])#需要改成变量
        result = self.query_by_app(query,"deliverycontroljira")#需要改成变量
        if not result:
          result="no data "


        print("#JOB_RESULT result=%s" % result)
        return result
    
    def check_log_date(self):
          with open('./D-ctrl_Log.log', 'r+') as f:
            log_date=f.read()
            log_date=log_date.split(" ")[0]
            print("#JOB_RESULT result=%sqweqweqwweqwewqeqweqeqweqeqeqweeqwe"% log_date)
            if log_date:
              now_time=datetime.now().strftime('%Y-%m-%d')
              day_value =datetime.strptime(now_time,"%Y-%m-%d") - datetime.strptime(log_date, "%Y-%m-%d")
              if day_value.days >=180:
                  f.truncate(0)
          f.close()
    def search_user_list_case41(self, eid):
          """
              判断case4输入日期和项目名是否正确 并查询splunk

            args：
              eid EID
              date 日期
              decide_list 项目名和appname的字典
              decide_name 项目名
            returns：
              res splunk中的查询数据
          """

          list_Addressee=[]
          query_Addressee = '| inputlookup PushUserList.csv  '
          result_Addressee=self.query_by_app(query_Addressee,"DCtrlChatBot")
          #print("#JOB_RESULT result_Addressee=%s" % result_Addressee)
       
          if result_Addressee == [] :
            splunk_spl().check_log_date()
            logger = logging.getLogger("D-ctrl_Log.log")
            fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
            format_str = logging.Formatter(fmt)
            th = handlers.TimedRotatingFileHandler(filename="D-ctrl_Log.log", when='D', encoding='utf-8')
            th.setFormatter(format_str)#设置文件里写入的格式
            logger.addHandler(th)
            logger.error("PushUserList.csvの情報はありません")
            return
          #print("#JOB_RESULT result_Addressee=%s" % result_Addressee)
          #需要修改后缀
          
          
          
          for i in range(len(result_Addressee)):
             list_Addressee.append(result_Addressee[i]["Eid"])
          #print("#JOB_RESULT list_Addressee=%s" % list_Addressee)
          
          
          result={}
          list_Addressee_APP=[]
          result1=""
          for b in range(len(list_Addressee)):
            query_verify_system='|`searchProjectsByUserChatbot("%s")`| fields System' % list_Addressee[b]
            result_verify_system=self.query_by_app(query_verify_system,"DCtrlChatBot")
            list_verify_system=[]
            for i in range(len(result_verify_system)):
              list_verify_system.append(result_verify_system[i]["System"])
            if "Jira" not in list_verify_system:
              continue
     
            #query='|`searchProjectsByUserChatbot("%s")`'% list_Addressee[b]
            #修改解除限制
            query='|`searchProjectsByUserChatbot("%s")`' % "yin.yang"
            result_Addressee_rights = self.query_by_app(query,"DCtrlChatBot")
            #print("#JOB_RESULT result_Addressee_rights=%s" % result_Addressee_rights)
            list_Addressee_APP=[]
            list_Addressee_rights=[]
            for i in range(len(result_Addressee_rights)):
              Pname=result_Addressee_rights[i]["ProjectName"]
              Aname=result_Addressee_rights[i]["AppName"]
           # print("#JOB_RESULT Pname=%s" %  Pname)
              list_Addressee_rights.append(Pname)
              list_Addressee_APP.append(Aname)
            print("#JOB_RESULT list_Addresse_APP=%s" % list_Addressee_APP)
            list_Addressee_APP=list(set(list_Addressee_APP))
            
            for AppName in list_Addressee_APP:
              Appname="deliverycontroljira"
              query = '|search `getJiraUserLoginInfo4Chatbot`'
              
              result_login_info = self.query_by_app(query,Appname)
              print("#JOB_RESULT result_login_info=%s" % result_login_info)

              list_login_name=[]
              for i in range(len(result_login_info)):
                Lname=result_login_info[i]["user"]
                list_login_name.append(Lname)
              #print("#JOB_RESULT list_login_name=%s" % list_login_name)

              dic_users_rights={}   
              for i in range(len(list_login_name)):
                list_user_rights=[]
                query='|`searchProjectsByUserChatbot("%s")`' % list_login_name[i]
                #query='|`searchProjectsByUserChatbot("%s")`' % "yin.yang"
                result_user_rights = self.query_by_app(query,"DCtrlChatBot")
               # print("#JOB_RESULT result_user_rights=%s" % result_user_rights)
                for j in range(len(result_user_rights)):
                  User_Pname=result_user_rights[j]["ProjectName"]
                  #print("#JOB_RESULT User_Pname=%s" % User_Pname)
                  list_user_rights.append(User_Pname)
                #print("#JOB_RESULT list_user_rights=%s" % list_user_rights)
                dic_users_rights[list_login_name[i]]=list_user_rights              
              list_sent=[]
              for i in dic_users_rights:
                a=set(list_Addressee_rights).intersection(set(dic_users_rights[i]))
                if a:
                  list_sent.append(i)

              html1 = """<h><strong>Jira(%s)</strong></h><table border="1" cellspacing="0" bgcolor="#FCFCFC"><tr><td bgcolor="#AEDD81"><big>&nbsp;&nbsp;user</big></td><td bgcolor="#AEDD81"><big>count</big></td><td bgcolor="#AEDD81"><big>&nbsp;&nbsp;lastestTime</big></td></tr>"""% AppName
              for i in range(len(result_login_info)):
                #print(result_login_info[i]['user'])
                if result_login_info[i]['user'] in list_sent:
                  try:
                    user = result_login_info[i]['user']
                  except(Exception):
                    user = ""
                  try:
                    count = result_login_info[i]["count"]
                    #print(count)
                  except(Exception):
                    count = ""
                  try:
                    lastesTime = result_login_info[i]["lastestTime"]
                  except(Exception):
                    lastesTime = ""

                  html2 = """<tr><td>%s</td><td>%s</td><td>%s</td></tr>""" % (user, count, lastesTime)
                else:
                  continue

                html1 = html1 + html2
              html1 = html1 + "</table>"
              print("#JOB_RESULT list_sent=%s" % list_sent)
              print("#JOB_RESULT result123=%s" % dic_users_rights)
              empty_list='<h><strong>Jira(%s)</strong></h><table border="1" cellspacing="0" bgcolor="#FCFCFC"><tr><td bgcolor="#AEDD81"><big>&nbsp;&nbsp;user</big></td><td bgcolor="#AEDD81"><big>count</big></td><td bgcolor="#AEDD81"><big>&nbsp;&nbsp;lastestTime</big></td></tr></table>'% AppName
              if html1 == empty_list:
                html1='<h><strong>Jira(%s)</strong></h><table border="1" cellspacing="0" bgcolor="#FCFCFC"><tr><td bgcolor="#AEDD81"><big>&nbsp;&nbsp;user</big></td><td bgcolor="#AEDD81"><big>count</big></td><td bgcolor="#AEDD81"><big>&nbsp;&nbsp;lastestTime</big></td></tr><tr><td><big>-</big></td><td><big>-</big></td><td><big>-</big></td></tr></table>'% AppName
              result[list_Addressee[b]+"@acpcloud2315outlook.onmicrosoft.com"]=html1
              result1=result1+""" '%s':'%s',"""%(list_Addressee[b]+"@acpcloud2315outlook.onmicrosoft.com_%s" % AppName,html1)
          #list_accendant=["paul.guangcao.zhang1@outlook.com"]
          #result["list_accendant"]=list_accendant
          result="""{%s}"""%result1[:-1]
          result=json.dumps(result)
          print("#JOB_RESULT result=%s" % eval(result))

    def search_user_list_case42(self, eid):
        """
            判断case4输入日期和项目名是否正确 并查询splunk

          args：
            eid EID
            date 日期
            decide_list 项目名和appname的字典
            decide_name 项目名
          returns：
            res splunk中的查询数据
        """  

        list_Addressee=[]
        query_Addressee = '| inputlookup PushUserList.csv  '
        result_Addressee=self.query_by_app(query_Addressee,"DCtrlChatBot")
        #print("#JOB_RESULT result_Addressee=%s" % result_Addressee)

        if result_Addressee == [] :
          splunk_spl().check_log_date()
          logger = logging.getLogger("D-ctrl_Log.log")
          fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
          format_str = logging.Formatter(fmt)
          th = handlers.TimedRotatingFileHandler(filename="D-ctrl_Log.log", when='D', encoding='utf-8')
          th.setFormatter(format_str)#设置文件里写入的格式
          logger.addHandler(th)
          logger.error("PushUserList.csvの情報はありません")
          return
        #print("#JOB_RESULT result_Addressee=%s" % result_Addressee)
        #需要修改后缀



        for i in range(len(result_Addressee)):
           list_Addressee.append(result_Addressee[i]["Eid"])
        #print("#JOB_RESULT list_Addressee=%s" % list_Addressee)


        result={}
        list_Addressee_APP=[]
        result1=""
        for b in range(len(list_Addressee)):
          query_verify_system='|`searchProjectsByUserChatbot("%s")`| fields System' % list_Addressee[b]
          result_verify_system=self.query_by_app(query_verify_system,"DCtrlChatBot")
          list_verify_system=[]
          for i in range(len(result_verify_system)):
            list_verify_system.append(result_verify_system[i]["System"])
          if "Redmine" not in list_verify_system:
            continue

          #query='|`searchProjectsByUserChatbot("%s")`'% list_Addressee[b]
          #修改解除限制
          query='|`searchProjectsByUserChatbot("%s")`' % "yin.yang"
          result_Addressee_rights = self.query_by_app(query,"DCtrlChatBot")
          #print("#JOB_RESULT result_Addressee_rights=%s" % result_Addressee_rights)
          list_Addressee_APP=[]
          list_Addressee_rights=[]
          for i in range(len(result_Addressee_rights)):
            Pname=result_Addressee_rights[i]["ProjectName"]
            Aname=result_Addressee_rights[i]["AppName"]
         # print("#JOB_RESULT Pname=%s" %  Pname)
            list_Addressee_rights.append(Pname)
            list_Addressee_APP.append(Aname)
          print("#JOB_RESULT list_Addresse_APP=%s" % list_Addressee_APP)
          list_Addressee_APP=list(set(list_Addressee_APP))

          for AppName in list_Addressee_APP:
            Appname="deliverycontrolforredmine"
            query = '|search `getRedmineUserLoginInfo4Chatbot`'

            result_login_info = self.query_by_app(query,Appname)
            print("#JOB_RESULT result_login_info=%s" % result_login_info)

            list_login_name=[]
            for i in range(len(result_login_info)):
              Lname=result_login_info[i]["user"]
              list_login_name.append(Lname)
            #print("#JOB_RESULT list_login_name=%s" % list_login_name)

            dic_users_rights={}   
            for i in range(len(list_login_name)):
              list_user_rights=[]
              query='|`searchProjectsByUserChatbot("%s")`' % list_login_name[i]
              #query='|`searchProjectsByUserChatbot("%s")`' % "yin.yang"
              result_user_rights = self.query_by_app(query,"DCtrlChatBot")
             # print("#JOB_RESULT result_user_rights=%s" % result_user_rights)
              for j in range(len(result_user_rights)):
                User_Pname=result_user_rights[j]["ProjectName"]
                #print("#JOB_RESULT User_Pname=%s" % User_Pname)
                list_user_rights.append(User_Pname)
              #print("#JOB_RESULT list_user_rights=%s" % list_user_rights)
              dic_users_rights[list_login_name[i]]=list_user_rights              
            list_sent=[]
            for i in dic_users_rights:
              a=set(list_Addressee_rights).intersection(set(dic_users_rights[i]))
              if a:
                list_sent.append(i)

            html1 = """<h><strong>Redmine(%s)</strong></h><table border="1" cellspacing="0" bgcolor="#FCFCFC"><tr><td bgcolor="#AEDD81"><big>&nbsp;&nbsp;user</big></td><td bgcolor="#AEDD81"><big>count</big></td><td bgcolor="#AEDD81"><big>&nbsp;&nbsp;lastestTime</big></td></tr>"""% AppName
            for i in range(len(result_login_info)):
              #print(result_login_info[i]['user'])
              if result_login_info[i]['user'] in list_sent:
                try:
                  user = result_login_info[i]['user']
                except(Exception):
                  user = ""
                try:
                  count = result_login_info[i]["count"]
                  #print(count)
                except(Exception):
                  count = ""
                try:
                  lastesTime = result_login_info[i]["lastestTime"]
                except(Exception):
                  lastesTime = ""

                html2 = """<tr><td>%s</td><td>%s</td><td>%s</td></tr>""" % (user, count, lastesTime)
              else:
                continue

              html1 = html1 + html2
            html1 = html1 + "</table>"
            print("#JOB_RESULT list_sent=%s" % list_sent)
            print("#JOB_RESULT result123=%s" % dic_users_rights)
            empty_list='<h><strong>Redmine(%s)</strong></h><table border="1" cellspacing="0" bgcolor="#FCFCFC"><tr><td bgcolor="#AEDD81"><big>&nbsp;&nbsp;user</big></td><td bgcolor="#AEDD81"><big>count</big></td><td bgcolor="#AEDD81"><big>&nbsp;&nbsp;lastestTime</big></td></tr></table>'% AppName
            if html1 == empty_list:
              html1='<h><strong>Redmine(%s)</strong></h><table border="1" cellspacing="0" bgcolor="#FCFCFC"><tr><td bgcolor="#AEDD81"><big>&nbsp;&nbsp;user</big></td><td bgcolor="#AEDD81"><big>count</big></td><td bgcolor="#AEDD81"><big>&nbsp;&nbsp;lastestTime</big></td></tr><tr><td><big>-</big></td><td><big>-</big></td><td><big>-</big></td></tr></table>'% AppName
            result[list_Addressee[b]+"@acpcloud2315outlook.onmicrosoft.com"]=html1
            result1=result1+""" '%s':'%s',"""%(list_Addressee[b]+"@acpcloud2315outlook.onmicrosoft.com_%s" % AppName,html1)
        #list_accendant=["paul.guangcao.zhang1@outlook.com"]
        #result["list_accendant"]=list_accendant
        result="""{%s}"""%result1[:-1]
        result=json.dumps(result)
        print("#JOB_RESULT result=%s" % eval(result))
        
    def search_user_list_case43(self, eid):
        """
            判断case4输入日期和项目名是否正确 并查询splunk

          args：
            eid EID
            date 日期
            decide_list 项目名和appname的字典
            decide_name 项目名
          returns：
            res splunk中的查询数据
        """  
        list_Addressee=[]
        query_Addressee = '| inputlookup PushUserList.csv '
        result_Addressee=self.query_by_app(query_Addressee,"DCtrlChatBot")
        if result_Addressee == [] :            
            splunk_spl().check_log_date()
            logger = logging.getLogger("D-ctrl_Log.log")
            fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
            format_str = logging.Formatter(fmt)
            th = handlers.TimedRotatingFileHandler(filename="D-ctrl_Log.log", when='D', encoding='utf-8')
            th.setFormatter(format_str)#设置文件里写入的格式
            logger.addHandler(th)
            logger.error("PushUserList.csvの情報はありません")
            return
        for i in range(len(result_Addressee)):
           list_Addressee.append(result_Addressee[i]["Eid"])
        print("#JOB_RESULT list_Addressee=%s" % list_Addressee)
        result={}
        #list_Addressee=["yangyinjp@outlook.com","satoshi.nagai","takaomi.okuzono","paul.guangcao.zhang1@outlook.com"]
        #list_Addressee=["a","b"]
        query = '|search `getSplunkUserLoginInfo4Chatbot`'
        result_login_info = self.query_by_app(query,"DCtrlChatBot")
        print("#JOB_RESULT result_login_info=%s" % result_login_info)
        
        list_login_name=[]
        for i in range(len(result_login_info)):
          Lname=result_login_info[i]["user"]
          list_login_name.append(Lname)
        print("#JOB_RESULT list_login_name=%s" % list_login_name)
        
        dic_users_rights={}   
        for i in range(len(list_login_name)):
          list_user_rights=[]
          query='|`searchProjectsByUserChatbot("%s")`' % list_login_name[i]
          #query='|`searchProjectsByUserChatbot("%s")`' % "yin.yang"
          result_user_rights = self.query_by_app(query,"DCtrlChatBot")
          print("#JOB_RESULT result_user_rights=%s" % result_user_rights)
          for j in range(len(result_user_rights)):
            User_Pname=result_user_rights[j]["ProjectName"]
            print("#JOB_RESULT User_Pname=%s" % User_Pname)
            list_user_rights.append(User_Pname)
          print("#JOB_RESULT list_user_rights=%s" % list_user_rights)
          dic_users_rights[list_login_name[i]]=list_user_rights
        
        for b in range(len(list_Addressee)):
          query='|`searchProjectsByUserChatbot("%s")`'% list_Addressee[b]
          #query='|`searchProjectsByUserChatbot("%s")`' % "yin.yang"
          result_Addressee_rights = self.query_by_app(query,"DCtrlChatBot")
          print("#JOB_RESULT result_Addressee_rights=%s" % result_Addressee_rights)
        
          list_Addressee_rights=[]
          for i in range(len(result_Addressee_rights)):
            Pname=result_Addressee_rights[i]["ProjectName"]
         # print("#JOB_RESULT Pname=%s" %  Pname)
            list_Addressee_rights.append(Pname)
          print("#JOB_RESULT list_Addressee_rights=%s" % list_Addressee_rights)
        
          list_sent=[]
          for i in dic_users_rights:
            a=set(list_Addressee_rights).intersection(set(dic_users_rights[i]))
            if a:
              list_sent.append(i)
        
          html1 = """<h><strong>Splunk</strong></h><table border="1" cellspacing="0" bgcolor="#FCFCFC"><tr><td bgcolor="#AEDD81"><big>&nbsp;&nbsp;user</big></td><td bgcolor="#AEDD81"><big>count</big></td><td bgcolor="#AEDD81"><big>&nbsp;&nbsp;lastestTime</big></td></tr>"""
          for i in range(len(result_login_info)):
            #print(result_login_info[i]['user'])
            if result_login_info[i]['user'] in list_sent:
              try:
                user = result_login_info[i]['user']
              except(Exception):
                user = ""
              try:
                count = result_login_info[i]["count"]
                #print(count)
              except(Exception):
                count = ""
              try:
                lastesTime = result_login_info[i]["lastestTime"]
              except(Exception):
                lastesTime = ""
          
              html2 = """<tr><td>%s</td><td>%s</td><td>%s</td></tr>""" % (user, count, lastesTime)
            else:
              continue

            html1 = html1 + html2
          html1 = html1 + "</table>"
          print("#JOB_RESULT list_sent=%s" % list_sent)
          print("#JOB_RESULT result123=%s" % dic_users_rights)
          print("#JOB_RESULT html1=%s" % html1)
          empty_list='<h><strong>Splunk</strong></h><table border="1" cellspacing="0" bgcolor="#FCFCFC"><tr><td bgcolor="#AEDD81"><big>&nbsp;&nbsp;user</big></td><td bgcolor="#AEDD81"><big>count</big></td><td bgcolor="#AEDD81"><big>&nbsp;&nbsp;lastestTime</big></td></tr></table>'
          if html1 == empty_list:
             html1='<h><strong>Splunk</strong></h><table border="1" cellspacing="0" bgcolor="#FCFCFC"><tr><td bgcolor="#AEDD81"><big>&nbsp;&nbsp;user</big></td><td bgcolor="#AEDD81"><big>count</big></td><td bgcolor="#AEDD81"><big>&nbsp;&nbsp;lastestTime</big></td></tr><tr><td><big>-</big></td><td><big>-</big></td><td><big>-</big></td></tr></table>'
          
          result[list_Addressee[b]+"@acpcloud2315outlook.onmicrosoft.com"]=html1
          
        #list_accendant=["paul.guangcao.zhang1@outlook.com"]
        #result["list_accendant"]=list_accendant
        print("#JOB_RESULT result=%s" % result)
    #assigned_to:group and answer , de:question_list close_notes:answer_list
    
    def search_user_list_case51(self,assigned_to,description,close_notes,assigned_group,actual_start,activity_due):
        
        if assigned_group == "510" or assigned_group == "520" or assigned_group == "530" or assigned_group == "540":
          print("#JOB_RESULT aaaaaaaaaa")
          
          csv_num=assigned_group[0:2]+"1"
          print("#JOB_RESULT csv_num=%s" % csv_num)
          csv_question=eval(self.csv_question)[csv_num]
          csv_answer=eval(self.csv_answer)[csv_num]
          if not csv_question or not csv_answer:
             to=urllib.quote(eval(self.receiver)[assigned_group[0:2]])
             subject=urllib.quote(eval(self.subject)[assigned_group[0:2]])
             title=urllib.quote(eval(self.title)[assigned_group[0:2]])
             if not subject:
                subject=" "
             mail="mailto:%s?subject=%s&body=%s" % (to,subject,title)            
             print("#JOB_RESULT result=%s" % mail)
             return " "
          query_question= '| inputlookup %s ' % csv_question
          result_question=self.query_by_app(query_question,"aaam-atr-v3-controlroom-sh")        
          print("#JOB_RESULT result_question=%s" % result_question)

          
          query_answer= '| inputlookup %s '% csv_answer
          result_answer=self.query_by_app(query_answer,"aaam-atr-v3-controlroom-sh")    
          print("#JOB_RESULT result_answer=%s" % result_answer)
          
          if result_question==[] or result_answer==[]:
             to=urllib.quote(eval(self.receiver)[assigned_group[0:2]])
             subject=urllib.quote(eval(self.subject)[assigned_group[0:2]])
             title=urllib.quote(eval(self.title)[assigned_group[0:2]])
             if not subject:
              subject=" "
             mail="mailto:%s?subject=%s&body=%s" % (to,subject,title)            
             print("#JOB_RESULT result=%s" % mail)
             return ""
          else:
             print("#JOB_RESULT result=%s" % {"type":"AdaptiveCard","$schema":"http://adaptivecards.io/schemas/adaptive-card.json","version":"1.2","body":[{"type":"TextBlock","text":"プロジェクト管理ツールの検討や導入のサポート」ですね。","wrap":"true"},{"type":"TextBlock","text":"最後まで処理を完了するためには メールソフト (Outlook)など の 利用が必要となります。","wrap":"true"},{"type":"TextBlock","text":"よろしければ、いくつかの質問にご回答のうえ、こちらがコンタクト送信を ご案内いたします 。","wrap":"true"},{"type":"ActionSet","actions":[{"type":"Action.Submit","title":"質問へ","style":"positive","data":{"msteams":{"type":"messageBack","displayText":"質問へ","text":"質問へ"}}},{"type":"Action.Submit","title":"キャンセル","style":"positive","data":{"msteams":{"type":"messageBack","displayText":"キャンセル","text":"キャンセル"}}}]}]})
             return ""
        if assigned_group == "511" or assigned_group == "521" or assigned_group == "531" or assigned_group == "541":
          csv_question=eval(self.csv_question)[assigned_group]
          csv_answer=eval(self.csv_answer)[assigned_group]

          query_question= '| inputlookup %s ' % csv_question
          result_question=self.query_by_app(query_question,"aaam-atr-v3-controlroom-sh")        
          print("#JOB_RESULT result_question=%s" % result_question)

          
          query_answer= '| inputlookup %s '% csv_answer
          result_answer=self.query_by_app(query_answer,"aaam-atr-v3-controlroom-sh")    
          print("#JOB_RESULT result_answer=%s" % result_answer)
          
          if result_question==[] or result_answer==[]:
             to=urllib.quote(eval(self.receiver)[assigned_group[0:2]])
             subject=urllib.quote(eval(self.subject)[assigned_group[0:2]])
             title=urllib.quote(eval(self.title)[assigned_group[0:2]])
             if not subject:
              subject=" "
             mail="mailto:%s?subject=%s&body=%s" % (to,subject,title)            
             print("#JOB_RESULT result=%s" % mail)
             return ""            
        else:
          result_question=eval(actual_start)
          print("#JOB_RESULT result_question=%s" % result_question)
          result_answer=eval(activity_due)
          print("#JOB_RESULT result_answer=%s" % result_answer) 
        question_context=""

        question_list1=description
        question_list=[]
        dynamic_question=""
        
        next_question=assigned_to.split("___")[0]
        
        if next_question[0]=="m" or next_question[0]=="i":
          next_question=next_question[1:]
        
        answers=assigned_to.split("___",1)[1]
        print("#JOB_RESULT answers1=%s" % answers)
        answers=answers.split("___")
        print("#JOB_RESULT answers2=%s" % answers)        
        qid=""
        answer_list=close_notes
        
        sum=2
        executed=0
        dic_question={}
        dic_answer={}

        mail_context=""
        mail=""
        
        #将答案插入列表
        if answer_list != "1":
            answer_list=eval(answer_list)
            for answer in answers:
                a=0
                if answer =="undefined":
                  answer=""
                print("#JOB_RESULT answer_list=%s" % answer_list)             
                if "|||" in answer:
                  
                  qid=answer.split("|||",1)[0]
                  answer=answer.split("|||",1)[1]
                  print("#JOB_RESULT qqid,answer=%s,%s" % (qid,answer))
                  for i in range(len(answer_list)):
                      if qid == "input":
                          for j in answer_list[i]:

                            if answer_list[i][j] == "bcasd":
                              print("#JOB_RESULT answer3=%s" % answer) 
                              answer_list[i][j]=answer

                              a=1
                              break 
                      if qid in answer_list[i]:
                          mutil_answer=re.search(r"(,\d+\|\|\|)", answer)
                          print("#JOB_RESULT mutil_answer=%s" % mutil_answer)
                          if mutil_answer != None:
                            answer=re.sub("\d\|\|\|","",answer)
                            print("#JOB_RESULT manswer=%s" % answer)
                          answer_list[i][qid]=answer        
                      if a==1:
                        break   
                else:
                  a=0
                  for i in range(len(answer_list)):
                      print("#JOB_RESULT answer44=%s" % answer)
                      for j in answer_list[i]:
                          if answer_list[i][j] == "bcasd":
                            answer_list[i][j]=answer
                            print("#JOB_RESULT answer_list[i][j]1=%s" % answer_list[i][j])
                            #print("#JOB_RESULT answer_list[i][j]=%s" % answer_list[i][j])
                            a=1
                            break
                            
                      if a==1:
                          break
        if next_question == "E":
            question_list1=eval(question_list1) 
            print("#JOB_RESULT question_list1=%s" % question_list1)         
            for q in range(len(question_list1)):
                mq=urllib.quote(question_list1[q].values()[0])
                ma=urllib.quote(answer_list[q].values()[0])
                mail_context=mail_context+"%E2%97%8F"+"%20%20"+mq+"%0d%0a"+"%20%20%20%20%20%20"+ma+"%0d%0a"
                #mail_context=mail_context+question_list1[q].values()[0]+":"+answer_list[q].values()[0]+"%0d%0a"
            print("#JOB_RESULT mail_context=%s" % mail_context)
            to=urllib.quote(eval(self.receiver)[assigned_group])
            subject=urllib.quote(eval(self.subject)[assigned_group])
            title=urllib.quote(eval(self.title)[assigned_group])
            if not subject:
              subject=" "
            ending="%0d%0a%0d%0a%E4%BB%A5%E4%B8%8A"
            mail="mailto:%s?subject=%s&body=%s%s%s%s" % (to,subject,title,"%0d%0a",mail_context,ending)
            print("#JOB_RESULT result=%s" % mail)
            return ""
        print("#JOB_RESULT next_question=%s" % next_question) 

        for i1 in range(len(result_question)):
          print("#JOB_RESULT i1=%s" % i1)
          print("#JOB_RESULT result_question[i1][Question_context]=%s" % result_question[i1]["Question_context"])
          if result_question[i1]["Question_group"]== next_question :
              question_context = result_question[i1]["Question_context"]
              question_id= result_question[i1]["Question_id"]            
              if question_list1 =='1':
                  dic_question={str(question_id):str(question_context)}
                  question_list.append(dic_question)
                  
                  answer_list=[]
                  dic_answer={str(question_id):"bcasd"}
                  answer_list.append(dic_answer)
                  executed=1
                  question_list1=0
                  
             
              elif executed == 0:

                  question_list=eval(question_list1)
                  executed=1
                  dic_question={str(question_id):str(question_context)}
                  question_list.append(dic_question)
                  
                  dic_answer={str(question_id):"bcasd"}
                  answer_list.append(dic_answer)                  
              
              else:
                  dic_question={str(question_id):str(question_context)}
                  print("#JOB_RESULT dic_question=%s" % dic_question)
                  question_list.append(dic_question)
                  
                  dic_answer={str(question_id):"bcasd"}
                  answer_list.append(dic_answer)
              print("#JOB_RESULT question_list=%s" % question_list)  
              list_choice_title=[]
              list_choice_value=[]
              #print("#JOB_RESULT question_list=%s" % question_list)     

              if result_question[i1]["Format"]=="Choice":
                #如果该问题是下拉选框
                for i in range(len(result_answer)):
                  #循环回答表
                  print("#JOB_RESULT Answer_context=%s" % result_answer[i]["Answer_context"])  
                  if result_answer[i]["Question_group"] == next_question and result_answer[i]["Question_id"]== question_id:
                      #查找对应的回答 
                        print("#JOB_RESULT Answer_context=%s" % result_answer[i]["Answer_context"])  
                        list_choice_title.append(result_answer[i]["Answer_context"])
                        if result_answer[i]["Next_question_group"] != "0":
                          list_choice_value.append(result_answer[i]["Next_question_group"]+"___"+result_answer[i]["Question_id"]+"|||"+result_answer[i]["Answer_context"])
                        else:
                          list_choice_value.append(result_answer[i]["Question_id"]+"|||"+result_answer[i]["Answer_context"])
                dynamic_answer=""
                dynamic_answer1=""
                print("#JOB_RESULT list_choice_value=%s" % list_choice_value)
                print("#JOB_RESULT list_choice_title=%s" % list_choice_title)            
                for i in range(len(list_choice_title)):  
                  dynamic_answer1=dynamic_answer1+"""{"title":"%s","value":"%s"},"""% (list_choice_title[i], list_choice_value[i])                        
                if result_question[i1]["Key"] == "True" :
                  dynamic_answer="""{"type":"Input.ChoiceSet","id":"a1","choices":[%s],"style": "expanded","value":"%s"}, """ % (dynamic_answer1[:-1],list_choice_value[0])
                else:
                  dynamic_answer="""{"type":"Input.ChoiceSet","id":"a%s","choices":[%s],"style": "expanded","value":"%s"}, """ % (sum,dynamic_answer1[:-1],list_choice_value[0])
                  sum=sum+1
                dynamic_question=dynamic_question+"""{"type":"TextBlock","text":"%s" ,"wrap":"true"},""" % question_context +dynamic_answer
              
              if result_question[i1]["Format"]=="MultiChoice":
                multi_next_question=""
                for i in range(len(result_answer)):
                  #循环回答表
                  if result_answer[i]["Question_group"] == next_question and result_answer[i]["Question_id"]== question_id:
                      #查找对应的回答 
                        list_choice_title.append(result_answer[i]["Answer_context"])
                        list_choice_value.append(result_answer[i]["Question_id"]+"|||"+result_answer[i]["Answer_context"])
                        multi_next_question=result_answer[i]["Next_question_group"]
                dynamic_answer=""
                dynamic_answer1=""
                #print("#JOB_RESULT list_choice_value=%s" % list_choice_value)
                #print("#JOB_RESULT list_choice_title=%s" % list_choice_title)            
                for i in range(len(list_choice_title)):  
                  dynamic_answer1=dynamic_answer1+"""{"title":"%s","value":"%s"},"""% (list_choice_title[i], list_choice_value[i])                        
                if result_question[i1]["Key"] == "True" :
                  dynamic_answer="""{"type":"Input.ChoiceSet","id":"multi","choices":[%s],"isMultiSelect": "true","style": "expanded","value":"%s"},{"type": "Input.Text","id": "a1","value": "m%s","isVisible": "false"}, """ % (dynamic_answer1[:-1],list_choice_value[0],multi_next_question)
                else:
                  dynamic_answer="""{"type":"Input.ChoiceSet","id":"a%s","choices":[%s],"isMultiSelect": "true","style": "expanded","value":"%s"}, """ % (sum,dynamic_answer1[:-1],list_choice_value[0])
                  sum=sum+1
                dynamic_question=dynamic_question+"""{"type":"TextBlock","text":"%s" ,"wrap":"true"},""" % question_context +dynamic_answer                

              if result_question[i1]["Format"]=="Input":
                dynamic_answer=""
                if result_question[i1]["Key"] == "True" :
                  for i in range(len(result_answer)):
                    #循环回答表
                    if result_answer[i]["Question_group"] == next_question and result_answer[i]["Question_id"]== question_id:
                        #查找对应的回答 
                          input_next_question=result_answer[i]["Next_question_group"]
                          dynamic_answer="""{"type":"Input.Text","id":"input"},{"type": "Input.Text","id": "a1","value": "i%s","isVisible": "false"}, """ % input_next_question
                else:
                  dynamic_answer="""{"type":"Input.Text","id":"a%s"}, """ % sum
                  sum=sum+1
                dynamic_question=dynamic_question+"""{"type":"TextBlock","text":"%s" ,"wrap":"true"},""" % question_context +dynamic_answer                
              
        print("#JOB_RESULT dynamic_question=%s" % dynamic_question[:-1])
           
        card="""{"type":"AdaptiveCard","$schema":"http://adaptivecards.io/schemas/adaptive-card.json","version":"1.2","body":[{"type":"Input.Text","placeholder":"Placeholder text","id":"result_question","value":"%s","isVisible": "false" },{"type":"Input.Text","placeholder":"Placeholder text","id":"result_answer","value":"%s","isVisible": "false" },{"type":"Input.Text","placeholder":"Placeholder text","id":"answer_list","value":"%s","isVisible": "false" },{"type":"Input.Text","placeholder":"Placeholder text","id":"question_list","value":"%s","isVisible": "false" },"""%(result_question,result_answer,answer_list, question_list) + dynamic_question+"""{"type": "ActionSet","actions":[{"type": "Action.Submit", "title":"次へ", "style": "positive","data":{"msteams":{"type":"messageBack","displayText":"次へ","text":"次へ"}}},{"type": "Action.Submit", "title":"メインメニューに戻る", "style": "positive","data":{"msteams":{"type":"messageBack","displayText":"メインメニューに戻る","text":"メインメニューに戻る"}}}]}]}"""               

        #card={"type":"AdaptiveCard","$schema":"http://adaptivecards.io/schemas/adaptive-card.json","version":"1.2","body":[{"type":"Input.Text","placeholder":"Placeholder text","id":"question_list","value":"%s" % "a"},eval(dynamic_question),{"type": "ActionSet","actions":[{"type": "Action.Submit", "title":"送信", "style": "positive","data":{"msteams":{"type":"messageBack","displayText":"送信","text":"送信"}}}]}]}

        print("#JOB_RESULT result=%s" % card)
        
        
if __name__ == '__main__':
    """
      主程序
    """
    user_eid, assigned_group, assigned_to,description,close_notes,actual_start,activity_due = sys.argv[1:]
    decide_name=""
    check_Unumber= assigned_group[0:2]
    decide_list = assigned_group[3:]
    print("#JOB_RESULT assigned_group[0:3]=%s" % assigned_group[0:3])    
    if assigned_group[0:3] != "511" and assigned_group[0:3] != "521" and assigned_group[0:3] != "531" and assigned_group[0:3] != "541" and assigned_group[0:3] != "510"and assigned_group[0:3] != "520"and assigned_group[0:3] != "530" and assigned_group[0:3] != "540":
      assigned_group =assigned_group[0:2]
    if check_Unumber=="32":
        decide_list=decide_list.split("&@$&")
        decide_name=decide_list[1]
        decide_list=decide_list[0]
    print("#JOB_RESULT assigned_to=%s" % assigned_to)
    print("#JOB_RESULT decide_list=%s" % decide_list)
    print("#JOB_RESULT decide_name=%s" % decide_name)
    print("#JOB_RESULT assigned_group=%s" % assigned_group)
    if assigned_group == '12':
        splunk_spl().search_user_list_case12(assigned_to)
        print("#JOB_RESULT step12=%s" % "step12")
    elif assigned_group == '11':
        splunk_spl().search_user_list_case11()
        print("#JOB_RESULT step11=%s" % "step11")
    elif assigned_group == '21':
        file_name = '2015.Dec31.Starts12h.csv'
        user_eid = 'yin.yang@accenture.com'
        splunk_spl().search_user_list_case21(user_eid)
        
    elif assigned_group == '22':
        user_eid = 'yin.yang@accenture.com'
        splunk_spl().search_user_list_case22(user_eid, assigned_to,decide_list)
        print("#JOB_RESULT step22=%s" % "step22")
    elif assigned_group == '31':
        file_name = '2015.Dec31.Starts12h.csv'
        user_eid = 'yin.yang@accenture.com'
        splunk_spl().search_user_list_case21(user_eid) 
    
    elif assigned_group == '32':
        user_eid = 'yin.yang@accenture.com'
        splunk_spl().search_user_list_case32(user_eid, assigned_to,decide_list,decide_name)
    elif assigned_group == '34':
        APP_Name = assigned_to
        
        #print("#JOB_RESULT result11=%s" % decide_list)
        try:
          decide_list= eval(decide_list)
          decide = decide_list[APP_Name]
        except NameError:
          decide="ネットワーク異常、再検索してください。"
        except KeyError:
          decide="入力された項目は存在しません。もう一度入力してください。"
        print("#JOB_RESULT result=%s" % decide)
    elif assigned_group == '41':
        splunk_spl().search_user_list_case41(user_eid)
    elif assigned_group == '42':
        splunk_spl().search_user_list_case42(user_eid)
    elif assigned_group == '43':
        splunk_spl().search_user_list_case43(user_eid)
    elif assigned_group == '51' or assigned_group == '511' or assigned_group == '52' or assigned_group == '521' or assigned_group == '53' or assigned_group == '531' or assigned_group == '54' or assigned_group == '541' or assigned_group == "510" or assigned_group == "520" or assigned_group == "530" or assigned_group == "540" :
        print("#JOB_RESULT description=%s" % description)
        splunk_spl().search_user_list_case51(assigned_to,description,close_notes,assigned_group,actual_start,activity_due)
    else:
        print("#JOB_RESULT assigned_group_check_user=%s" % assigned_group)
