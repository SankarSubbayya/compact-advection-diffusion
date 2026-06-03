# Paper results (auto-generated)

## 1. Modified-wavenumber resolving efficiency
(largest k·h, as fraction of π, where the modified wavenumber matches the true one within 1%)

| scheme | resolving k·h / π |
|---|---|
| central2 | 0.18 |
| central4 | 0.32 |
| central6 | 0.41 |
| compact4 | 0.43 |
| compact6 | 0.55 |

sample k'h vs kh:
| kh/π | central2 | central4 | compact4 | compact6 | exact |
|---|---|---|---|---|---|
| 0.25 | 0.71 | 0.78 | 0.78 | 0.79 | 0.79 |
| 0.50 | 1.00 | 1.33 | 1.50 | 1.56 | 1.57 |
| 0.75 | 0.71 | 1.11 | 1.64 | 1.98 | 2.36 |
| 0.90 | 0.31 | 0.51 | 0.88 | 1.22 | 2.83 |

## 2. Deformational benchmark — slotted cylinder (advection-dominated, t=T/2, N=129)
| scheme | rel L2 | min | max | IoU(>0.5) | mass |
|---|---|---|---|---|---|
| upwind-1 | 0.528 | +0.000 | 1.000 | 0.651 | 0.0850 |
| upwind-3 (OE-98) | 0.317 | -0.081 | 1.111 | 0.916 | 0.0900 |
| compact-4 (plain) | 0.336 | -0.562 | 1.450 | 0.929 | 0.0900 |
| BP-compact (ours) | 0.310 | -0.000 | 1.000 | 0.882 | 0.0899 |

(exact reference mass = 0.0881; IC max = 1.0)