import pandas as pd
from utils import functions as utils
from utils import config as config
#df = pd.read_csv("./healthcare_data.csv", low_memory=False)
#df = df.iloc[:3000]
#df = df[df['alert'].notna()]
#df = df.sort_values('reading_id', ascending=False)

#df.to_csv("test_data2.csv")
#input_df_2 = pd.read_csv("../test_data/test_data2.csv")

#df = utils.create_alert_table(input_df_2)
#df.to_csv("result_data2.csv", index=False)
#patients, readings, alerts, emergencies, warnings = utils.get_total_counts(input_df_2)
#print (patients, readings, alerts, emergencies, warnings )



mock_ages_1 = config.mock_data["ages_low"]
print(mock_ages_1)