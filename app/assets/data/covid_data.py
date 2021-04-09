import pandas as pd


COVID_DATA_DF = pd.read_csv("https://raw.githubusercontent.com/hadrienj/essential_math_for_data_science/master/data/covid19.csv")
COVID_DATA_DF['days'] = COVID_DATA_DF["Date"].str.split("/").apply(lambda x: x[2]).astype(int)

