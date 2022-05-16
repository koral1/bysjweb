# bysjweb
1.由于项目需要在linux环境下运行，所以部署在了服务器上，把post的地址改成了47.110.233.28（也就是服务器的地址）
如果需要改成别的服务器地址，如：
本地：127.0.0.1
其他服务器：ip地址
则在templates的index(1).html文件中把47.110.233.28全部替换成目标文件地址即可。pycharm中替换快捷键:cmd+r

2.项目的启动方式：sudo python3 app.py

3.项目的环境：ubuntu
sudo apt install net-tools
sudo apt install bridge-utils -y
sudo apt install python3-pip
sudo pip3 install flask

4.要先创建net1，再创建其他的，不然如果先创建veth，再创建net1,那么前端的veth图片会被net1盖住

5.删除veth要删除不在netns里的，不然可能找不到veth1

6.如果前端页面的控制台上有红色的issues标红，可以点击hide issues like that。已知的飘红的issues是希望可以配置cookie的环境，实现跨域访问。