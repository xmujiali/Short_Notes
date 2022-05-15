# 熟悉常见的Linux命令：

查看帮助文件
```man  xxx```

清理屏幕
```clear```

显示当前目录
```pwd```

改变目录
```
cd \
cd ~
cd ..
cd /home/jli/ABC/DEF
```

查看目录ls
```
ls
ls -l
ls -a
```

复制文件cp, scp
```
cp /home/st2/test/1/*.txt  .
cp  -r 源目录 目标目录
scp -r 源服务器:源服务器路径 目标服务器:目标服务器路径
如果已经登录到源服务器，下面的操作是可以的
scp -r ~/ABC/DEF/ 192.168.3.3:/home/jli/ABC/DEF
等价于
scp -r 192.168.1.2:/home/jli/ABC/DEF/ 192.168.3.3:/home/jli/ABC/DEF
```

移动文件mv, 基本上和cp相似，无需-r参数
删除文件rm
```
rm abc.txt
rm -r 目录名
```

新建目录mkdir

vi编辑器：
```
进入后按a编辑
esc退出编辑
esc +   :wq	保存退出
esc +   :q!	不保存退出

esc +   d 删除行
esc +   p 粘贴
```

其它内容后续再行补充，如果需要可以自行搜索。