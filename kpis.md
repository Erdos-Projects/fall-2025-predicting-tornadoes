# Key Performance Indicators

**Primary Key Performance Indicator**
1. Average Precision (PR-AUC)

**Secondary Key Performance Indicators**
2. F2-Score
3. Recall
4. ROC-AUC
5. Precision

Here is a summary of our metrics:

* Recall with scikit-learn's `recall_score`
    * Given by $$R=\frac{T_p}{T_p+F_n},$$ where $T_p$ is the number of true positives and $F_n$ is the number of false negatives.
    * Helps detect False Negatives (especially important for tornadoes). A Recall score of 1 is ideal; 0 is the worst.
* Precision with scikit-learn's `precision_score`
    * Given by $$P=\frac{T_p}{T_p+F_p},$$ where $T_p$ is the number of true positives and $F_p$ is the number of false positives.
    * Helps detect False Positives. A Precision score of 1 is ideal; 0 is the worst. 
    * While false positives are less than ideal, we will put more weight on false negatives (recall score) since this our goal is predicting tornado occurrence.
* F2-score with scikit-learn's `fbeta_score`.
    *$$F2 =\frac{(1+2^2)(\mathrm{precision}\cdot \mathrm{recall})}{(2^2\mathrm{precision})+\mathrm{recall}}$$
    * Provides a single measure  both false positives and false negatives.
    * Useful for overall summary of detection performance.
* Average Precision with scikit-learn's `average_precision_score`
    * Threshold independent
    * Area under the Precision-Recall curve (PR-AUC) given by plotting precision versus recall at various thresholds.
    * A weighted mean of the precision across with weights being differences in recall values across successive threshold values.
    * Informative metric for unbalanced target columns such as ours.
* ROC-AUC with scikit-learn's `roc_auc_score`
    * Area under the Receiver Operating Characteristic curve (ROC-AUC)given by plotting true positive rates over false positive rates at various thresholds.
    * Gives a sense on if the model is learning how to differentiate between conditions leading to tornadic and non-tornadic events even if the `Average Precision` (see below) score is low. 
    * Threshold independent.
    * Can appear overly optimistic in cases of severe class imbalance (like ours). Hence, we treat it as a secondary indicator of whether the model is learning to rank conditions leading to tornadic events versus non-tornadic events.

### Project Results and Interpretations


| Split | AP | F2 | Recall | Precision | ROC-AUC |
|-------|----|----|--------|-----------|---------|
| **Validation** (2018-2019) |0.07979 |0.091408 | 8.5% |12.6% | .904	 |
| **Test** (2020-2021) | 0.006182	 | 0% | 0%| 0.024558% | 0.918553 |

**Key Finding:** Severe temporal degradation (12.9x AP drop) demonstrates the challenge of distribution shift in meteorological prediction. The 0% recall and 0% precision represents a complete inversion of signal demonstrating that patterns learned from historical data (2000-2019) not only failed to generalize to the model but actively misled the model in testing. 


### Lessons Learned

1) **Temporal distribution shifts**: Atmospheric patterns shifted between training (2000-2019) and test (2020-2021) periods.
2) **Extreme class imbalance**: 0.15% tornado rate amplifies impact of distribution shifts
3) **Reliance on Seasonality and Time of Day**: Our model rely too heavily on what month it is and time of day. The test set had   more tornadoes in October than in May; moreover, there were 6 tornadoes in both January months for our test sets-- double the total January tornadoes for our training set.
4) **Limited feature set**: Surface weather observations alone provide insufficient signal. Future project may want to utilize radar data too. 




