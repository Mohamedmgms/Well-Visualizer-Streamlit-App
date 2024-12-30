import streamlit as st
from plotting_functions import plotly_scatter, plotly_line
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from welly_functions import load_welly, dict_wells, map_wells
import arps_model
import numpy as np
import plotly.express as px
import pandas as pd
import arps_model
from datetime import timedelta

colors = ["red", "orange", "green", "cyan", "blue", "violet", "red", "brown", "blue", "black", "red", "orange", "green", "cyan", "blue", "violet", "red", "brown", "blue", "black"]


def home():
    st.header("Home Page")
    st.write("Welcome to the Well Data Visualizer!")

def data_summary(df, curves_list, ind):
    st.header('Statistics of Dataframe')
    st.write(df.describe())
    st.header('Header of Dataframe')
    st.write(df.head(10))
    if curves_list is not None:
        curves_list = list(curves_list)
        curves_list = curves_list[1:]
        fig = make_subplots(rows=1, cols=len(curves_list), shared_yaxes=True)
        plotly_line(fig, df, curves_list, ind, colors[0:len(curves_list)], False, False, False, True)

def scatter(df):    
    col1, col2, col3 = st.columns(3)
    x_axis_val = col3.multiselect('Select Curves To Plot', df.columns, key=f"x_axis")
    y_axis_val = col3.selectbox('Y-axis', options=df.columns, key=f"y_axis")
    add_color = col3.checkbox("Add Color", value=False) 
    if add_color:
        selected_color = col3.selectbox('Color by', options=df.columns, key=f"color_scatter")
    else:
        selected_color = None
    col1.header('X-Axis')
    x_log = col1.radio('Linear or Logarithmic', ('X-Linear', 'X-Logarithmic'))
    x_inverse= col1.radio('Reverse axis', (False, True), index=0)
    col2.header('Y-Axis')

    y_log = col2.radio('Linear or Logarithmic', ('Y-Linear', 'Y-Logarithmic'))
    y_inverse = col2.radio('Reverse Axis', (False, True), index=1)
    square = col1.checkbox("Square Plot", value=True)
    if x_log == "X-Linear":
        x_log = False
    else:
        x_log = True
    if y_log == "Y-Linear":
        y_log = False
    else:
        y_log = True
    if len(x_axis_val)>=1:
        fig = make_subplots(rows=1, cols=len(x_axis_val), shared_yaxes=True)
        plotly_scatter(fig, df, x_axis_val, y_axis_val, selected_color,add_color, x_log, y_log, x_inverse, y_inverse, square = square)

color_picker = ["red", "green", "blue", "yellow", "purple", "black", "orange"]

def plot(df):
    col1, col2, col3 = st.columns(3)
    x_axis_val = col3.multiselect('Select Curves To Plot', df.columns, key=f"x_axis")
    y_axis_val = col3.selectbox('Y-axis', options=df.columns, key=f"y_axis")
    selected_color = col3.multiselect('Pick a color', colors, default=["blue"], key=f"color_plot")

    col1.header('X-Axis')
    x_log = col1.radio('Linear or Logarithmic', ('X-Linear', 'X-Logarithmic'), index=0)
    x_inverse= col1.radio('Reverse axis', (False, True))
    col2.header('Y-Axis')

    y_log = col2.radio('Linear or Logarithmic', ('Y-Linear', 'Y-Logarithmic'))
    y_inverse = col2.radio('Reverse Axis', (False, True), index=1)
    square = col1.checkbox("Square Plot", value=False)
    if x_log == "X-Linear":
        x_log = False
    else:
        x_log = True
    if y_log == "Y-Linear":
        y_log = False
    else:
        y_log = True
    if len(x_axis_val)>=1:
        fig = make_subplots(rows=1, cols=len(x_axis_val), shared_yaxes=True)
        plotly_line(fig, df, x_axis_val, y_axis_val, selected_color, x_log, y_log, x_inverse, y_inverse, square = square)

def welly_page():
    st.title('Multiple wells Visualization')
    well_path = st.sidebar.text_input('Enter well data folder path', "welly_data")
    wells, wells_data_df = load_welly(well_path)
    wells_df = dict_wells(wells)
    

    if wells is not None:
        pages_list = ["Home", "Data Summary", "Scatter Plot", "Line Plot"]
        st.sidebar.header('Navigation')
        options = st.sidebar.radio('Select what you want to display:', pages_list)

        if options == 'Home':
            home()
            st.header('Wells data')
            st.write(wells_df)
            st.header('Wells map')
            st.plotly_chart(map_wells(wells_df), use_container_width=True)
            st.write(wells_data_df.head(10))
        elif options == 'Data Summary':
            well_name = st.selectbox("Select the well to plot", options=wells_df["UWI"])
            wells_data_df = wells_data_df[wells_data_df["UWI"] == well_name]
            data_summary(wells_data_df, ["DEPT", "GR", "DT", "RHOB", "DRHO", "NPHI"], "DEPT")
        elif options == "Scatter Plot":
            well_name = st.selectbox("Select the well to plot", options=wells_df["UWI"])
            wells_data_df = wells_data_df[wells_data_df["UWI"] == well_name]
            scatter(wells_data_df)
        elif options == "Line Plot":
            well_name = st.selectbox("Select the well to plot", options=wells_df["UWI"])
            wells_data_df = wells_data_df[wells_data_df["UWI"] == well_name]
            plot(wells_data_df)

def get_arps_data(df):
    col1, col2, col3, col4 = st.columns(4)
    none_option = "None"
    name_col = col1.selectbox("Well Names Column", options=[none_option] + df.columns.tolist(), key="well_col")
    
    if name_col != none_option:
        well_name_options = df[name_col].unique().tolist()
        well_name = col2.selectbox("Well Name", options=well_name_options, key="well_name")
    else:
        well_name = none_option
    date_col = col3.selectbox("Date Column", options=[none_option] + df.columns.tolist(), key="date")
    prod_col = col4.selectbox("Production Column", options=[none_option] + df.columns.tolist(), key="prod")
    
    if name_col == none_option or date_col == none_option or prod_col == none_option:
        return None
    else:
        return [name_col, well_name, date_col, prod_col]

def error(orig, fitted):
    n = len(orig)
    t1 = (orig-fitted)**2
    t2 = np.sum(t1)
    t3 = t2/n
    err = np.sqrt(t3)
    return err

def plot_models(Q, x, y = [], x_label = "", y_label = "Production Rate", title = "", label = ""):
    plt.figure(figsize=(12, 8))
    colors = ["blue", "orange", "green"]
    for i, axis in enumerate(y):
        plt.plot(x, axis,label = label[i],color = colors[i], linestyle = "--", linewidth=3, alpha = 0.9)
    plt.plot(x, Q, color = "red",label = "Smoothed Production Data", linestyle = "-", linewidth=2, alpha = 1)
    plt.xlabel(x_label, fontsize=14)
    plt.ylabel(y_label, fontsize=14)
    plt.title(title, fontsize=16)

    plt.grid(which = "major", color = "#6666", linestyle = "-", alpha = 0.5)
    plt.grid(which = "minor", color = "#9999", linestyle = "-", alpha = 0.1)
    plt.minorticks_on()
    plt.legend()
    st.pyplot(plt)

def arps_plot(df, names_list):
    st.header("Fit Production Rate to")
    x_axis = st.selectbox("X-Axis", options=["Days", "Cummulative Production"], key="x-axis")
    window = st.slider("Window Size", min_value=5, max_value=100, key="window")
    if names_list is not None:
        arpa_param, clean_df = arps_model.arps(df, window, x_axis, names_list)
        T = clean_df["days"]
        Q = clean_df["smooth_prod"]
        G = clean_df["smooth_cum_prod"]
        titles = ["Exponential Parameters", "Harmonic Parameters", "Hyperbolic Parameters"]
        models = ["Exponential", "Harmonic", "Hyperbolic"]

        if x_axis == "Days":
            x_label = "Time, days"
            x = T
        else:
            x_label = "Cummulative Production"
            x = G

        y_exp = clean_df["Exponential Fitted"]
        y_har = clean_df["Harmonic Fitted"]
        y_hyp = clean_df["Hyperbolic Fitted"]

        y = [y_exp, y_har, y_hyp]
        errors = []
        for i, fit in enumerate(y):
            errors.append(error(Q, fit))

        plot_models(Q, x, [clean_df[names_list[3]]], x_label, title="Smoothed Production graph", label=["Production Data"])
        plot_models(Q, x, y, x_label, title='Fitted Smooth Production', label=["Exponential Fitted", "Harmonic Fitted", "Hyperbolic Fitted"])

        columns = st.columns(3)
        for i, col in enumerate(columns):
            col.header(titles[i])
            col.write(f"initial flow rate (qi): {arpa_param[models[i]][0]}")
            col.write(f"initial decline rate (Di): {arpa_param[models[i]][1]}")
            col.write(f"Arps' Decline Curve Exponent (b): {arpa_param[models[i]][2]}")
            col.write(f"Root Mean Square Error: {errors[i]}")

        best_index = errors.index(min(errors))
        best_model = models[best_index]
        st.header(f"The Best Model is the {best_model} model!")
        return best_model, arpa_param, clean_df
    else:
        st.write("Please make all selections to proceed.")

def arps(df, names_list):
    st.header("Fit Production Rate to")
    x_axis = st.selectbox("X-Axis", options=["Days", "Cummulative Production"], key="x-axis")
    window = st.slider("Window Size", min_value=5, max_value=100, key="window")
    if names_list is not None:
        arpa_param, clean_df = arps_model.arps(df, window, x_axis, names_list)
        models = ["Exponential", "Harmonic", "Hyperbolic"]
        Q = clean_df["smooth_prod"]
        y_exp = clean_df["Exponential Fitted"]
        y_har = clean_df["Harmonic Fitted"]
        y_hyp = clean_df["Hyperbolic Fitted"]

        y = [y_exp, y_har, y_hyp]
        errors = []
        for fit in y:
            errors.append(error(Q, fit))

        best_model = models[errors.index(min(errors))]
        return best_model, arpa_param, clean_df, x_axis
    else:
        st.write("Please make all selections to proceed.")

def generate_time_list(start_date, end_date):
    delta =  int((end_date - start_date).days)
    time = list(range(1, delta + 1))
    time_df = np.array(time)
    return time_df

def predict_plot(df, best, x_axis):

    time_plot = px.line(df, x='Time', y='Q_fitted', title=(f"Rate plotted to Time. (Rate fitted over {x_axis} by {best} Model)"))
    cum_plot = px.line(df, x='G_fitted', y='Q_fitted', title=(f"Rate plotted to Cummulative. (Rate fitted over {x_axis} by {best} Model)"))
    
    st.plotly_chart(time_plot)
    st.plotly_chart(cum_plot)

def prediction(best, arps_param, clean_df, names_list, x_axis):
    st.header("Dates")
    col1, col2 = st.columns(2)
    start_date = col1.selectbox("From:", options=clean_df[names_list[2]], index=clean_df[names_list[2]].tolist().index(clean_df[names_list[2]].min()))
    end_date = col2.selectbox("To:", options=clean_df[names_list[2]], index=clean_df[names_list[2]].tolist().index(clean_df[names_list[2]].max()))


    clean_df = clean_df[(clean_df[names_list[2]]>=start_date) & (clean_df[names_list[2]]<=end_date)]

    T = clean_df["days"]
    Q = clean_df["smooth_prod"]
    G = clean_df["smooth_cum_prod"]
    titles = ["Exponential Parameters", "Harmonic Parameters", "Hyperbolic Parameters"]
    models = ["Exponential", "Harmonic", "Hyperbolic"]

    if x_axis == "Days":
        x_label = "Time, days"
        x = T
    else:
        x_label = "Cummulative Production"
        x = G

    y_exp = clean_df["Exponential Fitted"]
    y_har = clean_df["Harmonic Fitted"]
    y_hyp = clean_df["Hyperbolic Fitted"]

    y = [y_exp, y_har, y_hyp]

    plot_models(Q, x, [clean_df[names_list[3]]], x_label, title="Smoothed Production graph", label=["Production Data"])
    plot_models(Q, x, y, x_label, title='Fitted Smooth Production', label=["Exponential Fitted", "Harmonic Fitted", "Hyperbolic Fitted"])
    
    st.header("Predict until:")
    predict_end_date = st.date_input("End of prediction")
    start_date = pd.Timestamp(start_date)
    predict_end_date = pd.Timestamp(predict_end_date)
    Time = generate_time_list(start_date, predict_end_date)
    best_index = models.index(best)
    qi = arps_param.loc["qi"][best_index]
    Di = arps_param.loc["Di"][best_index]
    b = arps_param.loc["b"][best_index]
    if best_index == 2:
        Q_fitted = arps_model.hyperbolic_model(Time, qi, Di, b)
        G_fitted = Q_fitted.cumsum()
    elif best_index == 1:
        Q_fitted = arps_model.harmonic_model(Time, qi, Di)
        G_fitted = Q_fitted.cumsum()
    elif best_index == 0:
        Q_fitted = arps_model.exponential_model(Time, qi, Di)
        G_fitted = Q_fitted.cumsum()
        
    df = pd.DataFrame({
        'Time': Time,
        'Q_fitted': Q_fitted,
        'G_fitted': G_fitted
    })
    predict_plot(df, best, x_axis)
    
    col1, col2 = st.columns(2)
    col1.header("Min Economical Rate")
    min_rate = col2.number_input("ER",value= 150, step=1, format="%d")

    if best_index == 2:
        time_at_min = arps_model.hyperbolic_time_from_rate(min_rate, qi, Di, b)
        cum_at_min = arps_model.hyperbolic_cum_from_rate(min_rate, qi, Di, b)
    elif best_index == 1:
        time_at_min = arps_model.harmonic_time_from_rate(min_rate, qi, Di)
        cum_at_min = arps_model.harmonic_cum_from_rate(min_rate, qi, Di)
    elif best_index == 0:
        time_at_min = arps_model.exponential_time_from_rate(min_rate, qi, Di)
        cum_at_min = arps_model.exponential_cum_from_rate(min_rate, qi, Di)

    time_delta = timedelta(days=time_at_min)
    date = start_date + time_delta
    col1.header("At Time:")
    col1.write(f"In {date.date()}")
    col1.write(f"After {time_at_min} days production rate will be {min_rate}")
    col2.header("Cummulative Production:")
    col2.write(f"{cum_at_min} will have been produced at {min_rate} production rate")
