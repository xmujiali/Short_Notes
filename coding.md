# 关于编程的一般性建议
- 编写代码只是为了解决问题，成功与否的唯一标准是能否解决达到你的目标。但是具体实现并没有唯一的答案!
- Coder可以对自己编写的代码有更高的要求，但是不能一蹴而就，应该逐步完善。
- 对一个很困难的问题，很难一下子直接找到解决的办法，这是非常正常的。你可以把问题进行拆分，把一个大问题编程n个小问题，每个小问题再变为m个小小问题，直到你可以轻松搞定。每个小/小小问题的答案就构成一段代码，把这些代码连接到一起，Bingo！
- 更好地组织代码的方式是类和函数(面向对象编程和面向过程编程)
- 以函数为例。例如
```
def integer_cubic(num):
    s = 0
    for i in range(num):
        s += num*num
    return s
```
函数事实上是函数的开发者与用户的一个协议，当用户正确提供约定的参数，例如integer_cubic(2)时，函数会返回某种约定的计算(立方)的结果(8)。关键在于：a.用户不必关心函数本身时如何实现的，很烂或者很巧妙都无所谓！b.如果用户胡乱使用，例如integer_cubic('Are you OK!')或者integer_cubic(2.1),都会出错！！！c.你懂的，函数只需要写1次或者0次，却可以调用无数次。

# 一个例子
我们想实现一个用数值方法求方程根的程序。
怎么办？分解一下任务
- 查一下数值求根的算法（二分法、切线法/牛顿法、割线法等等），假定我们选择了牛顿法。

$$ x_{n+1} = x_n - f(x_n)/f'(x_n) $$

- 分步实现
  - 确定函数名字及参数
  - 实现一次迭代
  - 实现多次迭代
  - 增加退出
- 再思考一下这套方法还能修改一下，来处理更加复杂的情形吗？

# 打开文件
-1. open
-2. read/readline/readlines/write/writeline/writelines
-3. close

```
# 打开文件
# r read
# w write
# a append
file = open('abc.csv','w')
# 读取文件
file.write(',1,2,3,4,5,6,7,8,9\n')
for i in range(1,10):
    line = str(i)+','
    for j in range(1,10):
        line += str(i*j) + ','
    file.write(line + '\n')
# 关闭文件
file.close()
```
偷懒并且推荐的办法：
```
with open('abc.csv','w') as file:
    # 读取文件
    file.write(',1,2,3,4,5,6,7,8,9\n')
    for i in range(1,10):
        line = str(i)+','
        for j in range(1,10):
            line += str(i*j) + ','
        file.write(line + '\n')
```

【例题】打开h2o.log，确认其中有
```
    -- Stationary point found.
```
这一行，然后再在全文中找到最后一个SCF Done所在的行
```
 SCF Done:  E(UHF) =  -75.4664269288     A.U. after    8 cycles
```
提取其中的能量。

解决方案的代码如下：
```
with open('h2o.log','r') as file:
    FAIL = True
    contents = file.readlines()
    for line in contents:
       if line == '    -- Stationary point found.\n':
           FAIL = False
    
    if False == FAIL:
        result = None
        for line in contents:
            text = line[0:10]
            if text == ' SCF Done:':
                result = line
    
    if result:
        result = result.split()
        print(result[4])
```