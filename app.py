import json

import os
from flask import Flask
from flask import request,redirect,url_for,session,g,render_template
from entity.Bridge import Bridge
from entity.Netns import Netns

from entity.Veth import Veth
from entity.Vxlan import Vxlan

app = Flask(__name__, static_url_path="/")


@app.route("/server/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        data=request.get_data()
        json_data =json.loads(data.decode("utf-8"))
        type=json_data.get("type")
        name=json_data.get("name1")
        print(type+" "+name)
        if type == 'vethpiar':
            vethname = name  # 输入
            vethpeername = json_data.get("name2")  # 输入
            DeviceNameList.append(vethname)
            DeviceNameList.append(vethpeername)
            VethFrontList.append(vethname)
            DeviceList.append(Veth(vethname, vethpeername))  # 把设备添加到list中
            DeviceList.append(Veth(vethpeername, vethname))
            indexVeth = DeviceNameList.index(vethname)
            DeviceList[indexVeth].create()
        elif type == 'netns':
            print("请输入需要添加的netns设备的名称")
            netnsname = input()
            DeviceNameList.append(netnsname)
            DeviceList.append(Netns(netnsname))
        elif type == 'bridge':
            print("请输入需要添加的bridge备的名称")
            bridgename = input()
            DeviceNameList.append(bridgename)
            DeviceList.append(Bridge(bridgename))
        elif type == 'vxlan':
            print("请输入需要添加的vxlan设备的名称")
            vxlanname = input()
            print("请输入需要添加的vxlan设备的多播ip")
            grouip = input()
            print("请输入需要添加的vxlan设备的本地ip")
            localip = input()
            print("请输入需要添加的vxlan设备的宿主机名称")
            eth0 = input()
            DeviceNameList.append(vxlanname)
            DeviceList.append(Vxlan(vxlanname, grouip, localip, eth0))
        return "ip"

@app.route("/server/connect", methods=['GET', 'POST'])
def connect():
    if request.method == 'POST':
        print(request.get_data())
        data=request.get_data()
        json_data =json.loads(data.decode("utf-8"))
        print(json_data)
        name1=json_data.get("name1")
        name2=json_data.get("name2")
        print(name1+" "+name2)
        return "ip"
#
@app.route("/server/addip", methods=['GET', 'POST'])
def addip():
    if request.method == 'POST':
        print(request.get_data())
        data=request.get_data()
        json_data =json.loads(data.decode("utf-8"))
        print(json_data)
        name=json_data.get("name")
        ip=json_data.get("ip")
        print(name+" "+ip)
        return "ip"

@app.route("/server/setup", methods=['GET', 'POST'])
def setup():
    if request.method == 'POST':
        print(request.get_data())
        data=request.get_data()
        json_data =json.loads(data.decode("utf-8"))
        print(json_data)
        name=json_data.get("name")
        print(name)
        return "ip"

@app.route("/server/delete", methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        print(request.get_data())
        data=request.get_data()
        json_data =json.loads(data.decode("utf-8"))
        print(json_data)
        name=json_data.get("name")
        print(name)
        return "ip"

@app.route("/server/openforward", methods=['GET', 'POST'])
def openforward():
    if request.method == 'POST':
        print("open")
        return "ip"

@app.route("/server/setroute", methods=['GET', 'POST'])
def setroute():
    if request.method == 'POST':
        print(request.get_data())
        data=request.get_data()
        json_data =json.loads(data.decode("utf-8"))
        print(json_data)
        name=json_data.get("name")
        print(name)
        return "ip"

@app.route("/server/dnat", methods=['GET', 'POST'])
def dnat():
    if request.method == 'POST':
        print(request.get_data())
        data=request.get_data()
        json_data =json.loads(data.decode("utf-8"))
        print(json_data)
        bridge=json_data.get("name")
        ip=json_data.get("ip")
        print(bridge+" "+ip)
        return "ip"

@app.route("/server/snat", methods=['GET', 'POST'])
def snat():
    if request.method == 'POST':
        print(request.get_data())
        data=request.get_data()
        json_data =json.loads(data.decode("utf-8"))
        print(json_data)
        bridge=json_data.get("name1")
        netns=json_data.get("name2")
        print(bridge+" "+netns)
        return "ip"

@app.route("/server/openserver", methods=['GET', 'POST'])
def openserver():
    if request.method == 'POST':
        print(request.get_data())
        data=request.get_data()
        json_data =json.loads(data.decode("utf-8"))
        print(json_data)
        name=json_data.get("name")
        print(name)
        return "ip"

@app.route("/server/ping", methods=['GET', 'POST'])
def ping():
    if request.method == 'POST':
        print(request.get_data())
        data=request.get_data()
        json_data =json.loads(data.decode("utf-8"))
        print(json_data)
        cmd=json_data.get("name")
        print(cmd)
        return "ip"

#提醒kfz设置server/route

@app.route("/")
def login():
    return render_template("index(1).html")



if __name__ == '__main__':
    DeviceList=[]
    DeviceNameList=[]
    VethFrontList=[]
    app.run()
