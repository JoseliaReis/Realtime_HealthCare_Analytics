import dash
import dash_table
import pandas as pd



df = pd.read_csv("../data/healthcare_data.csv")
app = dash.Dash(__name__)


def emergency_alerts(df):
    """
    function to create a dataframe for emergency alerts. Contains
        - list of conditions (like the if statement)
        - list of alerts (Emergency & Warning)
        - list of messages (contains information)
    Where every conditions is met (np.select) we add the timestamp, location, alert and message
    :param df:
    :return: Returns a new dataframe with the emergency information
    """
    #alert_frame = df[pd.notnull(df['alert'])]
    df = df[df['alert'].notna()]
    # keep only the columns we need
    df = df[['name', 'phone', 'alert', 'latitude', 'longitude', 'timestamp']]
    df = df.sort_values('timestamp',ascending=False)
    return df


alert_frame = emergency_alerts(df)

app.layout = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in alert_frame.columns],
    data=alert_frame.to_dict('records'),
)


if __name__ == '__main__':
    app.run_server(debug=True)