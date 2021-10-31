# hap-detector
## 卡尔曼滤波算法介绍
### 基本假设
模型假设运动速度恒定，传感器仅能测量目标位置（position-only-measured, POM）
#### 状态转移方程

$X_k=\phi_{k,k-1}X_{k-1}$

其中
$X_i=\begin{bmatrix} x_k\\v_x\\y_k\\v_y \end{bmatrix}$
是系统当前状态的向量，
$\phi_{k,k-1}=\begin{bmatrix} 1&dt&0&0 \\ 0&1&0&0 \\ 0&0&1&dt \\ 0&0&0&1 \end{bmatrix}$
是状态转移矩阵.

#### 测量方程
$z_k=Hx_k$

其中
$H=\begin{bmatrix} 1&0&0&0 \\ 0&0&1&0 \end{bmatrix}$
是测量矩阵.

### 卡尔曼滤波器的状态更新遵从以下步骤

#### 步骤1 - 预测
$\tilde{X}_k=\phi_{k,k-1}\hat{X}_{k-1}$

$P_{k|k-1}=\phi_{k,k-1}P_{k-1}\phi^T_{k,k-1}$

#### 步骤2 - 修正
$K_k=P_{k|k-1}H^T_k[H_kP_{k|k-1}H^T_k+R_k]^{-1}$

$\hat{X_k}=\tilde{X}_k+K_k[Z_k-H_k\tilde{X}_k]$

$P_k=(I-K_kH_k)P_{k|k-1}$
