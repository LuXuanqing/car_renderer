import cv2

def strip(path):
    '''把windows路径中的'\'改成'/'，去除'static'开头
    '''
    # 转换分隔符
    path = path.replace('\\', '/')
    # 去除'static/'
    path = path.split('static/')[1]
    return path


def img_prep(src, dst):
    #读取图片
    img = cv2.imread(src)
    h, w, _ = img.shape
    if w >= h:
        scaling_ratio = 256. / w
    else:
        scaling_ratio = 256. / h

    #对图片进行缩放
    img_resize = cv2.resize(img, None, fx=scaling_ratio,
                            fy=scaling_ratio, interpolation=cv2.INTER_CUBIC)

    #填充边缘部分
    h_resize, w_resize, _ = img_resize.shape  # 读取resize后的尺寸
    top_padding = (256 - h_resize) // 2  # 填充像素数量必须为整数
    bottom_padding = 256 - h_resize - top_padding
    left_padding = (256 - w_resize) // 2
    right_padding = 256 - w_resize - left_padding
    img_resize_padding = cv2.copyMakeBorder(
        img_resize,
        top_padding,
        bottom_padding,
        left_padding,
        right_padding,
        cv2.BORDER_REPLICATE)  # 用重复边缘像素值的方式填充

    #保存图片
    cv2.imwrite(dst, img_resize_padding)


if __name__ == '__main__':
    pass
