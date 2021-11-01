# hap-detector
## 卡尔曼滤波算法介绍
### 基本假设
模型假设运动速度恒定，传感器仅能测量目标位置（position-only-measured, POM）
#### 状态转移方程

<img src="https://latex.codecogs.com/svg.image?X_k=\phi_{k,k-1}X_{k-1}" title="X_k=\phi_{k,k-1}X_{k-1}" />

其中
<img src="https://latex.codecogs.com/svg.image?X_i=\begin{bmatrix}&space;x_k\\v_x\\y_k\\v_y&space;\end{bmatrix}" title="X_i=\begin{bmatrix} x_k\\v_x\\y_k\\v_y \end{bmatrix}" />
是系统当前状态的向量，
<img src="https://latex.codecogs.com/svg.image?\phi_{k,k-1}=\begin{bmatrix}&space;1&dt&0&0&space;\\&space;0&1&0&0&space;\\&space;0&0&1&dt&space;\\&space;0&0&0&1&space;\end{bmatrix}" title="\phi_{k,k-1}=\begin{bmatrix} 1&dt&0&0 \\ 0&1&0&0 \\ 0&0&1&dt \\ 0&0&0&1 \end{bmatrix}" />
是状态转移矩阵.

#### 测量方程
<img src="https://latex.codecogs.com/svg.image?z_k=Hx_k" title="z_k=Hx_k" />
其中

<img src="https://latex.codecogs.com/svg.image?H=\begin{bmatrix}&space;1&0&0&0&space;\\&space;0&0&1&0&space;\end{bmatrix}" title="H=\begin{bmatrix} 1&0&0&0 \\ 0&0&1&0 \end{bmatrix}" />
是测量矩阵.

### 卡尔曼滤波器的状态更新遵从以下步骤

#### 步骤1 - 预测
<img src="https://latex.codecogs.com/svg.image?\tilde{X}_k=\phi_{k,k-1}\hat{X}_{k-1}" title="\tilde{X}_k=\phi_{k,k-1}\hat{X}_{k-1}" />

<br/><img src="https://latex.codecogs.com/svg.image?P_{k|k-1}=\phi_{k,k-1}P_{k-1}\phi^T_{k,k-1}" title="P_{k|k-1}=\phi_{k,k-1}P_{k-1}\phi^T_{k,k-1}" />

#### 步骤2 - 修正
<img src="https://latex.codecogs.com/svg.image?K_k=P_{k|k-1}H^T_k[H_kP_{k|k-1}H^T_k&plus;R_k]^{-1}" title="K_k=P_{k|k-1}H^T_k[H_kP_{k|k-1}H^T_k+R_k]^{-1}" />

<br/><img src="https://latex.codecogs.com/svg.image?\hat{X_k}=\tilde{X}_k&plus;K_k[Z_k-H_k\tilde{X}_k]" title="\hat{X_k}=\tilde{X}_k+K_k[Z_k-H_k\tilde{X}_k]" />

<br/><img src="https://latex.codecogs.com/svg.image?P_k=(I-K_kH_k)P_{k|k-1}" title="P_k=(I-K_kH_k)P_{k|k-1}" />
