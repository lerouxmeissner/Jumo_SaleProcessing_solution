Jumo_SaleProcessing_solution:

<b>Prerequisites:</b>
    Python and pip is installed on environment
    internet connection is available (for installing required python dependencies)

Optional:
    Docker installed (can optionally create and run in container)
    
<b>Instructions:</b>
  Option 1: Run in on local machine with python virtual environment
    run: python3 -m venv venv
    run: source venv/bin/activate
    run: pip install -r requirements.txt
    run: python process_sales.py (if using conda, use pythonw instead of python/python3)

  Option 2: Run in docker container
    start docker
    run: cd <path to Jumo_Solution unarchived directory>
    run: docker build -t python-jumo . (this could take a few minutes. needs to download dependencies)

    Option 2A: run as interactive
        run: docker run -i -t python-jumo /bin/bash
        run: python process_sales.py
        run: cd SalesProcessing/Data/Output/
        run: cat <filename.csv> (all_sales_data.csv, sales_per_network_report.csv, sales_per_region_report.csv)

    Option 2B: run as an executable
        run: docker run -t python-jumo

  Matplotlib graphs are stored in the Output directory for easier analysis.
  
<b>Assumptions:</b>
    'Sales' directory will be cleared once data is processed. I purposely don't clear it in my solution because i need the data to demonstrate that the program keeps adding the new data to the output(because the data is streamed to the sales directory).
    If no new data is added to the 'Sales' directory, it will keep adding the same data to the output.
    The reports in the 'Output' directory is stored daily, and the file name contains the date. all data processed on the same day will be in the same output file.
    SalesProcessing.zip will be unarchived in the same directory as process_sales.py,so directory structure will be:
       |-SalesProcessing
         |-Data
           |-Archive
           |-Output
           |-Region
           |-Sales
         |-process_sales.png
       |-process_sales.py
       |-requirements.txt
       |-assumptions.txt
       |-prerequisites.txt
       |-instructions.txt

    Directory Structure will remain the same.
    Data will always be in csv format.
    More files can be added to 'Sales' directory.
    The name of the region_csv will remain constant.
    
<b>Scaling notes:<b>
    Many docker containers can be used to process data. The processing will then be distributed, but someone first has to assign which data gets processed inside which container. This can be automated if needed.
    At the moment, one container is sufficient.
    DataFrames (python pandas library) is not suggested for Big data, but we are working with less than 1000 records (15), so i believe it is a good fit for the current need.
    CSVs can be processed in chunks if CSV files contain to many records.
    Dataframes caters for any additional columns. So if new columns get added over time, the solution will not need to change.
