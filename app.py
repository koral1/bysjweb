import json

import os
from flask import Flask
from flask import request,redirect,url_for,session,g,render_template
from entity.Bridge import Bridge
from entity.Netns import Netns

from entity.Veth import Veth
from entity.Vxlan import Vxlan


app = Flask(__name__, static_url_path="/")

def deleteVeth(Device, index):
    if Device in VethFrontList:
        del DeviceList[index]
        del DeviceList[index]
        del DeviceNameList[index]
        del DeviceNameList[index]
        VethFrontList.remove(Device)
    else:
        VethFrontList.remove(DeviceNameList[index - 1])
        del DeviceList[index - 1]
        del DeviceList[index - 1]
        del DeviceNameList[index - 1]
        del DeviceNameList[index - 1]

@app.route("/server/create", methods=['GET', 'POST'])
def create():
    DeviceAddressList = []
    if request.method == 'POST':
        data=request.get_data()
        json_data =json.loads(data.decode("utf-8"))
        type=json_data.get("type")
        name=json_data.get("name1")
        if type == "vethpair":
            vethname = name  # 输入
            vethpeername = json_data.get("name2")  # 输入
            DeviceNameList.append(vethname)
            DeviceNameList.append(vethpeername)
            VethFrontList.append(vethname)
            DeviceList.append(Veth(vethname, vethpeername))  # 把设备添加到list中
            DeviceList.append(Veth(vethpeername, vethname))
            indexVeth = DeviceNameList.index(vethname)
            DeviceList[indexVeth].create()
            index = indexVeth
            index2 = index + 1
            DeviceAddressList.append(hex(id(DeviceList[index])))
            DeviceAddressList.append(hex(id(DeviceList[index2])))
            json_str = json.dumps(DeviceAddressList)
            print("veth")
        elif type == "netns":
            netnsname = name
            DeviceNameList.append(netnsname)
            DeviceList.append(Netns(netnsname))
            index= DeviceNameList.index(netnsname)
            DeviceAddressList.append(hex(id(DeviceList[index])))
            json_str = json.dumps(DeviceAddressList)
            print("netns")
        elif type == "bridge":
            bridgename = name
            DeviceNameList.append(bridgename)
            DeviceList.append(Bridge(bridgename))
            index=DeviceNameList.index(bridgename)
            DeviceAddressList.append(hex(id(DeviceList[index])))
            json_str = json.dumps(DeviceAddressList)
            print("br")
        elif type == "vxlan":
            vxlanname = name
            grouip = json_data.get("name2")
            localip = json_data.get("name3")
            eth0 = json_data.get("name4")
            DeviceNameList.append(vxlanname)
            DeviceList.append(Vxlan(vxlanname, grouip, localip, eth0))
            index= DeviceNameList.index(vxlanname)
            DeviceAddressList.append(hex(id(DeviceList[index])))
            json_str = json.dumps(DeviceAddressList)
            print("vxlan")
        print(DeviceNameList)
        print(DeviceList)
        print(DeviceList[index])
        return json_str #不知道这里传的是网络设备还是字符串，，，用了join方法，最后返回的应该是字符串了

@app.route("/server/connect", methods=['GET', 'POST'])
def connect():
    if request.method == 'POST':
        data=request.get_data()
        json_data =json.loads(data.decode("utf-8"))
        name1=json_data.get("name1")
        name2=json_data.get("name2")
        Device1 = name1
        Device2 = name2
        index1 = DeviceNameList.index(Device1)
        index2 = DeviceNameList.index(Device2)
        if DeviceList[index1].gettype() == "netns":
            os.system("sh shell/connect/VethToNetns.sh " + Device2 + " " + Device1)
            DeviceList[index1].connect(Device2)
            DeviceList[index2].connect(Device1)
        if DeviceList[index2].gettype() == "netns":
            os.system("sh shell/connect/VethToNetns.sh " + Device1 + " " + Device2)
            DeviceList[index1].connect(Device2)
            DeviceList[index2].connect(Device1)
        if DeviceList[index1].gettype() == "bridge":
            os.system("sh shell/connect/MasterBr.sh " + Device2 + " " + Device1)
            DeviceList[index1].connectlist(Device2)
            DeviceList[index2].connect(Device1)
        if DeviceList[index2].gettype() == "bridge":
            os.system("sh shell/connect/MasterBr.sh " + Device1 + " " + Device2)
            DeviceList[index1].connect(Device2)
            DeviceList[index2].connectlist(Device1)
        print(DeviceNameList)
        print(DeviceList)
        return "ip"


@app.route("/server/addip", methods=['GET', 'POST'])
def addip():
    if request.method == 'POST':
        data=request.get_data()
        json_data =json.loads(data.decode("utf-8"))
        name=json_data.get("name")
        Deviceip=json_data.get("ip")
        Device = name
        ip = Deviceip
        index = DeviceNameList.index(Device)
        if DeviceList[index].gettype() != "veth":
            DeviceList[index].addip(ip)
        elif DeviceList[index].gettype() == "veth":
            ConnectedDevice = DeviceList[index].getconnectdevice()
            if ConnectedDevice == "":
                DeviceList[index].addipVeth(ip)
            else:
                indexConnected = DeviceNameList.index(ConnectedDevice)
                ConnectedType = DeviceList[indexConnected].gettype()
                if ConnectedType == "netns":
                    DeviceList[index].addipVethNetns(ip, ConnectedDevice)
                else:
                    DeviceList[index].addipVeth(ip)
        return "ip"

@app.route("/server/setup", methods=['GET', 'POST'])
def setup():
    if request.method == 'POST':
        data=request.get_data()
        json_data =json.loads(data.decode("utf-8"))
        name=json_data.get("name")
        Device = name
        index = DeviceNameList.index(Device)
        if DeviceList[index].gettype() != "veth":
            DeviceList[index].setup()
        elif DeviceList[index].gettype() == "veth":
            ConnectedDevice = DeviceList[index].getconnectdevice()
            if ConnectedDevice == "":
                DeviceList[index].setup()
            else:
                indexConnected = DeviceNameList.index(ConnectedDevice)
                ConnectedType = DeviceList[indexConnected].gettype()
                if ConnectedType == "netns":
                    DeviceList[index].setupVethNetns(ConnectedDevice)
                else:
                    DeviceList[index].setupVeth()
        return "ip"

@app.route("/server/delete", methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        data=request.get_data()
        json_data =json.loads(data.decode("utf-8"))
        name=json_data.get("name")
        Device = name
        index = DeviceNameList.index(Device)
        if DeviceList[index].gettype() == "veth":
            ConnectedDevice = DeviceList[index].getconnectdevice()
            if ConnectedDevice == "":
                DeviceList[index].delete()
                deleteVeth(Device, index)
            else:
                indexConnected = DeviceNameList.index(ConnectedDevice)
                ConnectedType = DeviceList[indexConnected].gettype()
                if ConnectedType == "netns":
                    DeviceList[index].deleteVethNetns(ConnectedDevice)
                    deleteVeth(Device, index)
                else:
                    DeviceList[index].delete()
                    deleteVeth(Device, index)
        elif DeviceList[index].gettype() == "netns":  # 似乎num2等于2，3，4的情况可以合并
            DeviceList[index].delete()
            del DeviceList[index]
            del DeviceNameList[index]
        elif DeviceList[index].gettype() == "bridge":
            DeviceList[index].delete()
            del DeviceList[index]
            del DeviceNameList[index]
        elif DeviceList[index].gettype() == "vxlan":
            DeviceList[index].delete()
            del DeviceList[index]
            del DeviceNameList[index]
        print(DeviceNameList)
        print(DeviceList)
        return "ip"

@app.route("/server/openforward", methods=['GET', 'POST'])
def openforward():
    if request.method == 'POST':
        os.system("sudo	sysctl net.ipv4.conf.all.forwarding=1")
        os.system("sudo iptables -P FORWARD ACCEPT")
        print("openforward")
        return "ip"

@app.route("/server/setroute", methods=['GET', 'POST'])
def setroute():
    if request.method == 'POST':
        data=request.get_data()
        json_data =json.loads(data.decode("utf-8"))
        name=json_data.get("name")
        Netnsname=name #配置和netns相连的veth，以及和veth相连的bridge
        indexNetns=DeviceNameList.index(Netnsname)
        Vethname=DeviceList[indexNetns].getconnectdevice()
        indexVeth=DeviceNameList.index(Vethname)
        VethPeerName=DeviceList[indexVeth].getpeername()
        indexPeerName=DeviceNameList.index(VethPeerName)
        Bridgename=DeviceList[indexPeerName].getconnectdevice()
        indexBr=DeviceNameList.index(Bridgename)
        ipBr=DeviceList[indexBr].getip()
        os.system("sh shell/net/gw.sh "+Netnsname+" "+ipBr+" "+Vethname)
        return "ip"

@app.route("/server/dnat", methods=['GET', 'POST'])
def dnat():
    if request.method == 'POST':
        data=request.get_data()
        json_data =json.loads(data.decode("utf-8"))
        bridge=json_data.get("name")
        ip=json_data.get("ip")
        Bridgename=bridge
        # index=DeviceNameList.index(Bridgename)
        os.system("sh shell/net/DNAT.sh "+ip+" "+Bridgename)
        print("已配置完成,内部虚拟网络访问外网时,将namespace请求中的IP换成外部网络认识的ip,进而达到正常访问外部网络的效果。")
        return "ip"

@app.route("/server/snat", methods=['GET', 'POST'])
def snat():
    if request.method == 'POST':
        data=request.get_data()
        json_data =json.loads(data.decode("utf-8"))
        bridge=json_data.get("name1")
        netns=json_data.get("name2")
        Bridgename = bridge
        Netnsname = netns
        indexNetns = DeviceNameList.index(Netnsname)
        Vethname = DeviceList[indexNetns].getconnectdevice()
        indexVeth = DeviceNameList.index(Vethname)
        ipVeth = DeviceList[indexVeth].getip()
        os.system("sh shell/net/SNAT.sh " + Bridgename + " " + ipVeth)
        print("已配置完成,外部网络若访问tcp的8088端口,则就转发到" + Bridgename + "的80端口。" + "地址为" + ipVeth + ":80")
        return "ip"

@app.route("/server/openserver", methods=['GET', 'POST'])
def openserver():
    if request.method == 'POST':
        data=request.get_data()
        json_data =json.loads(data.decode("utf-8"))
        name=json_data.get("name")
        Netnsname = name
        os.system("sh shell/net/server.sh " + Netnsname)
        return "ip"

@app.route("/server/ping", methods=['GET', 'POST'])
def ping():
    if request.method == 'POST':
        data=request.get_data()
        json_data =json.loads(data.decode("utf-8"))
        cmd=json_data.get("name")
        cmd = input()
        os.system(cmd)
        return "ip"

#提醒kfz设置server/route

@app.route("/")
def login():
    return render_template("index(1).html")



if __name__ == '__main__':
    DeviceList=[]
    DeviceNameList=[]
    VethFrontList=[]
    app.run(host='0.0.0.0')
