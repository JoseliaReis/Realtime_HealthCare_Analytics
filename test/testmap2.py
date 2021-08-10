import dash
import dash_table
import pandas as pd



df = pd.read_csv("../data/healthcare_data.csv")

app = dash.Dash(__name__)


from utils import functions as util


util.create_data_table(df)

app.layout = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in alert_frame.columns],
    data=alert_frame.to_dict('records'),
)


if __name__ == '__main__':
    app.run_server(debug=True)
