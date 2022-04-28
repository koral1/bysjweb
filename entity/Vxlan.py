import os

class Vxlan:
    def __init__(self,name,goupip,localip,eth0):
        self.__name=name #私有成员变量，前缀为俩条下划线
        self.__state="DOWN" #Down的状态
        self.__type="vxlan"
        os.system("sh shell/create/CreateVxlan.sh "+self.__name+" "+
                  goupip+" "+localip+" "+eth0)
    def delete(self):
        os.system("sh shell/delete/delvxlan.sh "+self.__name)
    def connect2br(self,bridgename):#待测试
        os.system("sh shell/connect/MasterBr.sh "+self.__name+" "+bridgename)
        self.__connectdevice=bridgename  
    def connect(self,DeviceName):
        self.__connectdevice=DeviceName
    def addip(self,IP):
        os.system("sh shell/net/AddIP.sh "+self.__name+" "+IP)
        self.__ip=IP.replace("/24","")
    def setup(self):
        os.system("sudo ip link set "+self.__name+" up")
        self.__state="UP"
    def getname(self):
        return self.__name 
    def getip(self):
        return self.__ip      
    def getstatus(self):
        return self.__status
    def gettype(self):
        return self.__type
    def getconnectdevice(self):
        return self.__connectdevice
    def getstate(self):
        return self.__state

# vxlan1=Vxlan("vxlan1","224.1.1.1","10.211.55.3","enp0s5")
# os.system("ip a")
# print(vxlan1.getstatus())
# print("-----------------------------------------------------------")
# # vxlan1.delete()
# # os.system("ip a")
# vxlan1.addip("10.0.0.1/24")
# vxlan1.setup()
# print(vxlan1.getstatus())
# print("-----------------------------------------------------------")
# os.system("ip a")
# vxlan1.delete()
# print("-----------------------------------------------------------")
# os.system("ip a")