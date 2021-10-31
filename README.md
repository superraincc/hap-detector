# hap-detector
## kalman filter description
### Step 1 - predict

<img src="https://latex.codecogs.com/svg.image?\tilde{X}_k=\phi_{k,k-1}\hat{X}_{k-1}" title="\tilde{X}_k=\phi_{k,k-1}\hat{X}_{k-1}" />

<img src="https://latex.codecogs.com/svg.image?P_{k|k-1}=\phi_{k,k-1}P_{k-1}\phi^T_{k,k-1}&plus;Q" title="P_{k|k-1}=\phi_{k,k-1}P_{k-1}\phi^T_{k,k-1}+Q" />

### Step 2 - correct
$K_k=P_{k|k-1}H^T_k[H_kP_{k|k-1}H^T_k+R_k]^{-1}$

$\hat{X_k}=\tilde{X}_k+K_k[Z_k-H_k\tilde{X}_k]$

$P_k=(I-K_kH_k)P_{k|k-1}$

<img src="https://latex.codecogs.com/svg.image?x_{a}" title="x_{a}" />