import numpy as np
from welly import Well
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
import plotly.graph_objects as go
import lasio
from Exercises_21_functions import get_curves, figure


def load(file, type):
    file_extension = type.lower()
    las = None
    if file_extension == ".las":
        las = lasio.read(file)  # Pass the file object directly to lasio.read
        df = las.df()
    elif file_extension == ".csv":
        df = pd.read_csv(file)
    elif file_extension == ".xlsx":
        df = pd.read_excel(file)
    else:
        raise ValueError("Unsupported file type")
    if ("DEPT" not in df.columns)  & ("DATEPRD" not in df.columns) & ("MD" not in df.columns):
        df.reset_index(drop=False, inplace=True)
    if ("MD" in df.columns) & ("INC" in df.columns) & ("AZI" in df.columns):
        df = df[["MD", "INC", "AZI"]]
        df['TVD'] = df['MD'] * np.cos(np.radians(df['INC']))
        df['x-offset'] = df['MD'] * np.sin(np.radians(df['INC'])) * np.cos(np.radians(df['AZI']))
        df['y-offset'] = df['MD'] * np.sin(np.radians(df['INC'])) * np.sin(np.radians(df['AZI']))
        las = Well()
        las.name = 'Well_0'
        las.data['survey'] = df
        las.location.add_deviation(df[['MD', 'INC', 'AZI']])
    return df, las

def plotly_line(fig, df, x, y,color = ["red"], logx=False, logy=False, invertx=False, inverty=True, square = False):
    columns = x if isinstance(x, list) else [x]
    if square:
        h = 600
    else:
        h = 1200
    if len(x) == len(color):
        for i, column in enumerate(columns):

            line = px.line(
                df,
                x=column,
                y=y
            )

            for trace in line.data:
                trace.update(line=dict(color=color[i]))
                fig.add_trace(trace, row=1, col=i+1)
            if column in ["RDEP", "RMED", "MPRM", "CKHG"]:
                fig.update_xaxes(type='log') 
            if logx:
                fig.update_xaxes(type='log')
            if logy:
                fig.update_yaxes(type='log')
            if invertx:
                fig.update_xaxes(autorange="reversed")
            if inverty:
                fig.update_yaxes(autorange="reversed")

            fig.update_xaxes(title_text=column, row=1, col=i+1)
        fig.update_yaxes(title_text=y, row=1, col=1)

        fig.update_layout(
            height=h,
            width=len(columns) * 400,  # Adjust width based on the number of columns
            title_text=f'Line Plots for {x} vs. {y}',
            showlegend=True
        )
        st.plotly_chart(fig)
    else:
        st.wrie("Choose a color for each Curve")



def plotly_scatter(fig, df, x, y, color_by = None,add_color = False, logx=False, logy=False, invertx=False, inverty=True, square = True):
    columns = x if isinstance(x, list) else [x]

    if square:
        h = 600
    else:
        h = 1200
    for i, column in enumerate(columns):
        st.write(column)
        if add_color:
            scatter = px.scatter(
                df,
                x=df[column],
                y=df[y],
                color=df[color_by]
            )
        else:
            scatter = px.scatter(
                df,
                x=df[column],
                y=df[y]
            )

        # scatter.update_traces(marker = dict(color = color_by))
        for trace in scatter.data:
            fig.add_trace(trace, row=1, col=i+1)

        if logx:
            fig.update_xaxes(type='log', row=1, col=i+1)
        if logy:
            fig.update_yaxes(type='log', row=1, col=i+1)
        if invertx:
            fig.update_xaxes(autorange="reversed", row=1, col=i+1)
        if inverty:
            fig.update_yaxes(autorange="reversed", row=1, col=i+1)

        fig.update_xaxes(title_text=column, row=1, col=i+1)
        fig.update_yaxes(title_text=y, row=1, col=i+1)

    fig.update_layout(
        height=h,
        width=len(columns) * 600,  # Adjust width based on the number of columns
        title_text=f'Scatter Plots for {x} vs. {y} with {color_by}',
        coloraxis=dict(colorscale='viridis', colorbar=dict(title=color_by)),
        showlegend = True
    )

    st.plotly_chart(fig)

# def graph_plot(df, ax, x,y = "DEPT", line_style = "-",marker = None, grid_style='--', font=10, bold=True, width=0.5, title="", label="",y_label = "", opacity=0.8,
#                 fill_between=None, invert_x = False, invert_y = True, logy = False, logx = False, grid = True, minor_ticks = True,color = ["green", "yellow", "red", "black", "blue"]):

    
  
#     ax.plot(df[x], df[y],c = color, lw=width,label = label, alpha=opacity, marker = marker)


#     ax.set_title(title, fontsize=font, fontweight='bold' if bold else 'normal')
    
#     if logy:
#         ax.semilogy()
#     if logx:
#         ax.semilogx()

#     ax.set_xlabel(label, fontsize=font)

    
#     ax.grid(grid, which = "major", color = "#6666", linestyle = grid_style, alpha = opacity/2)
#     ax.grid(grid, which = "minor", color = "#9999", linestyle = grid_style, alpha = opacity/10)

#     if minor_ticks:
#         ax.minorticks_on()

def plot_ex_11(df):
    fig, ax = plt.subplots() 
    scatter = ax.scatter(x=df['NEU'], y=df['DEN'], c=df['GR'], cmap='viridis', vmin=0, vmax=100)

    ax.set_xlim(-15, 45)  # Set limits for x-axis
    ax.set_ylim(3, 1.5)   # Set reversed limits for y-axis (to flip it)

    ax.set_title('Bulk Density to Neutron Porosity Scatter Plot with GR')  # Add title
    ax.set_ylabel("Bulk density, G/C3")  # Label for y-axis
    ax.set_xlabel("Neutron porosity, PU")  # Label for x-axis

    # Add color bar
    cbar = plt.colorbar(scatter, ax=ax, label="Gamma Ray")

    ax.grid(False)  # Remove grid lines

    st.pyplot(fig)

def plot_exe_12(df, x, y):
    fig, axes = plt.subplots(figsize=(10, 16))
    curves = ["Gamma Ray", "Medium Resistivity", "Bulk Density", "Neutron Porosity", "Deep Resistivity"]
    #plt.title('Gamma Ray, Deep Resistivity, Bulk Density, Neutron Porosity to Depth', fontsize=16, )

    ax1 = plt.subplot2grid((1, 3), (0, 0), rowspan=1, colspan=1)
    ax2 = plt.subplot2grid((1, 3), (0, 1), rowspan=1, colspan=1)
    ax3 = plt.subplot2grid((1, 3), (0, 2), rowspan=1, colspan=1)
    ax4 = ax3.twiny()
    ax5 = ax2.twiny()


    ax1.plot(df[x[0]], df[y], data=df, color = "green", lw=0.7)
    ax1.set_xlim(0, 200)

    ax2.plot(df[x[1]], df[y], data=df, color = "orange", lw=0.7)
    ax2.set_xlim(0.02, 200)
    ax2.semilogx()

    ax3.plot(df[x[2]], df[y], color = "red", lw=0.7)
    ax3.grid(True, axis='x', linestyle='--')
    ax3.set_xlim(1.5, 3)

    ax4.plot(df[x[3]], df[y], color = "blue", lw=0.7)
    ax4.grid(True, axis='x')
    ax4.set_xlim(45, -15)

    ax5.plot(df[x[4]], df[y], color = "black", lw=0.7)
    ax5.semilogx()
    ax5.grid(True, axis='x')
    ax5.set_xlim(0.02, 200)

    for i, ax in enumerate([ax1, ax2, ax3, ax4, ax5]):
        ax.set_ylim(df[y].max(), df[y].min())
        ax.xaxis.set_ticks_position("top")
        ax.xaxis.set_label_position("top")
        ax.set_xlabel(curves[i], fontsize=14)
        ax.grid(True, linestyle='--')

    ax4.spines["top"].set_position(("axes", 1.1))
    ax5.spines["top"].set_position(("axes", 1.1))


    plt.setp(ax2.get_yticklabels(), visible=False)
    plt.setp(ax3.get_yticklabels(), visible=False)

    fig.subplots_adjust(wspace=0.04)
    plt.tight_layout()

    st.pyplot(fig)

def plot_exe_13(df):
    fig, ax = plt.subplots(figsize=(10, 14))

    ax1 = plt.subplot2grid(shape=(3, 3), loc=(0, 0), rowspan=3)
    ax2 = plt.subplot2grid(shape=(3, 3), loc=(0, 1), rowspan=3)
    ax3 = plt.subplot2grid(shape=(3, 3), loc=(0, 2))
    ax4 = plt.subplot2grid(shape=(3, 3), loc=(1, 2))
    ax5 = plt.subplot2grid(shape=(3, 3), loc=(2, 2))

    # Core Porosity vs DEPTH         
    ax1.scatter(df['CPOR'], df['DEPTH'], marker='.', c='red')
    ax1.set_xlim(0, 40)
    ax1.set_ylim(4000, 3800)
    ax1.set_xlabel('Core Porosity', fontsize=10)
    ax1.set_ylabel('Depth', fontsize=10)
    ax1.grid(True, which='both', axis='x', linestyle='--')
    ax1.set_title('Core Porosity vs Depth', fontsize=11, fontweight='bold')  # Bold title

    # Core Permeability vs DEPTH     
    ax2.scatter(df['CKHG'], df['DEPTH'], marker='.', c='green')
    ax2.set_xlim(0.01, 20000)
    ax2.set_ylim(4000, 3800)
    ax2.semilogx()
    ax2.set_xlabel('Core Permeability', fontsize=10)
    ax2.grid(True, which='both', axis='x', linestyle='--')
    ax2.set_title('Core Permeability vs Depth', fontsize=11, fontweight='bold')  # Bold title

    # Core Porosity vs Core Permeability 
    ax3.scatter(df['CPOR'], df['CKHG'], marker='.', alpha=0.6)  # Porosity on x and permeability on y
    ax3.semilogy()
    ax3.set_ylim(0.01, 20000)
    ax3.set_xlim(0, 40)
    ax3.set_title('Porosity/Permeability Scatter Plot', fontsize=11, fontweight='bold')  # Bold title
    ax3.set_xlabel('Core Porosity %', fontsize=10)
    ax3.set_ylabel('Core Permeability mD', fontsize=10)
    ax3.grid(True, which='both', axis='x', linestyle='--')

    # Core Porosity Histogram
    ax4.hist(df['CPOR'], bins=30, edgecolor='black', color='red', alpha=0.8)
    ax4.set_xlabel('Core Porosity', fontsize=10)
    ax4.set_ylabel('Frequency', fontsize=10)
    ax4.grid(True, which='both', axis='y', linestyle='--')
    ax4.set_title('Core Porosity Histogram', fontsize=11, fontweight='bold')  # Bold title

    # Core Grain Density Histogram
    ax5.hist(df['CGD'], bins=30, edgecolor='black', color='brown', alpha=0.8)
    ax5.set_xlabel('Core Grain Density', fontsize=10)
    ax5.set_ylabel('Frequency', fontsize=10)
    ax5.grid(True, linestyle='--')
    ax5.set_title('Core Grain Density Histogram', fontsize=11, fontweight='bold')  # Bold title

    plt.setp(ax2.get_yticklabels(), visible=False)
    plt.tight_layout() 
    st.pyplot(fig)

def plot_exe_21(df, las):
    curves_data = get_curves(df, las)
    figure(df, curves_data)

curves_names = [("x-offset", "y-offset", "X Offset", "Y Offset", "Top View of Well Path"),
                 ("x-offset", "TVD", "X Offset", "Total Vertical Depth", "X Offset vs TVD"),
                 ("y-offset", "TVD", "Y Offset", "Total Vertical Depth", "Y Offset vs TVD")]

def plot_exe_22(df):
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 15))

    ax1 = axes[0, 0]  
    ax2 = axes[1, 0]  
    ax3 = axes[0, 1] 

    for i, curve in enumerate(curves_names):
        if i == 0:
            ax = ax1
        elif i == 1:
            ax = ax2
        elif i == 2:
             ax = ax3
        else:
            ax = None

        if ax is not None:
            ax.plot(df[curve[0]], df[curve[1]], linestyle='-', label='Well Path', marker = "o", markersize = 3)
            ax.scatter(df[curve[0]].iloc[0], df[curve[1]].iloc[0], color='green', marker='o', s=100, label='Start')
            ax.scatter(df[curve[0]].iloc[-1], df[curve[1]].iloc[-1], color='red', marker='x', s=100, label='End')

            if curve[1] == "TVD":
                ax.set_ylim(3000, 0)
            else:
                ax.set_ylim(-1250, 100)
                
            ax.set_xlim(-1250, 100)
            ax.set_xlabel(curve[2])
            ax.set_ylabel(curve[3])
            ax.set_title(curve[4])
            ax.grid(which = "major", color = "#6666", linestyle = "-", alpha = 0.5)
            ax.grid(which = "minor", color = "#9999", linestyle = "-", alpha = 0.1)
            ax.minorticks_on()
            ax.legend()

    plt.tight_layout()
    st.pyplot(fig)

def plot_exe_23(well):
    datum = [589075.56, 5963534.91, 0]

    trajectory = well.location.trajectory(datum=datum)

    fig = px.scatter_3d(trajectory, x=0, y=1, z=2)
    fig.update_layout(scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    ))

    st.plotly_chart(fig)
    # fig = plt.figure(figsize=(10, 10))
    # ax = fig.add_subplot(111, projection='3d')

    # ax.plot(x_trajectory, y_trajectory, z_trajectory, label='Well Path', color='blue', marker = "o", markersize = 3)
    # #ax.scatter(x_trajectory, y_trajectory, z_trajectory, color='blue', s = 5)

    # ax.scatter(x_trajectory[0], y_trajectory[0], z_trajectory[0], color='green', label='Start', s=100, marker = "o")
    # ax.scatter(x_trajectory[-1], y_trajectory[-1], z_trajectory[-1], color='red', label='End', s=100, marker = "x")

    # ax.set_xlabel('X Offset, M')
    # ax.set_ylabel('Y Offset, M')
    # ax.set_zlabel('TVD, M')
    # ax.set_title('3D Plot of Well Path')
    # ax.legend()
    # st.pyplot(fig)

