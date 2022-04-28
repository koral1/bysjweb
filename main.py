from html.entities import entitydefs
import os
import cgi,cgitb
from sqlite3 import connect
from entity.Bridge import Bridge
from entity.Netns import Netns

from entity.Veth import Veth
from entity.Vxlan import Vxlan


def showallmenu(): #修改网络设备的功能先不做
    print("----请选择操作----")
    print("1.创建虚拟网络设备")
    print("2.连接虚拟网络设备")
    print("3.为网络设备配置ip")
    print("4.启动网络设备")
    print("5.删除网络设备")   
    # print("6.查看网络设备")
    # print("7.修改网络设备")
    print("6.配置路由")
    print("7.ping")
    print("8.退出")
    
def choosedevice():
    print("1.vethpair")
    print("2.netns")
    print("3.bridge")
    print("4.vxlan")

def showcremenu():
    print("请选择添加的设备")
    choosedevice()
    
def showdelmenu():
    print("请选择删除的设备类型")
    choosedevice()

def inputdevice():
    print("请输入设备名称：")

def showipmenu():
    print("请选择配置ip的设备类型") 
    choosedevice()
    
def showinfo():
    print("请选择需要查看的设备类型")
    choosedevice()
  
def iptablesmenu():
    print("---请选择配置路由的操作---")
    print("1.开启转发相关配置")
    print("2.配置默认路由")
    print("3.配置DNAT规则")
    print("4.配置SNAT规则")
    print("5.在net中启动一个server") 

def create():#注意，要先删除veth再删除netns，不然删除netns时，如果该netns与veth是相连的，那么会顺便把vethpair删除
    num2=input()
    if num2=='1':
        print("请输入veth和veth_p的名称")
        vethname=input() #输入
        vethpeername=input() #输入
        DeviceNameList.append(vethname)
        DeviceNameList.append(vethpeername)
        VethFrontList.append(vethname)
        DeviceList.append(Veth(vethname,vethpeername)) #把设备添加到list中
        DeviceList.append(Veth(vethpeername,vethname))
        indexVeth=DeviceNameList.index(vethname) 
        DeviceList[indexVeth].create()
    elif num2=='2':
        print("请输入需要添加的netns设备的名称")
        netnsname=input()
        DeviceNameList.append(netnsname)
        DeviceList.append(Netns(netnsname))
    elif num2=='3':
        print("请输入需要添加的bridge备的名称")
        bridgename=input()
        DeviceNameList.append(bridgename)
        DeviceList.append(Bridge(bridgename))
    elif num2=='4':
        print("请输入需要添加的vxlan设备的名称")
        vxlanname=input()
        print("请输入需要添加的vxlan设备的多播ip")
        grouip=input()
        print("请输入需要添加的vxlan设备的本地ip")
        localip=input()
        print("请输入需要添加的vxlan设备的宿主机名称")
        eth0=input()
        DeviceNameList.append(vxlanname)
        DeviceList.append(Vxlan(vxlanname,grouip,localip,eth0))
    print(DeviceNameList)
    print(DeviceList)

        
# def delete():
#     num2=input()
#     print("请选择需要删除的设备名称")
#     if num2=='1':
#         vethname=input()
#         indexVeth=DeviceNameList.index(vethname)
#         DeviceList[indexVeth].delete()
#         del DeviceList[indexVeth]
#         del DeviceList[indexVeth]
#         del DeviceNameList[indexVeth]
#         del DeviceNameList[indexVeth]
#     elif num2=='2': #似乎num2等于2，3，4的情况可以合并
#         netnsname=input()
#         indexNetns=DeviceNameList.index(netnsname)
#         DeviceList[indexNetns].delete()
#         del DeviceList[indexNetns]
#         del DeviceNameList[indexNetns]
#     elif num2=='3':
#         bridgename=input()
#         indexBr=DeviceNameList.index(bridgename)
#         DeviceList[indexBr].delete()
#         del DeviceList[indexBr]
#         del DeviceNameList[indexBr]      
#     elif num2=='4':
#         vxlanname=input()
#         indexVxlan=DeviceNameList.index(vxlanname)
#         DeviceList[indexVxlan].delete()
#         del DeviceList[indexVxlan]
#         del DeviceNameList[indexVxlan]  
#     print(DeviceNameList)
#     print(DeviceList)
    
def delete():
    print("请输入需要删除的设备名称")
    Device=input()
    index=DeviceNameList.index(Device)
    # 又有两个bug了，第一个是，这里删的一直是veth设备后面的设备，但是不一定是一对veth
    # 目前想法是创建一个VethFrontlist，记录在前面的veth，如果veth在VethFrontlist里
    # 就按照这里已写好的方法，如果不是，就del DeviceList[index-1]
    #第二个bug是“cannot find veth1”,找不到veth1设备，这里和上面veth设备需要判断connectDevice是不是netns类型的同理
    #明天按照这个改好就好
    if DeviceList[index].gettype()=="veth":
        ConnectedDevice=DeviceList[index].getconnectdevice()
        if ConnectedDevice=="":
            DeviceList[index].delete() 
            deleteVeth(Device,index)
        else :
            indexConnected=DeviceNameList.index(ConnectedDevice)
            ConnectedType=DeviceList[indexConnected].gettype()
            if ConnectedType=="netns":
                DeviceList[index].deleteVethNetns(ConnectedDevice)
                deleteVeth(Device,index)
            else:
                DeviceList[index].delete()
                deleteVeth(Device,index)           
    elif DeviceList[index].gettype()=="netns": #似乎num2等于2，3，4的情况可以合并
        DeviceList[index].delete()
        del DeviceList[index]
        del DeviceNameList[index]
    elif DeviceList[index].gettype()=="bridge":
        DeviceList[index].delete()
        del DeviceList[index]
        del DeviceNameList[index]      
    elif DeviceList[index].gettype()=="vxlan":
        DeviceList[index].delete()
        del DeviceList[index]
        del DeviceNameList[index]  
    print(DeviceNameList)
    print(DeviceList)
    
def deleteVeth(Device,index):
    if Device in VethFrontList:
        del DeviceList[index] 
        del DeviceList[index] 
        del DeviceNameList[index]
        del DeviceNameList[index]
        VethFrontList.remove(Device)
    else:
        VethFrontList.remove(DeviceNameList[index-1])
        del DeviceList[index-1] 
        del DeviceList[index-1] 
        del DeviceNameList[index-1]
        del DeviceNameList[index-1]    
    

def connect(): #该函数仅支持
    print("请输入需要连接的设备1")
    Device1=input()
    print("请输入需要连接的设备2")
    Device2=input() 
    index1=DeviceNameList.index(Device1)
    index2=DeviceNameList.index(Device2)
    if DeviceList[index1].gettype()=="netns":
        os.system("sh shell/connect/VethToNetns.sh "+Device2+" "+Device1)
        DeviceList[index1].connect(Device2)
        DeviceList[index2].connect(Device1)
    if DeviceList[index2].gettype()=="netns":
        os.system("sh shell/connect/VethToNetns.sh "+Device1+" "+Device2)
        DeviceList[index1].connect(Device2)
        DeviceList[index2].connect(Device1)        
    if DeviceList[index1].gettype()=="bridge":
        os.system("sh shell/connect/MasterBr.sh "+Device2+" "+Device1)
        DeviceList[index1].connectlist(Device2)
        DeviceList[index2].connect(Device1)
    if DeviceList[index2].gettype()=="bridge":
        os.system("sh shell/connect/MasterBr.sh "+Device1+" "+Device2)
        DeviceList[index1].connect(Device2)   
        DeviceList[index2].connectlist(Device1)     
    print(DeviceNameList)
    print(DeviceList)
    
def addip():#调试，结果都对
    print("请输入需要添加ip的设备")
    Device=input()
    print("请输入需要添加给设备的ip地址")
    ip=input()
    index=DeviceNameList.index(Device)
    if DeviceList[index].gettype()!="veth":
        DeviceList[index].addip(ip)
        # os.system("sh shell/net/AddIP.sh "+Device+" "+ip)
    elif DeviceList[index].gettype()=="veth":
        ConnectedDevice=DeviceList[index].getconnectdevice()
        if ConnectedDevice=="":
            DeviceList[index].addipVeth(ip)
            # os.system("sh shell/net/AddIP.sh "+Device+" "+ip)
        else :
            indexConnected=DeviceNameList.index(ConnectedDevice)
            ConnectedType=DeviceList[indexConnected].gettype()
            if ConnectedType=="netns":
                DeviceList[index].addipVethNetns(ip,ConnectedDevice)
                # os.system("sh shell/net/AddIP.sh "+Device+" "+ip+" "+ConnectedDevice) 
            else:
                DeviceList[index].addipVeth(ip)
                # os.system("sh shell/net/AddIP.sh "+Device+" "+ip)
            

def setup():#未调试
    print("请输入你想要启动的设备")
    Device=input()
    index=DeviceNameList.index(Device)
    if DeviceList[index].gettype()!="veth":
        DeviceList[index].setup()
    elif DeviceList[index].gettype()=="veth":
        ConnectedDevice=DeviceList[index].getconnectdevice()
        if ConnectedDevice=="":
            DeviceList[index].setup()
        else :
            indexConnected=DeviceNameList.index(ConnectedDevice)
            ConnectedType=DeviceList[indexConnected].gettype()
            if ConnectedType=="netns":
                DeviceList[index].setupVethNetns(ConnectedDevice)
            else:
                DeviceList[index].setupVeth()
    
def iptables():
    print("请选择需要进行的ip操作")  
    num2=input()
    if num2=='1':
        os.system("sudo	sysctl net.ipv4.conf.all.forwarding=1")
        os.system("sudo iptables -P FORWARD ACCEPT")#开启转发功能
    elif num2=='2':  
        print("请输入需要配置路由的设备")
        print("netns设备0w6")
        Netnsname=input() #配置和netns相连的veth，以及和veth相连的bridge
        indexNetns=DeviceNameList.index(Netnsname)
        Vethname=DeviceList[indexNetns].getconnectdevice()
        indexVeth=DeviceNameList.index(Vethname)
        VethPeerName=DeviceList[indexVeth].getpeername()
        indexPeerName=DeviceNameList.index(VethPeerName)
        Bridgename=DeviceList[indexPeerName].getconnectdevice()
        indexBr=DeviceNameList.index(Bridgename)
        ipBr=DeviceList[indexBr].getip()
        os.system("sh shell/net/gw.sh "+Netnsname+" "+ipBr+" "+Vethname)
    elif num2=='3':  
        print("请输入要设置的bridge设备")
        Bridgename=input()
        index=DeviceNameList.index(Bridgename)
        print("请输入该虚拟网络的网段")
        ip=input()
        os.system("sh shell/net/DNAT.sh "+ip+" "+Bridgename)
        print("已配置完成,内部虚拟网络访问外网时,将namespace请求中的IP换成外部网络认识的ip,进而达到正常访问外部网络的效果。")
    elif num2=='4':  
        print("请输入要设置的bridge设备")
        Bridgename=input()
        print("请输入需要配置的netns设备")
        Netnsname=input()
        indexNetns=DeviceNameList.index(Netnsname)
        Vethname=DeviceList[indexNetns].getconnectdevice()
        indexVeth=DeviceNameList.index(Vethname)
        ipVeth=DeviceList[indexVeth].getip()    
        os.system("sh shell/net/SNAT.sh "+Bridgename+" "+ipVeth)
        print("已配置完成,外部网络若访问tcp的8088端口,则就转发到"+Bridgename+"的80端口。"+"地址为"+ipVeth+":80")
    elif num2=='5':  
        print("请输入将启动server的netns设备")
        Netnsname=input()
        os.system("sh shell/net/server.sh "+Netnsname)

def ping():
    print("请输入")
    cmd=input()
    os.system(cmd)

if __name__ == "__main__":
    DeviceList=[]
    DeviceNameList=[]
    VethFrontList=[]
    while True:
        showallmenu()
        num=input('请选择：')
        if num=='1':
            showcremenu()
            create() 
        elif num=='2':
            connect()
        elif num=='3':
            addip()
        elif num=='4':
            setup()
        elif num=='5':
            delete()            
        elif num=='6':
            iptablesmenu()
            iptables()
        elif num=='7':
            ping()
        # elif num=='8':
        # elif num=='9':
        elif num=='8':
            break
        