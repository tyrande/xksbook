from flask import Flask, Response, json, request, redirect
import time, hashlib, os, xmltodict
import xml.etree.ElementTree as ET
app = Flask(__name__)

@app.route('/')
def hi():
    return 'Hi'

@app.route('/wx', methods=['GET', 'POST'])
def wx():
    if request.method == 'POST':
        wxmsg = receive(request.data)
        print '----1----'
        print wxmsg
        respmsg = {}
        respmsg['ToUserName'] = wxmsg['fromUserName']
        respmsg['FromUserName'] = wxmsg['toUserName']
        respmsg['CreateTime'] = int(time.time())
        respmsg['MsgType'] = 'text'
        respmsg['Content'] = 'HelloKitty'
        print '----2----'
        print respmsg
        return xmltodict.unparse({'xml' : respmsg})
    else:
        return wxauth(request.args)

def wxauth(wxargs):
    try:
        signature = wxargs.get('signature', '')
        timestamp = wxargs.get('timestamp', '')
        nonce = wxargs.get('nonce', '')
        echostr = wxargs.get('echostr', '')
        token = 'xksbook'

        wxlist = [token, timestamp, nonce]
        wxlist.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, wxlist)
        hashcode = sha1.hexdigest()
        print "handle/GET func: hashcode, signature: ", hashcode, signature
        if hashcode == signature:
            return echostr
        else:
            return ""
    except Exception, Argument:
        return Argument

def receive(wxdata):
    if len(wxdata) == 0: return {}
    xmldata = ET.fromstring(wxdata)
    msg = {}
    msg['type'] = xmldata.find('MsgType').text
    msg['toUserName'] = xmldata.find('ToUserName').text
    msg['fromUserName'] = xmldata.find('FromUserName').text
    msg['createTime'] = xmldata.find('CreateTime').text
    msg['msgType'] = xmldata.find('MsgType').text
    msg['msgId'] = xmldata.find('MsgId').text
    if msg['type'] == 'text': msg['content'] = xmldata.find('Content').text.encode("utf-8")
    if msg['type'] == 'image':
        msg['picUrl'] = xmlData.find('PicUrl').text
        msg['mediaId'] = xmlData.find('MediaId').text
    return msg

if __name__ == '__main__':
    app.debug = True
    app.run()
