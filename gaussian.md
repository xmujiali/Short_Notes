# Gaussian使用

## 提交Gaussian的计算(假定使用Gaussian 16)
提交计算任务
```g16  xxx.gjf  &```
会自动地生成xxx.log文件作为输出（windows下输出是xxx.out)

如果没有在最后加上&，任务将在当前shell中运行，你只能等待任务结束才能进行其它操作，而且此时断线或者退出都会直接中断任务！！！所以，正式的计算务必使用&，让任务在后台运行。如果要查看任务情况请使用 ps或top。


# 输入文件中一定要写check文件
使用checkpoint文件的最大优点是可以从某个中间结果继续计算，而不必从头开始。
假如你已经进行了CO2的HF计算，希望进行MP2的计算，那么可以这样做(假定test_CO2.chk是HF计算的chk文件)
```
%oldchk=test_CO2.chk
%chk=test_CO2_MP2.chk
#P MP2/6-31+G* geometry=check guess=read

CO2

0       1
```

## 单点能计算SP(可以不写SP)
单点能/SCF计算是一切量化计算的基础，其目的在于获得给定几何结构下的波函数。
一下是一些你最需要了解的内容：
命令行的开头，#表示正常的输出，#T表示给出更简的输出，#P表示给出更详尽的输出，推荐。
```#```
控制SCF计算的精度
`scf=tight 或者 scf=(loose)`
MaxCycle给出SCF迭代次数的上限，超过会直接停止。
`scf=(tight,MaxCycle=512)`
qc, xqc, yqc使用不同的迭代算法，对于特别难收敛的体系才需要考虑采用，并且会大大增加SCF计算所耗费的时间
```
scf=(qc)
scf=(xqc)
scf=(yqc)
```
放松对称性判断的标准，可以使用`symm=(loose) `,推荐用GV更方便
关闭对称性可以使用`symm=None`

## opt
opt关键字除可以寻找能量极小点之外，还可以寻找过渡态、鞍点等。目前我们暂时只关注能量极小点。

```
控制优化的精度,但是需要配合其它设置才有意义。
opt=verytight
opt=tight
opt=loose


opt=restart
opt=
```






## freq
frequency 几个主要作用：
- 检验优化的结构是否是local minimum。因此必须要在opt成功的结构上，采用相同的方法/基组进行frequency计算。
- 给出振动频率，进而获得预测的红外/拉曼光谱。
- 利用统计热力学给出相关的热力学量，如$S, C_V, \Delta H,\Delta G$等等。


## NLO(Non-Linear Optics)，关键字是polar

