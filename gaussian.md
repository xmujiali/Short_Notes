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

## 几何优化
几何优化的目的在于寻找势能面上的极小点。还可以用来搜索1级的鞍点（过渡态TS），高级鞍点。目前，我们只关心极小点。

```
 Variable       Old X    -DE/DX   Delta X   Delta X   Delta X     New X
                                 (Linear)    (Quad)   (Total)
    R1        2.94797  -0.37366   0.00000  -0.30000  -0.30000   2.64797
         Item               Value     Threshold  Converged?
 Maximum Force            0.373659     0.000450     NO
 RMS     Force            0.373659     0.000300     NO
 Maximum Displacement     0.150000     0.001800     NO
 RMS     Displacement     0.212132     0.001200     NO
 Predicted change in Energy=-1.000297D-01
 Lowest energy point so far.  Saving SCF results.
 GradGradGradGradGradGradGradGradGradGradGradGradGradGradGradGradGradGrad



 Variable       Old X    -DE/DX   Delta X   Delta X   Delta X     New X
                                 (Linear)    (Quad)   (Total)
    R1        2.04630  -0.00006  -0.00003   0.00000  -0.00003   2.04626
         Item               Value     Threshold  Converged?
 Maximum Force            0.000062     0.000450     YES
 RMS     Force            0.000062     0.000300     YES
 Maximum Displacement     0.000017     0.001800     YES
 RMS     Displacement     0.000024     0.001200     YES
 Predicted change in Energy=-1.022867D-09
 Optimization completed.
    -- Stationary point found.

```

```
控制优化的收敛精度,必须要配合其他的设置如SCF，Int等
opt=VeryTight
opt=Tight
opt=Loose

opt=(MaxCycles=N) 作opt的次数
opt=(MaxStep=N)
控制opt时改变结构的最大长度或角度，单位是0.01N Bohr or radians，默认的N为30。在09之前，此方案是无效的，此前是直接使用IOP去控制,参考
http://sobereva.com/93
???

重启优化
opt=restart
```

opt的一个重要内容是限制性优化。可以参考：
http://bbs.keinsci.com/thread-9022-1-1.html

此外Gaussian 16中还提供了Generalized Internal Coordinate (GIC)，不会用。
另外，补充一个水分子的例子。
```
%chk=test.chk
%mem=2000MB
#p hf/3-21G opt=z-matrix

test

0       1
O
H       1       B1
H       1       B2      2 A
Variables:
        B1=0.9
        B2=1.1
Constants:
        A=100.0
```
【练习】利用这个方案，绘制一个H2O的HF能量～B1的图，对比B1很大的时候，分子HF能量与E(OH)+E(H)是否相同？
输入文件如下：
```
%chk=h.chk
%mem=2000MB
%CPU=4
#p hf/3-21G 

h

0       2
H

```
```
%chk=oh.chk
%mem=2000MB
%CPU=4
#p hf/3-21G opt

h

0       2
O
H       1       1.0

```
```
%chk=h2o.chk
%mem=2000MB
%CPU=4
#p hf/3-21G opt=z-matrix  guess=read

test

0       1
O
H       1       B1
H       1       B2      2 A
Variables:
        A=100.0
        B2=1.1
Constants:
        B1=0.9
```
修改最后的Constants中B1的值，即可实现对第一个O-H键长的柔性扫描（区分柔性扫描与刚性扫描！）。从下面的数据可以看到，HF/3-21G确实可以描述在0.9x埃附近的能量最低点，但是其对解离行为的描述是错误的！原因在于B1很大的时候，化学上应该将该体系视为一个H原子和一个OH自由基，但是HF（UHF也没求）要求电子配对，使得实际上描述的是一个H+和一个OH-，这是错误的。
可以使用guess=mix来破坏alpha和beta电子轨道的对称性，构造出alpha电子在H上，beta电子在OH上的波函数，立即就能解决这一问题。


```
                  HF/3-21G
E(H)=           -0.496198636018
E(OH)=          -74.9702282708
E(H)+ E(OH)=    -75.466426906818
	
B1                E(HF/3-21)
0.5             -74.7995664071
0.6             -75.2431743965
0.7             -75.4525630025
0.8             -75.5464264096
0.9             -75.5810437519
1.0             -75.5849818205
1.1             -75.5732362682
1.2             -75.5536084412
1.4             -75.5052553503
1.6             -75.4555725268
1.8             -75.4097320289
2.0             -75.3690417627
2.5             -75.2890867806
3.0             -75.2356074388
3.5             -75.2032240825
4.0             -75.1852939483
5.0             -75.1684056051
6.0             -75.1592141297
7.0             -75.152785143
8.0             -75.1479867191
9.0             -75.144265932
10.0            -75.1412956315
20.0            -75.1279839048
50.0            -75.1200258437
100.0           -75.117375752
100.0           -75.4664269288 (guess=mix)
```





## freq
frequency 几个主要作用：
- 检验优化的结构是否是local minimum。因此必须要在opt成功的结构上，采用相同的方法/基组进行frequency计算。
【练习】构造一个乙烷的重叠式构象，优化并计算频率，就会发现虚频。
- 给出振动频率，进而获得预测的红外/拉曼光谱(freq=Raman)。
- 利用统计热力学给出相关的热力学量，如$S, C_V, \Delta H,\Delta G$等等。


## NLO(Non-Linear Optics)，关键字是polar
MultiWFN是一个波函数分析软件，可以方便地帮助我们读取非线性光学系数。
http://sobereva.com/multiwfn/

http://sobereva.com/231

【联系】熟悉MultiWFN的操作；使用Excel表格实现MultiWFN的计算（注意，Gaussian给出的是input orientation的结果，而MultiWFN给出的standard orientation的结果，这将导致某些与取向相关的结果会不一致！