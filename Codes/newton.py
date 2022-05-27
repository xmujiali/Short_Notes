'''
牛顿法求方程的根,原理：
        x_n+1 = x_n - f(x_n)/f'(x_n)

'''
import numpy as np

def newton(x_old, f, f_prime, delta=1e-4, N=100):
    # 确定函数名字及参数

    # 实现一次迭代
    # x1 = x0 - f(x0) / f_prime(x0)
    # 实现多次迭代
    for i in range(N):
        x_new = x_old - f(x_old) / f_prime(x_old)
        print(x_new)
        if np.abs(x_new-x_old)<delta:
            print('Founded:',x_new)
            return x_new
        x_old=x_new

    # 增加退出条件
    return x_new

def f1(x):
    return x**2 - 2
def f_prime1(x):
    return 2 * x

if __name__ == '__main__':
    res = newton(1.4,f=f1, f_prime=f_prime1, delta=1e-1000)
    print(res)