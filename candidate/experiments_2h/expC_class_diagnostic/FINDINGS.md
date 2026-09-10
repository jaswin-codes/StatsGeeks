# Class-level findings

Class order: 1,2,3,4. Repeated query pixels mean episodes are not independent samples.

## 5 shots
- Mean class F1: [0.661895, 0.474917, 0.509528, 0.563373]
- Class SD: [0.032462, 0.118206, 0.122255, 0.020733]
- Macro-variance fractions (including covariance): [0.1138, 0.4115, 0.4267, 0.048]
- Dominant bidirectional confusion by count: 1 <-> 2; normalized directed: 2 -> 1.
- Gain vs joint control: [0.042268, 0.009458, 0.069191, 0.027914]
- Gain vs compact local: [0.027528, 0.004139, 0.082072, 0.003296]
- Poor episodes: [4, 7]

## 25 shots
- Mean class F1: [0.656164, 0.581302, 0.632601, 0.578629]
- Class SD: [0.014792, 0.019781, 0.019269, 0.024135]
- Macro-variance fractions (including covariance): [0.1603, 0.196, 0.2603, 0.3834]
- Dominant bidirectional confusion by count: 1 <-> 2; normalized directed: 2 -> 1.
- Gain vs joint control: [0.003391, 0.002586, -0.000259, 0.007489]
- Gain vs compact local: [0.0, 0.0, 0.0, 0.0]
- Poor episodes: [7]

## 50 shots
- Mean class F1: [0.662962, 0.570325, 0.642119, 0.593686]
- Class SD: [0.014072, 0.026959, 0.011836, 0.013283]
- Macro-variance fractions (including covariance): [0.126, 0.5932, 0.1873, 0.0935]
- Dominant bidirectional confusion by count: 1 <-> 2; normalized directed: 2 -> 1.
- Gain vs joint control: [0.004989, 0.004204, 0.000441, 0.005458]
- Gain vs compact local: [0.0, 0.0, 0.0, 0.0]
- Poor episodes: [4, 8]

## 100 shots
- Mean class F1: [0.667905, 0.57253, 0.646231, 0.591386]
- Class SD: [0.010576, 0.016231, 0.00826, 0.008921]
- Macro-variance fractions (including covariance): [0.1827, 0.4658, 0.2481, 0.1033]
- Dominant bidirectional confusion by count: 1 <-> 2; normalized directed: 2 -> 1.
- Gain vs joint control: [0.005469, 0.00509, 0.002855, 0.006631]
- Gain vs compact local: [0.0, 0.0, 0.0, 0.0]
- Poor episodes: [8]

## 200 shots
- Mean class F1: [0.670229, 0.581466, 0.652849, 0.591386]
- Class SD: [0.006469, 0.009124, 0.007282, 0.00529]
- Macro-variance fractions (including covariance): [0.119, 0.3722, 0.2923, 0.2165]
- Dominant bidirectional confusion by count: 1 <-> 2; normalized directed: 2 -> 1.
- Gain vs joint control: [0.006236, 0.0056, 0.002756, 0.005566]
- Gain vs compact local: [0.0, 0.0, 0.0, 0.0]
- Poor episodes: [5, 7]

## Answers
Largest low-shot macro-variance contributor: class 3; weakest mean F1: class 2.
The variance decomposition allocates correlated class changes via cov(class F1, macro F1)/4; it is descriptive, not causal.
Largest contributor accounts for 42.7%, so do not attribute all 5-shot SD to one class.
Per-class wins/losses/ties and every episode gain are in diagnostic.json. Source geometry alone is isolated by compact_local; joint_control also includes dimension changes. No class-specific safeguard is justified by ten highly overlapping episodes. None implemented.
