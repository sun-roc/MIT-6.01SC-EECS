import math
def calc():
    env = {}
    while True:
        lists = list(raw_input("% "))
        if len(lists)==1:
            
        else:
            
def my_compute(data):
    for i,value in enumerate(data):
        if value == "=":
            data[0] = float(data[2])
            break
        if value == "*":
            data[i-1] =float(data[i-1]) * float(data[i+1])
            data.pop()
            data.pop()
            break
        if value == "/":
            data[i-1] =float(data[i-1]) * float(data[i+1])
            data.pop()
            data.pop()
            break
        if value == "+":
            data[i-1] = float(data[i - 1]) + float(data[i + 1])
            data.pop()
            data.pop()
            break
        if value == "-":
            data[i-1] = float(data[i - 1]) - float(data[i + 1])
            data.pop()
            data.pop()
            break
    return data
def search (data):
        while True:
            if ")" in data:
                kuohao = data.index(")")
                for i in range(kuohao ,-1,-1): 
                    if data[i] == "(":
                        blank_list = []
                        blank_list = data[i+1:kuohao]
                        new_value = my_compute(blank_list)[0] #将计算完的新值提出来
                        del(data[i:kuohao+1]) #将计算晚的括号从data里面删除掉
                        data.insert(i,new_value) #将计算完的新值插入到里面
                        break
            else:
                break
        return data

