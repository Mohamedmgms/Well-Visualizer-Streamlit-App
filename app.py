import streamlit as st
import pandas as pd
from plotting_functions import load, plot_ex_11, plot_exe_12, plot_exe_13, plot_exe_21, plot_exe_22, plot_exe_23
import os
import streamlit as st
# from pages_functions import get_curves_data
from pages import scatter, plot, home, data_summary, welly_page, get_arps_data, arps_plot, prediction, arps
# from get_cols import curves_list

def get_curve_cols(file, ext):
    if file == "15-9-19_SR_COMP.LAS":
        curves_list = df.columns
        index = 'DEPT'
        pages_list = ["Home", "Data Summary", "Scatter Plot", "Line Plot", "Exercises"]

    elif file == '15_9-19A-CORE.csv':
        curves_list = ['DEPTH', 'CKHG', 'CPOR', 'CGD']
        index = 'DEPTH'
        pages_list = ["Home", "Data Summary", "Scatter Plot", "Line Plot", "Exercises"]

    elif file == 'L05-15-Spliced.las':
        curves_list = ['DEPT', 'BHT',"WTBH", 'CAL', 'CHT', "TEN", "TTEN", "CNQH", "GR", "MBVI", "MBVM", "MCBW", "MPHE", "MPHS", "MPRM", "PEQH", "PORZC", "ZDNCQH"]
        index = 'DEPT'
        pages_list = ["Home", "Data Summary", "Scatter Plot", "Line Plot", "Exercises"]
    elif file == 'L05-15-Survey.csv':
        curves_list = ['MD', 'INC',"AZI", 'TVD', 'x-offset', "y-offset"]
        index = 'MD'
        pages_list = ["Home", "Data Summary", "Scatter Plot", "Line Plot", "Exercises"]
    elif file == "Volve production data.xlsx":
        curves_list = None
        index = None
        pages_list = ["Home", "Data Summary", "ARPS' Model", "Prediction"]
    elif ext == ".xlsx":
        curves_list = None
        index = None
        pages_list = ["Home", "Data Summary", "ARPS' Model", "Prediction"]  
    elif ext == ".csv":
        curves_list = None
        index = None
        pages_list = ["Home", "Data Summary", "Scatter Plot", "Line Plot", "Exercises"]
    elif ext == ".las":
        curves_list = None
        index = None
        pages_list = ["Home", "Data Summary", "Scatter Plot", "Line Plot", "Exercises"]
    else:
        curves_list = None
        index = None
        pages_list = ["Home", "Data Summary", "Scatter Plot", "Line Plot", "Exercises"]
   
    return curves_list, index, pages_list


pd.set_option('display.max_columns', None)
st.set_page_config(layout="wide",
                    initial_sidebar_state="auto",
                      page_title="Well Visualizer")


st.title('Well Data Visualizer')
st.text('This is a web app to allow visualization of wells data')

st.sidebar.title("Sidebar")
st.sidebar.header('Files')

upload_file = None

state = st.sidebar.selectbox("Select what you want", options=["Well Logs", "Multiple Wells", "ARPS' Model"])
if state == "Multiple Wells":
    welly_page()
elif state == "Well Logs":
    upload_file = st.sidebar.file_uploader('Upload a file containing well data', type=["csv", "las"])
    if upload_file is not None:
        ext = os.path.splitext(upload_file.name)[-1].lower()
        df, las= load(upload_file.name, ext)
elif state == "ARPS' Model":
    upload_file = st.sidebar.file_uploader('Upload a file containing well production data', type=["xlsx"])


    if upload_file is not None:
        ext = os.path.splitext(upload_file.name)[-1].lower()
        df, las= load(upload_file.name, '.xlsx')
        



if upload_file is not None:
    curves_list, index, pages_list = get_curve_cols(upload_file.name, ext)
    st.sidebar.header('Navigation')
    options = st.sidebar.radio('Select what you want to display:', pages_list)


    if options == 'Home':
        home()
    elif options == 'Data Summary':
        data_summary(df, curves_list, index)
    elif options == "Scatter Plot":
        scatter(df)
    elif options == "Line Plot":
        plot(df)
    elif options == "Exercises":
        if upload_file.name == "15-9-19_SR_COMP.LAS":
            plot_ex_11(df)
            plot_exe_12(df, ["GR", "RMED", "DEN", "NEU", "RDEP"], "DEPT")
        elif upload_file.name == '15_9-19A-CORE.csv':
            plot_exe_13(df)
        elif upload_file.name == 'L05-15-Spliced.las':
            plot_exe_21(df, las)
        elif upload_file.name == "L05-15-Survey.csv":
            plot_exe_22(df)
            plot_exe_23(las)
    elif options == "ARPS' Model":
        names_list = get_arps_data(df)
        arps_plot(df, names_list)
    elif options == "Prediction":
        names_list = get_arps_data(df)
        if names_list is not None:
            best, arps_param, clean_df, x_axis = arps(df, names_list)
            prediction(best, arps_param, clean_df, names_list, x_axis)
        else:
            st.write("Please make all selections to proceed.")    
else:
    st.write("")

