


# 最初 无参数
def set_func(func):
    def call_func():
        func()
    return call_func

@set_func
def index():
    print('我是第一个闭包')
#
# 展开来看闭包的原理:
# 就是把index当作参数传递给set_func, 得到一个对象obj,这个对象是指向call_func,与原本
# 的index函数已经没有联系,obj被调用后，其中的func指向index,从而调用了index()函数。这与我们直接看到的调用index有些区别
# func = set_func(index)
# 我们看似调用的index(),其实是在调用call_func
# index()



# 进化版的需要传入参数
def set_func(func):
    def call_func(m):
        func(m)
    return call_func

@set_func
def index(m):
    print('我是需要传入参数%s的闭包函数'%(m))
index(100)
# 对于需要参数的数据，这里可以理解为obj==>call_func需要参数(m), 既call_func(m)，而func指向的是index,
# index 需要参数，所以 func 也就需要参数 既 func(m). 这里可以写成通用版本

def set_func(func):
    def call_func(*args, **kwargs):
        func(*args, **kwargs)
    return call_func


# 进阶3 多个装饰器装饰一个函数




def set_func1(func):
    def call_func1(*args, **kwargs):
        print('*************闭包1')
        func(*args, **kwargs)
    return call_func1


def set_func2(func):
    def call_func2(*args, **kwargs):
        print('*************闭包2')
        func(*args, **kwargs)
    return call_func2

@set_func1
@set_func2
def index():
    print('我是调用多个闭包的函数')

多个装饰器装饰一个函数
当有多个装饰器装饰一个函数时，分析如下：
第一步，距离函数最近的那个装饰器先装饰函数 obj1 = set_func2(index)
第二步 把obj当成一个函数，set_func1对obj进行装饰， obj2 = set_func1(obj1)
此时装饰的效果就是我们得到的obj2指向的是call_func1
当我们在调用index()实际上是在执行call_func1,call_func1执行后执行obj1指向的对象call_func2,call_func2执行后
会执行func,最后执行index
所以我们看到的执行结果是如上所示



# 进阶3 一个装饰器装饰多个函数


def set_func2(func):
    def call_func2(*args, **kwargs):
        print('*************闭包')
        func(*args, **kwargs)
    return call_func2

@set_func2
def index1():
    print('函数1')
    
@set_func2
def index2():
    print('函数2')

# 一个装饰器装饰多个函数与装饰一个函数的分析是一样的



# 进阶5 使用装饰器简化问题


URL_FUNT_DICT = dict()
def route(url):
    def set_func(func):
        URL_FUNT_DICT[url] = func
        def call_func(*args, **kwargs):
            return func(*args, **kwargs)
        return call_func
    return set_func
@route('index')
def index():
    pass

# index()
# print(URL_FUNT_DICT)