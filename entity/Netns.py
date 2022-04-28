import os

class Netns:
    def __init__(self,name):
        self.__name=name #私有成员变量，前缀为俩条下划线
        self.__type="netns"
        os.system("sh shell/create/CreateNetns.sh "+self.__name)
    def delete(self):
        os.system("sh shell/delete/delnetns.sh "+self.__name)
    def getname(self):
        return self.__name 
    def connect(self,DeviceName):
        self.__connectdevice=DeviceName
    def gettype(self):
        return self.__type
    def getconnectdevice(self):
        return self.__connectdevice

# net1=Netns("net1")
# print(net1.getname())
# os.system("sudo ip netns list")
# print("------------------------------------")
# net1.delete()
# os.system("sudo ip netns list")