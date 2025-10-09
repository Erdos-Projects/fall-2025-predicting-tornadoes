# scraping script used to download storm events data October 6th 2025
# Make sure bash is updated before running this script.

directory="your/path/here/Data/Storm Event Data/Raw Data" 

cd "${directory}"

baseurl="https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/" 

yearset1=({2000..2014} 2017 2018 2019 2021) 
# The years in yearset1 have ~c20250520.csv.gz at the end of their url.
# 2015,2016 have a ~c20250818.csv.gz and 2020 has a ~c20250702.csv.gz
# This is handled by the if-elif block below

for year in {2000..2021}; do
    if [[ " ${yearset1[@]} " =~ " ${year} " ]]; then
        file="StormEvents_details-ftp_v1.0_d${year}_c20250520.csv.gz"
    
    elif [[" 2015 2016 " =~ " ${year} " ]]; then
        file="StormEvents_details-ftp_v1.0_d${year}_c20250818.csv.gz"
    
    elif [[ "2020"  == "${year}" ]]; then
        file="StormEvents_details-ftp_v1.0_d${year}_c20250702.csv.gz"
    fi
    download="${baseurl}${file}" # URL of file to download
    newfile="${year}_storm_events.csv.gz" # New file name to be used
    echo "Downloading..."
    # Downloads file at 'download' replaced with newfile name
    wget -q -O "${newfile}" "${download}" 
    echo "Unzipping..."
    # unzips .gz file and replaces with .csv file with same name
    gunzip -d "${newfile}" 
    done
