import welly
import pandas as pd
import plotly.express as px

def load_welly(path):

    wells = welly.read_las(f"{path}/*.las")
    wells_df = wells.df().reset_index(drop=False)
    return wells, wells_df

def dict_wells(wells):
    well_dict = {}
    for well in wells:
        well_dict[well.uwi] = {'well name':well.name, 
                            'Lat':well.location.latitude,
                            'Long':well.location.longitude}

    wells_df = pd.DataFrame.from_dict(well_dict, orient='index')
    wells_df.reset_index(inplace=True)
    wells_df.rename(columns={'index':'UWI'}, inplace=True)
    return wells_df

def map_wells(wells_df):
    fig = px.scatter_mapbox(wells_df, lat='Lat', lon='Long',zoom=7,  hover_name='well name')
    fig.update_layout(mapbox_style='open-street-map')
    return fig
