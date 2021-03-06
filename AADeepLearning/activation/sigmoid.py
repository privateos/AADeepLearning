import numpy as np


class Sigmoid:
    """
    Sigmoid激活函数层
    """
    @staticmethod
    def init(layer, flow_data_shape, config):
        """
        初始化， 这里无操作
        :param layer: 层，包含该层的权重、偏置项、梯度、前向输入输出缓存、实例化对象等信息
        :param flow_data_shape: 流动数据的形状
        :param config:配置
        :return: 更新后的层， 流动数据的形状
        """
        return layer, flow_data_shape
    @staticmethod
    def forword(flow_data, layer, is_train):
        """
        前向传播
        :param flow_data: 流动数据
        :param layer: 层，包含该层的权重、偏置项、梯度、前向输入输出缓存、实例化对象等信息
        :param is_train: 是否是训练模式
        :return: 流动数据， 更新后的层
        """
        flow_data = 1 / (1 + np.exp(-flow_data))
        return flow_data, layer
    @staticmethod
    def backword(flow_data, layer, config):
        """
        反向传播
        :param flow_data: 流动数据
        :param layer: 层，包含该层的权重、偏置项、梯度、前向输入输出缓存、实例化对象等信息
        :param config:配置
        :return: 流动数据， 更新后的层
        """
        # dsigmoid/dz  = a*(1-a)
        flow_data = flow_data * (layer["output"]*(1-layer["output"]))
        return flow_data, layer

    @staticmethod
    def update_parameters(layer, config, iteration):
        """
        更新权重和偏置项， 这里无操作
        :param layer: 层，包含该层的权重、偏置项、梯度、前向输入输出缓存、实例化对象等信息
        :param config:配置
        :param iteration:迭代次数
        :return: 更新后的层
        """
        return layer
