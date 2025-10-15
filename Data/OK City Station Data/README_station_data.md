
# Station Data
Add description here:

## How to Obtain
The dataset used for Data/OK City Station Data/Raw Data can be (and was) obtained as follows:

1) Go to https://www.ncei.noaa.gov/access/search/data-search/global-hourly
2) Type Oklahoma City OK, US in the `Where` text box.
3) Click `Select Date Range` below `When`.
4) In the date boxes provided type 2000/01/01 in the first and type 2021/31/12 in the second.
5) Below the filter options, click `Select All`.
6) Click `Quick Add` and `Proceed to Cart`.
7) Enter Contact information and submit.

After completing these steps you will receive a download link for the csv files you have requested. After downloading the file(s) onto your device, in [split_data.py](<OK City Station Data/Raw Data/split_data.py>) paste the file address into the `filepath` variable. 

## Legal Matters
Fill out

## Contents

1. Cleaned Data
    * nothing so far
    
2. Raw Data
    * [split_data.py](<OK City Station Data/Raw Data/split_data.py>)
        * The data we acquired from the NOAA as desribed in the [How to Obtain](#how-to-obtain) subsection was too large, and was split into sub-csv's by using this python script.
        
    * [Station_72353013967_Part_1.csv](<Raw Data/Station_72353013967_Part_1.csv>)
    * [Station_72353013967_Part_2.csv](<Raw Data/Station_72353013967_Part_2.csv>)
    * [Station_72353013967_Part_3.csv](<Raw Data/Station_72353013967_Part_3.csv>)
    * [Station_72353013967_Part_4.csv](<Raw Data/Station_72353013967_Part_4.csv>)
    * [Station_72354013919_Part_1.csv](<Raw Data/Station_72354013919_Part_1.csv>)



    * [Station_72354013919_Part_2.csv](<Raw Data/Station_72354013919_Part_2.csv>)
    * [Station_72354013919_Part_3.csv](<Raw Data/Station_72354013919_Part_3.csv>)
    * [Station_72354013919_Part_4.csv](<Raw Data/Station_72354013919_Part_4.csv>)

    * [Station_72354099999.csv](<Raw Data/Station_72354099999.csv>)

    * [Station_72354403954_Part_1.csv](<Raw Data/Station_72354403954_Part_1.csv>)
    * [Station_72354403954_Part_2.csv](<Raw Data/Station_72354403954_Part_2.csv>)
    * [Station_72354403954_Part_3.csv](<Raw Data/Station_72354403954_Part_3.csv>)
    * [Station_72354403954_Part_4.csv](<Raw Data/Station_72354403954_Part_4.csv>)

    * [Station_72354499999.csv](<Raw Data/Station_72354499999.csv>)

    * [Station_72357003948_Part_1.csv](<Raw Data/Station_72357003948_Part_1.csv>)
    * [Station_72357003948_Part_2.csv](<Raw Data/Station_72357003948_Part_2.csv>)
    * [Station_72357003948_Part_3.csv](<Raw Data/Station_72357003948_Part_3.csv>)
    * [Station_72357003948_Part_4.csv](<Raw Data/Station_72357003948_Part_4.csv>)

    * [Station_72357099999.csv](<Raw Data/Station_72357099999.csv>)

    * [Station_99999903948.csv](<Raw Data/Station_99999903948.csv>)

    * [Station_99999903954.csv](<Raw Data/Station_99999903954.csv>)

3. Raw Data Observations
    * [Features_No_NAN_Counts_script.py](<Raw Data Observations/Features_No_NAN_Counts_script.py>)
        * This script creates [Features_No_NAN_Counts.csv](<Raw Data Observations/Features_No_NAN_Counts.csv>). Requires the csv files from the Raw Data Folder to run.
    * [Features_No_NAN_Counts.csv](<Raw Data Observations/Features_No_NAN_Counts.csv>)
        * This csv file holds the counts of the number of non-nan values for each feature for each station. Note: In the documentation (isd-format-document.pdf) sometimes a number stands in for a nan value. We will deal with that if we choose such a feature later on.


