#encoding = utf-8
'''
部署到其他机器后, 请修改convert函数里的图片读取保存路径
convert函数实现输入一张任意尺寸(小于opencv支持的最大尺寸就行)图片, 自动完成图片缩放+补边+上色并保存到默认路径
'''

import tensorflow as tf
from model import CycleGAN
import utils

def color(src, dst):
  FLAGS = tf.flags.FLAGS
  tf.flags.DEFINE_string('model', 'pretrained/sketch2render.pb', 'model path (.pb)')
  tf.flags.DEFINE_string('input', src, 'input image path (.jpg)')
  tf.flags.DEFINE_string('output', dst, 'output image path (.jpg)')
  tf.flags.DEFINE_integer('image_size', '256', 'image size, default: 256')

  graph = tf.Graph()

  with graph.as_default():
    with tf.gfile.FastGFile(FLAGS.input, 'rb') as f:
      image_data = f.read()
      input_image = tf.image.decode_jpeg(image_data, channels=3)
      input_image = tf.image.resize_images(input_image, size=(FLAGS.image_size, FLAGS.image_size))
      input_image = utils.convert2float(input_image)
      input_image.set_shape([FLAGS.image_size, FLAGS.image_size, 3])

    with tf.gfile.FastGFile(FLAGS.model, 'rb') as model_file:
      graph_def = tf.GraphDef()
      graph_def.ParseFromString(model_file.read())
    [output_image] = tf.import_graph_def(graph_def,
                          input_map={'input_image': input_image},
                          return_elements=['output_image:0'],
                          name='output')

  with tf.Session(graph=graph) as sess:
    generated = output_image.eval()
    with open(FLAGS.output, 'wb') as f:
      f.write(generated)

'''
使用示范:
在E:/GAN/CycleGAN-TensorFlow/test/raw/有一张名为aaa.jpg的汽车线稿
输入以下命令, 即可在E:/GAN/CycleGAN-TensorFlow/test/sketch/ 下生成一张aaa.jpg的256*256线稿
然后在E:/GAN/CycleGAN-TensorFlow/test/render/ 下生成一张上色后的aaa.jpg图片
'''

if __name__ == '__main__':
  color('static/pic/preprocessed/20180420192559.jpg',
        'static/pic/result/20180420192559.jpg')
  color('static/pic/preprocessed/20180420192615.jpg',
        'static/pic/result/20180420192615.jpg')
  color('static/pic/preprocessed/20180420192630.jpg',
        'static/pic/result/20180420192630.jpg')
