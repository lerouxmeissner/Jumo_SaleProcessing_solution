import matplotlib.pyplot as plt
import pandas as pd
import os
import zipfile
import time


def get_regions():
    try:
        # read csv and convert to dataframe(using utf-8 encoding). set Region as the index.
        regions_df = pd.read_csv('SalesProcessing/Data/Region/region_2016.csv', index_col="Region", encoding="utf-8")
        # remove regions that has end date (meaning it is inactive/replaced)
        regions_df = regions_df[pd.isnull(regions_df['EndDate'])]
        return regions_df
    except FileNotFoundError:
        print("SalesProcessing/Data/Region/ does not exist")
        return None


def get_sales():
    try:
        # get a list of all files in the 'Sales' directory
        sales_files = [file for file in os.listdir('SalesProcessing/Data/Sales')]
    except FileNotFoundError:
        print('SalesProcessing/Data/Sales does not exist')
        return None

    # create a new Sales dataframe
    sales_df = pd.DataFrame()

    # for each sales file in 'Sales' directory, create a dataframe and concatenate it to sales_df
    for sales_csv in sales_files:
        # convert sales csv to dataframe (using utf-8 encoding)
        new_sales = pd.read_csv('SalesProcessing/Data/Sales/' + sales_csv, encoding="utf-8")
        # concatenate current sales file to sales_df and reset indexes
        # (because each index starts at zero for new csv import)
        # 'Identifier' column is not unique
        sales_df = pd.concat([sales_df, new_sales]).reset_index(drop=True)
    return sales_df


def enrich_region_data(sales_df, regions_df):
    # add region description column by looking up the 'Region' value from sales_df in region
    sales_df['Region Description'] = regions_df.loc[sales_df['Region']]['RegionDescription'].values


def generate_output(region_column):
    # get string format of time for archive name
    date_string = time.strftime("%Y%m%d")+"_"
    output_path = 'SalesProcessing/Data/Output/'
    exists = os.path.isfile(output_path + date_string + 'all_sales_data.csv')
    # export sales data to csv in 'Output' directory
    if exists:
        # Store configuration file values
        sales.to_csv(output_path + date_string + 'all_sales_data.csv', mode='a', encoding='utf-8', index=False,
                     header=False)
    else:
        # Keep presets
        sales.to_csv(output_path + date_string + 'all_sales_data.csv', encoding='utf-8', index=False, header=True)

    sales_all = pd.read_csv(output_path + date_string + 'all_sales_data.csv', encoding="utf-8")

    # group sales by 'Network'
    sales_per_network_report = sales_all.groupby(['Network'])['Amount'].sum()
    # export Network sales data to csv in 'Output' directory
    sales_per_network_report.to_csv(output_path + date_string + 'sales_per_network_report.csv', header=True)
    # generate bar graph
    generate_graph(sales_per_network_report, date_string+'sales_per_network_report')

    # group sales by 'Region'
    sales_per_region_report = sales_all.reset_index().groupby([region_column])['Amount'].sum()
    # export Region sales data to csv in 'Output' directory
    sales_per_region_report.to_csv(output_path + date_string + 'sales_per_region_report.csv', header=True)
    # generate bar graph
    generate_graph(sales_per_region_report, date_string+'sales_per_region_report')

    # group sales by 'Network' and 'Region'
    sales_per_network_and_region_report = sales_all.reset_index().groupby(['Network', region_column])['Amount'].sum()
    # generate bar graph
    generate_graph(sales_per_network_and_region_report, date_string+'sales_per_network_and_region_report')


def generate_graph(df, name):
    # plot df to matplotlib graph
    df.plot(kind='bar', x='identifier', y='Amount')
    # add space around the graph to allow labels to fit into img that will be exported
    plt.tight_layout()
    # export graph to .png image file in 'Output' directory
    plt.savefig('SalesProcessing/Data/Output/' + name + '.png')
    # clear graph and data to allow for next graph
    plt.clf()
    print("")
    print("=======" + name + "=======")
    print(df)


def archive():
    # get string format of time for archive name
    filename = time.strftime("%Y%m%d-%H%M%S")
    # change directory to create zip file in 'Archive' directory
    os.chdir('SalesProcessing/Data/Archive')
    # create zip file
    zipper = zipfile.ZipFile(filename + '.zip', 'w', zipfile.ZIP_DEFLATED)

    for root, dirs, files in os.walk('../Sales'):
        for file in files:
            file_path = os.path.join(root, file)
            # write file from 'Output' directory
            zipper.write(file_path)

    zipper.close()
    # cd back to project root directory
    os.chdir("../../../")


if __name__ == '__main__':
    regions = get_regions()
    sales = get_sales()

    if sales is None or sales.empty:
        print("no sales data available in 'Sales' directory.")
    else:
        if regions is None or regions.empty:
            print("no region data available in 'Region' directory.")
            region_field = 'Region'
        else:
            enrich_region_data(sales, regions)
            region_field = 'Region Description'
        generate_output(region_field)
        archive()

    # exit()
