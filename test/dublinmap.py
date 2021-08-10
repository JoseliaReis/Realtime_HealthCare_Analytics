import pandas as pd 
import plotly.express as px

px.set_mapbox_access_token("pk.eyJ1IjoiYnJpYW5ob3VyaWdhbiIsImEiOiJja3JtN2VhOTUxbm5wMnBvNWVia2tncW92In0.tRvm3Wd57OOxTYGaDydSTw")
df = pd.read_csv("../data/healthcare_data.csv", low_memory=False)

def generate_dublin_map(df):
    figure = px.scatter_mapbox(df, lat="latitude", lon="longitude", color="name", hover_name="name",
                            hover_data=['timestamp', 'heart_rate','blood_pressure_top','blood_pressure_bottom',
                                        'body_temperature','blood_sugar_level'],
                            size_max=15, zoom=12)
    return figure


fig = generate_dublin_map(df)

fig.show()
