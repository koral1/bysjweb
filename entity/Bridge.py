import os

class Bridge:
    def __init__(self,name):
        self.__name=name #私有成员变量，前缀为俩条下划线
        self.__connectlist=[] #brigde用connectlist,其他都是用connectdevice
        self.__type="bridge"
        self.__state="DOWN"
        os.system("sh shell/create/CreateBr.sh "+self.__name)
    def delete(self):
        os.system("sh shell/delete/delbr.sh "+self.__name)
    # def connect2br(self,DeviceName):#待测试
    #     os.system("sh shell/connect/MasterBr.sh "+DeviceName+" "+self.__name)
    #     self.__connectlist.append(DeviceName)
    def connectlist(self,DeviceName):
        self.__connectlist.append(DeviceName)
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
    def gettype(self):
        return self.__type
    def getconnectlist(self):
        return self.__connectlist
    def getstate(self):
        return self.__state
        
        
        
# br1=Bridge("br1")
# os.system("ip a")
# print(br1.getname())
# br1.delete()
# os.system("ip a")