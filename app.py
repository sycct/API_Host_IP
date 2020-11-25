#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Flask, abort, jsonify, g
import socket
import os

from qqwry import QQwry

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def set_app():
    wry = QQwry()
    ip_data_path = os.path.join(os.getcwd(), 'ip_data\\qqwry.dat')
    if os.path.exists(ip_data_path):
        if wry.is_loaded():
            return wry
        else:
            # 如果没有加载数据，首先加载
            wry.load_file(ip_data_path, loadindex=True)
            return wry


wry = set_app()


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


@app.route('/location/<string:ip>')
def location(ip):
    wry = QQwry()
    ip_data_path = os.path.join(os.getcwd(), 'ip_data\\qqwry.dat')
    if os.path.exists(ip_data_path):
        if wry.is_loaded():
            get_location_str = wry.lookup(ip)
        else:
            # 如果没有加载数据，首先加载
            wry.load_file(ip_data_path, loadindex=True)
            get_location_str = wry.lookup(ip)
        if get_location_str is None:
            return jsonify({'result': False})
        else:
            get_country = get_location_str[0]
            get_city = get_location_str[1]
            return jsonify({'result': True, 'country': get_country, 'city': get_city})


if __name__ == '__main__':
    app.run()
