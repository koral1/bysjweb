import os

class Veth:
    def __init__(self,name,peername):
        self.__name=name #私有成员变量，前缀为俩条下划线
        self.__peername=peername #私有成员变量，前缀为俩条下划线
        self.__type="veth"
        self.__state="DOWN"
        self.__connectdevice=""
    def create(self): #在终端创建
        os.system("sh shell/create/CreateVethPair.sh "+self.__name+" " +self.__peername)
        #os.system("sudo ip link add "+self.__name+" type veth peer name "+self.__peername)
    def delete(self): #删除
        os.system("sh shell/delete/delveth.sh "+self.__name)
    def deleteVethNetns(self,netnsname):
        os.system("sh shell/delete/delveth.sh "+self.__name+" "+netnsname)
    def veth2netns(self,netnsname): #连接到netns上,待测试
        os.system("sudo ip netns exec "+netnsname+" ip link delete "+self.__name)
    def connect(self,DeviceName):#待定
        self.__connectdevice=DeviceName
    def addipVeth(self,IP):
        os.system("sh shell/net/AddIP.sh "+self.__name+" "+IP)
        self.__ip=IP.replace("/24","")
    def addipVethNetns(self,IP,Netns):
        os.system("sh shell/net/AddIP.sh "+self.__name+" "+IP+" "+Netns)
        self.__ip=IP.replace("/24","")
    def setupVeth(self):
        os.system("sudo ip link set "+self.__name+" up")
        self.__state="UP"
    def setupVethNetns(self,netnsname):
        os.system("sudo ip netns exec "+netnsname+" ip link set "+self.__name+" up")
        self.__state="UP"    
    def getname(self):
        return self.__name 
    def getpeername(self):
        return self.__peername
    def getip(self):
        return self.__ip
    def gettype(self):
        return self.__type
    def getconnectdevice(self):
        return self.__connectdevice
    def getstate(self):
        return self.__state



# veth1=Veth("veth1","veth1_p")
# veth1_p=Veth("veth1_p","veth1")
# print(veth1.getname())
# print(veth1.getpeername())
# os.system("ip a")
# veth1.delete()
# os.system("ip a")
