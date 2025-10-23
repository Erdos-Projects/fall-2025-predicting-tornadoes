# Processed Data Feature Assumptions

## Domain Irrelevant or Redundant Columns
The following list consists of features from the raw station datasets in `Data/station/raw` that we choose to delete in the final merged dataset used for EDA and modeling. Reasons for their deletion vary: they either have little to no pertinence in the formation of tornadoes, or the time scales in which they are measured are too long to be informative. 

```python
columns_to_drop = [ 
                    'NAME',
                    'SOURCE',
                    'REPORT_TYPE',
                    'CALL_SIGN',
                    'QUALITY_CONTROL',
                    'CALL_SIGN.1',
                    'QUALITY_CONTROL.1',
                    'REPORT_TYPE.1',
                    'SOURCE.1',
                    'AB1',
                    'AD1',
                    'AE1',
                    'AG1',
                    'AH1',
                    'AH2',
                    'AH3',
                    'AH4',
                    'AH5',
                    'AH6',
                    'AI1',
                    'AI2',
                    'AI3',
                    'AI4',
                    'AI5',
                    'AI6',
                    'AK1',
                    'AM1',
                    'AN1',
                    'AT1',
                    'AT2',
                    'AT3',
                    'AT4',
                    'AT5',
                    'AT6',
                    'AT7',
                    'AT8',
                    'AU1',
                    'AU2',
                    'AU3',
                    'AU4',
                    'AU5',
                    'AW1',
                    'AW2',
                    'AW3',
                    'AW4',
                    'AW5',
                    'AW6',
                    'AW7',
                    'AX1',
                    'AX2',
                    'AX3',
                    'AX4',
                    'AX5',
                    'AX6',
                    'ED1',
                    'EQD',
                    'GD1',
                    'GD2',
                    'GD3',
                    'GD4',
                    'GE1',
                    'GF1',
                    'IA1',
                    'KC1',
                    'KC2',
                    'KD1',
                    'KD2',
                    'KE1',
                    'MH1',
                    'MK1',
                    'MV1',
                    'MW1',
                    'MW2',
                    'MW3',
                    'MW4',
                    'MW5',
                    'OD1',
                    'OE1',
                    'OE2',
                    'OE3',
                    'REM',
                    'SA1',
                    'UA1',
                    'UG1',
                    'WA1'
                    ]
```
## High NaN Frequency Columns
In addition to the columns in columns_to_drop, we will drop the following columns since 50% of their values are NaN in the merged dataset. Of course NaN values in general are not necessarily meaningless, but as we are using data from different stations, we a large NaN frequency is indicative of some but not all capturing a particular type of data. So, we choose to perform this deletion of columns to be consistent across stations.

```python
80_NaN_cols =   [
                    'AA1',
                    'AA2',
                    'AA3',
                    'AA4',
                    'AJ1',
                    'AL1',
                    'GA2',
                    'GA3',
                    'GA4',
                    'GA5',
                    'GA6',
                    'GJ1',
                    'GK1',
                    'GP1',
                    'GQ1',
                    'GR1',
                    'HL1',
                    'KA1',
                    'KA2',
                    'KA3',
                    'KA4',
                    'KB1',
                    'KB2',
                    'KB3',
                    'KG1',
                    'KG2',
                    'MD1',
                    'MF1',
                    'MG1',
                    'OC1',
                    'RH1',
                    'RH2',
                    'RH3'
            ]
```
### Code Snippet

```python

## Imports 

import pandas as pd
import numpy as np
import os
import math
from src.cleaning.merged_tornado_indicator import create_tornado_indicator


data = create_tornado_indicator(drop_cols=columns_to_drop,split_tuples=False, mapping=None,time_window=1,val_radius=50)

80_NaN_cols =[]
# frequency of missing values 
na_freq = (data.isna().sum())/len(data)
for idx in na_freq.index:
    if na_freq[idx]>=.5:
        80_NaN_cols.append(idx)

print(80_NaN_cols)
```

**Note:** In the output of the above code, you will find additional columns each with a 'TORNADO' appearing somewhere in each. We DO NOT delete these, as these are useful for predicting the occurrence of a tornado.