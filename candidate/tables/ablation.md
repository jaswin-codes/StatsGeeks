| method | origin | shots | mean | population_sd | episodes | configuration | protocol |
|---|---|---|---|---|---|---|---|
| A | factorial | 160 | 0.722195 | 0.0217145 | 5 | {"adaptive": false, "pool": false, "prior": 0.0, "spatial": false} | five development folds; 160 train/40 validation per class |
| A+B | factorial | 160 | 0.730752 | 0.0423746 | 5 | {"adaptive": false, "pool": true, "prior": 0.0, "spatial": false} | five development folds; 160 train/40 validation per class |
| A+B+C | factorial | 160 | 0.7455 | 0.0349133 | 5 | {"adaptive": false, "pool": true, "prior": 0.0, "spatial": true} | five development folds; 160 train/40 validation per class |
| A+B+C+D | factorial | 160 | 0.760888 | 0.0266599 | 5 | {"adaptive": true, "pool": true, "prior": 0.0, "spatial": true} | five development folds; 160 train/40 validation per class |
| A+B+D | factorial | 160 | 0.731972 | 0.0375896 | 5 | {"adaptive": true, "pool": true, "prior": 0.0, "spatial": false} | five development folds; 160 train/40 validation per class |
| A+C | factorial | 160 | 0.73843 | 0.0182849 | 5 | {"adaptive": false, "pool": false, "prior": 0.0, "spatial": true} | five development folds; 160 train/40 validation per class |
| A+C+D | factorial | 160 | 0.755892 | 0.026483 | 5 | {"adaptive": true, "pool": false, "prior": 0.0, "spatial": true} | five development folds; 160 train/40 validation per class |
| A+D | factorial | 160 | 0.726862 | 0.0230834 | 5 | {"adaptive": true, "pool": false, "prior": 0.0, "spatial": false} | five development folds; 160 train/40 validation per class |
| ASTRA_AGF | factorial | 160 | 0.766282 | 0.0250711 | 5 | {} | five development folds; 160 train/40 validation per class |
| EXPF | factorial | 160 | 0.684321 | 0.0256143 | 5 | {} | five development folds; 160 train/40 validation per class |
| No_source_prior | mechanism | 160 | 0.760888 | 0.0266599 | 5 | {"prior": 0.0} | five development folds; 160 train/40 validation per class |
| Coordinate_RF | mechanism | 160 | 0.769798 | 0.0163559 | 5 | {"coord": true} | five development folds; 160 train/40 validation per class |
