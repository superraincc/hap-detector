import numpy as np

class KalmanFilter(object):

    def __init__(self, stateVariance=1, measurementVariance=1):

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
        self.Q = np.matrix(stateVariance * np.identity(self.F.shape[0]))
        # 测量噪声协方差矩阵
        self.R = np.matrix(measurementVariance * np.identity(self.H.shape[0]))
        # 最小均方误差
        self.P = self.Q

        # 状态向量
        self.state = np.matrix([[0],[1],[0],[1]])
        

    def predict(self):
        # 预测k时刻状态
        self.predictedState = self.F * self.state

        # 更新最小均方误差
        self.P = self.F * self.P * self.F.T + self.Q

        return self.predictedState


    def correct(self, currentMeasurement):
        # 计算卡尔曼增益
        self.K = self.P * self.H.T * (self.H * self.P * self.H.T + self.R)

        # 根据测量值修正预测结果
        self.state = self.predictedState + \
            self.K * (currentMeasurement - self.H * self.predictedState)

        # 更新测量最小协方差
        self.P = self.P - self.K * self.H * self.P

