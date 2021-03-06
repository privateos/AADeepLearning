# pip install AADeepLearning
from aa_deep_learning.AADeepLearning import AADeepLearning
from aa_deep_learning.AADeepLearning.datasets import mnist
from aa_deep_learning.AADeepLearning.datasets import np_utils
import numpy as np
np.random.seed(0)

# mnist数据集已经被划分成了60,000个训练集，10,000个测试集的形式，如果数据不存在则自动下载
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 第一个维度是样本数目，第二维度是通道数表示颜色通道数，第三维度是高，第四个维度是宽
x_train = x_train.reshape(x_train.shape[0], 1, 28, 28)
x_test = x_test.reshape(x_test.shape[0], 1, 28, 28)

# 将x_train, x_test的数据格式转为float32
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')

# 归一化，将值映射到 0到1区间
x_train /= 255
x_test /= 255

# 因为是10分类，所以将类别向量(从0到10的整数向量)映射为二值类别矩阵，相当于将向量用one-hot重新编码
y_train = np_utils.to_categorical(y_train, 10)
y_test = np_utils.to_categorical(y_test, 10)

# 网络配置文件
config = {
    # 初始学习率
    "learning_rate": 0.001,
    # 优化策略: sgd/momentum/rmsprop/adam
    "optimizer": "adam",
    # 使用动量的梯度下降算法做优化,可以设置这一项，默认值为 0.9 ，一般不需要调整
    "momentum_coefficient": 0.9,
    # 训练多少次
    "number_iteration": 500,
    # 每次用多少个样本训练
    "batch_size": 64,
    # 迭代多少次打印一次信息
    "display": 10,

}

# 网络结构，数据将从上往下传播
net = [
    {
        # 层名
        "name": "convolutional_1",
        # 层类型，卷积层
        "type": "convolutional",
        # 卷积核个数
        "kernel_number": 1,
        # 卷积核高
        "kernel_height": 2,
        # 卷积核宽
        "kernel_width": 2,
        # 填充数，1：在图片最外层填充1圈0，2：填充2圈0，以此类推
        "padding": 1,
        # 滑动步长，1：水平或垂直方向滑动步长都为1，2：水平或垂直方向滑动步长都为2，以此类推
        "stride": 1,
        # 权重初始化  gaussian/xavier/msra
        "weight_init": "msra"
    },
    {
        # 层名
        "name": "relu_1",
        # 层类型， 激活函数层
        "type": "relu"
    },
    {
        # 层名
        "name": "pooling_1",
        # 层类型，池化层
        "type": "pooling",
        # 模式 max（最大池化）/average（平均池化）
        "mode": "max",
        # 池化核高
        "kernel_height": 2,
        # 池化核宽
        "kernel_width": 2,
        # 滑动步长，1：水平或垂直方向滑动步长都为1，2：水平或垂直方向滑动步长都为2，以此类推
        "stride": 1
    },
    {
        # 层名，无限制
        "name": "flatten_1",
        # 层类型，将数据展平为适合神经网络的结构，用于输入层或者卷积层和全连接层中间。 (60000, 1, 28, 28) ——> (784, 60000)
        "type": "flatten"
    },
    {
        # 层名
        "name": "fully_connected_1",
        # 层类型，全连接层
        "type": "fully_connected",
        # 神经元个数
        "neurons_number": 256,
        # 权重初始化方式  msra/xavier/gaussian
        "weight_init": "msra"
    },
    {
        # 层名
        "name": "relu_2",
        # 层类型（激活层） 可选，relu，sigmoid，tanh，
        "type": "relu"
    },
    {
        # 层名
        "name": "fully_connected_2",
        # 层类型，全连接层
        "type": "fully_connected",
        # 神经元个数， 因为是10分类，所以神经元个数为10
        "neurons_number": 10,
        # 权重初始化方式  msra/xavier/gaussian
        "weight_init": "msra"
    },
    {
        # 层名
        "name": "softmax_1",
        # 层类型，分类层，最终输出十分类的概率分布
        "type": "softmax"
    }
]

# 定义模型，传入网络结构和配置项
AA = AADeepLearning(net=net, config=config)
# 训练模型
AA.train(x_train=x_train, y_train=y_train)

# 使用测试集预测，返回概率分布和准确率， score:样本在各个分类上的概率， accuracy:准确率
score, accuracy = AA.predict(x_test=x_test, y_test=y_test)
print("test set accuracy:", accuracy)
