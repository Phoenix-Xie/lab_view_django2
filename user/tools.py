import datetime
import threading
from lab_view_django2.settings import DEFAULT_FROM_EMAIL as FromEmail
import requests
from django.http import HttpResponse
import json
from django.core.mail import send_mail
from lab_view_django2.settings import template_id, page, appid, appsecret
from user.models import Apply, Code2OpenID


def CrossDomainReturn(result):
    response = HttpResponse(json.dump(result), content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response['Access-Control-Max-Age'] = '1000'
    response['Access-Control-Allow-Headers'] = '*'
    return response


# 信息推送
class pushMsgThread(threading.Thread):
    def __init__(self, formId, openId, name, statu, Content):
        super(pushMsgThread, self).__init__()
        self.fromId=formId
        self.openId=openId
        self.name = name
        self.statu = statu
        self.Content=Content

    def run(self):
        pushMsg(self.fromId, self.openId, self.name, self.statu, self.Content)


# 推送消息
def pushMsg(formId, openid, name, statu, message):
    formId = str(formId)
    # print(formId)
    #url = "https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token=ACCESS_TOKEN"
    data = {
        "touser": str(openid),
        "template_id": str(template_id),
        "page": str(page),
        "form_id": str(formId),
        "data": {"keyword1": {"value": str(name)},
                 "keyword2": {"value": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) },
                 "keyword3": {"value": statu},
                 "keyword4": {"value": message}
                 },
        "emphasis_keyword": 'keyword3.DATA'
    }

    while True:
        access_token =get_access_token()
        if access_token==False:
            print("获取access_token失败")
            return

        push_url = 'https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token={}'.format(access_token)
        response=requests.post(push_url, json=data, timeout=3, verify=False)
        errcode=response.json()["errcode"]

        if errcode==40001: #token过期
            get_access_token()
        else:
            break


# 发送邮件
class sendEmailThread(threading.Thread):
    def __init__(self,title,content,toEmail):
        super(sendEmailThread, self).__init__()
        self.content=content
        self.title=title
        self.toEmail=toEmail

    def run(self):
        send_mail(self.title, self.content, FromEmail,
                  [self.toEmail], fail_silently=False)
        # try:
        #     send_mail(self.title,self.content, FromEmail,
        #               [self.toEmail], fail_silently=False)
        # except:
        #     print("发送邮件出错")
        #     pass


# 获取access_token 两小时生效时间
def get_access_token():
    try:
        url = "https://api.weixin.qq.com/cgi-bin/token"
        param = {"grant_type": "client_credential",
                 "appid": appid,
                 "secret": appsecret,
                 }
        result = requests.get(url, params=param)
        result = result.json()
        result = result["access_token"]
        # print(result)
        return result
    except:
        return False


def getOpenId(jscode):

    try:
        code2openid = Code2OpenID.objects.filter(jscode=jscode)
        if code2openid.count()== 0:
            url = "https://api.weixin.qq.com/sns/jscode2session"
            param = {"grant_type": "authorization_code",
                     "appid": appid,
                     "secret": appsecret,
                     "js_code": jscode,
                     }
            result = requests.get(url, params=param)
            result = result.json()
            print(result)
            result = result["openid"]
            Code2OpenID.objects.create(jscode=jscode, openId=result)
        else:
            result = code2openid[0].openId
        return result
    except:
        print("获取openid失败")
