#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Flask, abort, jsonify
import socket

app = Flask(__name__)


@app.route('/<string:ip>')
def host_ip(ip):
    try:
        # 判断是bot，获取IP
        host = socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.error) as e:
        # 验证失败，应该记录错误，以方便以后处理问题
        # 发送到RabbitMq消息队列，记录错误内容
        abort(500)
    host_ip = socket.gethostbyname(host)
    if host_ip == ip:
        # 如果验证通过，加入search_engine_bot_ip列表,之后显示正常页面
        return jsonify({'ip': ip, 'host': host})


if __name__ == '__main__':
    app.run()
