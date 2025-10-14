The dataset used for Data/OK City Station Data/Raw Data can be (and was) obtained as follows:

1) Go to https://www.ncei.noaa.gov/access/search/data-search/global-hourly
2) Type Oklahoma City OK, US in the `Where` text box.
3) Click `Select Date Range` below `When`.
4) In the date boxes provided type 2000/01/01 in the first and type 2021/31/12 in the second.
5) Below the filter options, click `Select All`.
6) Click `Quick Add` and `Proceed to Cart`.
7) Enter Contact information and submit.

After completing these steps you will receive a download link for the csv files you have requested. After downloading the file(s) onto your device, in [split_data.py](<OK City Station Data/Raw Data/split_data.py>) paste the file address into the `filepath` variable. 

KA1 = Max Temp stuff
KA2 = Min Temp stuff
