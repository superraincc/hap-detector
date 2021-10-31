import numpy as np

class KalmanFilter(object):

    def __init__(self, initMeasurement=np.array([[0], [0]]), 
        stateVariance=1, measurementVariance=1):

        # 采样间隔时间
        self.dt = 0.04

        # F:状态转移矩阵
        self.F = np.array(
            [[1, self.dt, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, self.dt],
            [0, 0, 0, 1]])
        		
        # H:测量矩阵
        self.H = np.array(
            [[1, 0, 0, 0], 
            [0, 0, 1, 0]])

        # 过程噪声协方差矩阵
        self.Q = np.array(stateVariance * np.identity(self.F.shape[0]))
        # 测量噪声协方差矩阵
        self.R = np.array(measurementVariance * np.identity(self.H.shape[0]))
        # 最小均方误差
        self.P = self.Q

        # 用初始测量更新状态向量的初值
        self.state = np.array([[initMeasurement[0, 0]], [1],
            [initMeasurement[1, 0]], [1]])
        

    def predict(self):
        # 预测k时刻状态
        self.predictedState = np.dot(self.F, self.state)

        # 更新最小均方误差
        self.P = np.dot(self.F, np.dot(self.P, self.F.T)) + self.Q

        return np.array([[self.predictedState[0, 0]], [self.predictedState[2, 0]]])


    def correct(self, currentMeasurement):
        # 计算卡尔曼增益
        self.K = np.linalg.inv(np.dot(self.H, np.dot(self.P, self.H.T)) + self.R)
        self.K = np.dot(self.P, np.dot(self.H.T, self.K))

        # 根据测量值修正预测结果
        self.state = self.predictedState + \
            np.dot(self.K, (currentMeasurement - np.dot(self.H, self.predictedState)))

        # 更新测量最小协方差
        self.P = np.dot((np.identity(self.P.shape[0]) - np.dot(self.K, self.H)), self.P)

