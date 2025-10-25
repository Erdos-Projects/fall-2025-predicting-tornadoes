# EDA Checklist


## **1. Data Access and Setup**
- [x] Import cleaned data from the **processed** folder (not raw or interim).
- [x] Display a small sample (`df.head()`, `df.sample(5)`).
- [x] Note any missing or unexpected columns.

---

## **2. Data Overview**
- [x] Record `df.shape` (rows × columns).
- [x] Use `df.info()` to inspect dtypes and non-null counts.
- [x] Use `df.describe()` for numeric summaries.
- [ ] Identify potential key columns (e.g., date, station ID, latitude, longitude).
- [ ] Save these outputs as markdown cells or summary CSVs.

---

## **3. Data Quality and Cleaning Checks**
- [x] Count missing values (`df.isna().sum()`).
- [x] Identify columns with >50% missing data.
- [x] Detect duplicates (`df.duplicated().sum()`).
- [x] Check for placeholder codes (e.g., 9999, -9999). See ISD documentation.
- [x] Validate date formats and ranges.
- [ ] Spot out-of-range values (negative speeds, lat/lon outside expected bounds). 

---

## **4. Type Validation**
- [x] Confirm numeric-like strings were converted properly.
- [ ] Verify categorical columns (e.g., station name, source) remain strings.
- [x] Ensure dates are `datetime64[ns]` objects.
- [x] Check for mixed-type columns using `df[col].apply(type).value_counts()`.

---

## **5. Statistical Exploration**
- [] Summarize distributions (mean, std, min, max) for key features.
- [ ] Plot histograms or KDEs for numeric variables.
- [ ] Identify skewed or heavy-tailed variables.
- [ ] Look for normalization/scaling needs.
- [ ] Compute correlations between weather features (temperature, pressure, wind, humidity).

---

## **6. Spatial Analysis **
- [ ] Plot station coordinates on a map to confirm coverage.
- [ ] Check for duplicated or overlapping coordinates.
- [ ] Compare tornado event coordinates with station locations.

---

## **7. Temporal Patterns**
- [ ] Convert date/time fields to datetime and extract `year`, `month`, `hour`.
- [ ] Plot tornado occurrences by month/year.
- [ ] Examine diurnal (hourly) and seasonal patterns.
- [ ] Check for missing or uneven temporal sampling.

---

## **8. Feature Relationships**
- [ ] Create scatterplots for related variables (e.g., humidity vs. temperature).
- [ ] Make boxplots for distributions by time or category.
- [ ] Compute and plot a correlation heatmap.
- [ ] Identify redundant or highly correlated variables.

---

## **9. Documentation & Team Notes**
- [ ] Record findings in your EDA notebook (`EDA_Draft_[Name].ipynb`).
- [ ] Add markdown notes for:
  - Columns to drop or transform later.
  - Observed anomalies.
  - Promising or unstable features.
- [ ] End with a short markdown summary:
  - **Top 3 data quality issues**.
  - **Top 3 potentially predictive features**.
  - **Next steps or questions for the team.**

---

## **10. Optional Deliverables**
- [ ] Save plots to `results/eda_plots/`.
- [ ] Export summary tables (e.g., missingness, correlation matrix).
- [ ] Write a concise EDA summary in markdown for the final report.

---

## ** Best Practices**
- Always analyze **copies** of data, not master files.
- Commit **notebooks and results**, not large CSVs.
- Use clear markdown headers for sections (`### Section Name`).
- Label plot axes and include descriptive titles.
- Note every transformation you perform.
- Avoid overwriting processed data; always write new versions.

---

**Shared Deliverable:** Each member completes their own `EDA_Draft_[Name].ipynb`, then the team consolidates findings into a master EDA summary notebook before modeling.