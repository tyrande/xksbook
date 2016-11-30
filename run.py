from flask import Flask, Response, json, request, redirect
import time, hashlib, os
import xml.etree.ElementTree as ET
app = Flask(__name__)

@app.route('/')
def hi():
    return 'Hi'

@app.route('/wx', methods=['GET', 'POST'])
def wx():
    try:
        signature = request.args.get('signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')
        echostr = request.args.get('echostr', '')
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

if __name__ == '__main__':
    app.debug = True
    app.run()
