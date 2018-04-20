def strip(path):
    '''把windows路径中的'\'改成'/'，去除'static'开头
    '''
    # 转换分隔符
    path = path.replace('\\', '/')
    # 去除'static/'
    path = path.split('static/')[1]
    return path



if __name__ == '__main__':
    print(strip('static/pic\\original\\20180420185339.jpg'))
