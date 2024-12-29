import matplotlib.pyplot as plt
import streamlit as st

def get_curves(df, las):
    colors = [
        "Red", "blue", "brown", "brown",                         #DEPTH BHT CAL CHT
        "black", "aqua", "blue", "red",                        #CN CNC CNCQH CNQH
            "Black", "green",                                    #SYSDEPTH GR
            "Red", "Blue", "Green",                             #MBVI MBVM MCBW
            "blue", "Orange", "Purple",                       #MPHE MPHS MPRM
            "orange", "red", "Black",                        #PEQH PORZ PORZC
                "green", "Red",                                  #TEN TTEN
                "red",                                         #WTBH
                "red", "blue", "black", "blue", "cyan", "black"#ZCORQH ZDEN ZDENQH ZDNC ZDNCQH tot_fluids
    ]

    data_dict = {}
    colors = [
        "Red", "blue", "brown", "brown",                         #DEPTH BHT CAL CHT
        "black", "aqua", "blue", "red",                        #CN CNC CNCQH CNQH
            "Black", "green",                                    #SYSDEPTH GR
            "Red", "Blue", "Green",                             #MBVI MBVM MCBW
            "blue", "Orange", "Purple",                       #MPHE MPHS MPRM
            "orange", "red", "Black",                        #PEQH PORZ PORZC
                "green", "Red",                                  #TEN TTEN
                "red",                                         #WTBH
                "red", "blue", "black", "blue", "cyan", "black"#ZCORQH ZDEN ZDENQH ZDNC ZDNCQH tot_fluids
    ]
    limits = [(2770, 2910), (84, 99), (0, 11), (-154, 6460),                                     #DEPT BHT CAL CHT
            (72, -15), (72, -15), (72, -15), (72, -15),                                       #CN CNC CNCQH CNQH
                (2770, 2910), (28, 150),                                                          #SYSDEPTH GR
                (0, 16), (0, 16), (0, 18.8),                                                    #MBVI MBVM MCBW
                (0, 23), (0, 23), (0.001, 100),                                                 #MPHE MPHS MPRM
                (2, 14), (-11, 61), (-11, 61),                                                 #PEQH PORZ PORZC
                (-154, 6460), (-154, 6460),                                                   #TEN TTEN
                (84, 99),                                                                    #WTBH
                (-0.5, 0.5), (1.5, 3), (1.5, 3), (1.5, 3) , (1.5, 3), (0, 16)                  #ZCORQH ZDEN ZDENQH ZDNC ZDNCQH tot_fluids
    ]

    for i, curve in enumerate(las.curves):
        mnemonic = curve.mnemonic
        description = curve.descr
        unit = curve.unit
        #value = list(curve.data)
        #shape = (len(curve.data),)

        data_dict[mnemonic] = {
            "description": description + "," + unit,
            "label": mnemonic + ', ' + unit,
            "color": colors[i],
            "limit": limits[i]
        }

    data_dict["tot_fluids"] = {
            "description": "tot_fluids",
            "label": "tot",
            "color": "black",
            "limit": (0, 16)
        }

    depth_limit = data_dict["DEPT"]["limit"]
    return data_dict


def graph_plot(df, ax, x,y = "DEPT",line_style = "-",marker = None, grid_style='--', font=10, bold=True, width=0.5, title="", label="",y_label = "", opacity=0.8,
                fill_between=None, invert_x = False, invert_y = True, logy = False, logx = False, grid = True, minor_ticks = True, data_dict = None):

    x_limit = data_dict[x]['limit']
    y_limit = data_dict[y]['limit']
    
    x_label = data_dict[x]['label']
    y_label = data_dict[y]['label']
    
  
    ax.plot(df[x], df[y], color=data_dict[x]['color'], lw=width,label = label, alpha=opacity, marker = marker)


    ax.set_title(title, fontsize=font, fontweight='bold' if bold else 'normal')
    
    if invert_x:
        ax.set_xlim(x_limit[1], x_limit[0])
    else:
        ax.set_xlim(x_limit)
    if invert_y:
        ax.set_ylim(y_limit[1], y_limit[0])
    else:
        ax.set_ylim(y_limit)
    
    if logy:
        ax.semilogy()
    if logx:
        ax.semilogx()

    ax.set_xlabel(label, fontsize=font)
    #ax.set_ylabel('Depth, M', fontsize=font)
    
    ax.grid(grid, which = "major", color = "#6666", linestyle = grid_style, alpha = opacity/2)
    ax.grid(grid, which = "minor", color = "#9999", linestyle = grid_style, alpha = opacity/10)

    if minor_ticks:
        ax.minorticks_on()
    #ax.legend(loc = "upper right")

def graph_scatter(df, ax, x,y = "DEPT",line_style = "-",marker = None, grid_style='--', font=10, bold=True, width=0.5, title="", label="",y_label = "", opacity=0.8,
                fill_between=None, invert_x = False, invert_y = True, logy = False, logx = False, grid = True, minor_ticks = True, add_color=False, color=None, min=0, max=100, colormap='viridis', data_dict = None):
    
    x_limit = data_dict[x]['limit']
    y_limit = data_dict[y]['limit']

    x_label = data_dict[x]['label']
    y_label = data_dict[y]['label']
        
    if add_color:
        ax.scatter(df[x], df[y], c=color, s=width, alpha=opacity, vmin=min, vmax=max, cmap=colormap)
    else:
        ax.scatter(df[x], df[y], color=data_dict[x]['color'], s=width, alpha=opacity)

    ax.set_title(title, fontsize=font, fontweight='bold' if bold else 'normal')
    
    if invert_x:
        ax.set_xlim(x_limit[1], x_limit[0])
    else:
        ax.set_xlim(x_limit)
    if invert_y:
        ax.set_ylim(y_limit[1], y_limit[0])
    else:
        ax.set_ylim(y_limit)
    
    if logy:
        ax.semilogy()
    if logx:
        ax.semilogx()

    ax.set_xlabel(label, fontsize=font)
    #ax.set_ylabel(y_label, fontsize=font)
    
    ax.grid(grid, which = "major", color = "#6666", linestyle = grid_style, alpha = opacity/2)
    ax.grid(grid, which = "minor", color = "#9999", linestyle = grid_style, alpha = opacity/10)

    if minor_ticks:
        ax.minorticks_on()
    #ax.legend(loc = "lower left")

def graph_histogram(df, ax, x, style='--', font=10, bold=True, bins=20, title="", label="", opacity=0.7, edge='black', logy = False, logx = False, grid = True, grid_style='--', data_dict = None):
    ax.hist(df[x], bins=bins, color=data_dict[x]['color'], alpha=opacity, edgecolor=edge)
    ax.set_xlim(data_dict[x]['limit'])
    if logy:
        ax.semilogy()
    if logx:
        ax.semilogx()
    ax.set_xlabel(label, fontsize=font)
    ax.set_ylabel("Frequency", fontsize=font)

    ax.set_title(title, fontsize=font, fontweight='bold' if bold else 'normal')
    ax.grid(grid, which = "major", color = "#6666", linestyle = grid_style, alpha = opacity/2)
    ax.grid(grid, which = "minor", color = "#9999", linestyle = grid_style, alpha = opacity/10)

def figure(df, curves_data):
    no_cols = 9
    no_rows = 8
    fig, axes = plt.subplots(nrows=no_rows, ncols=no_cols, figsize=(20, 24))

    ax1 = plt.subplot2grid(shape=(no_rows, no_cols), loc=(0, 0), rowspan=4, colspan=1)  #GR
    ax12 = plt.subplot2grid(shape=(no_rows, no_cols), loc=(0, 1), rowspan=4, colspan=1) #Photoelectric Cross-Section
    ax5 = plt.subplot2grid(shape=(no_rows, no_cols), loc=(0, 2), rowspan=4, colspan=1)  #Caliper
    ax6 = plt.subplot2grid(shape=(no_rows, no_cols), loc=(0, 3), rowspan=4, colspan=1)  #Temperatures

    ax3 = plt.subplot2grid(shape=(no_rows, no_cols), loc=(0, 4), rowspan=4, colspan=2)  #Neutron Porosity
    ax2 = plt.subplot2grid(shape=(no_rows, no_cols), loc=(0, 6), rowspan=4, colspan=2)  #Bulk Density

    ax19 = plt.subplot2grid(shape=(no_rows, no_cols), loc=(0, 8), rowspan=4, colspan=1) #Bulk Density

    ax7 = plt.subplot2grid(shape=(no_rows, no_cols), loc=(4, 0), rowspan=4, colspan=1)  #Tensions
    ax9 = plt.subplot2grid(shape=(no_rows, no_cols), loc=(4, 1), rowspan=4, colspan=1)  #Fluids
    ax10 = plt.subplot2grid(shape=(no_rows, no_cols), loc=(4, 2), rowspan=4, colspan=1) #Clay Fluids
    ax18 = plt.subplot2grid(shape=(no_rows, no_cols), loc=(4, 3), rowspan=4, colspan=1) #Permeabiltiy vs Depth scatter plot
    ax4 = plt.subplot2grid(shape=(no_rows, no_cols), loc=(4, 4), rowspan=4, colspan=2)  #Porosity
    ax11 = plt.subplot2grid(shape=(no_rows, no_cols), loc=(4, 6), rowspan=2, colspan=2) #Porosity vs. Permeability

    ax13 = plt.subplot2grid(shape=(no_rows, no_cols), loc=(6, 6), rowspan=2, colspan=2) #Neutron Porosity vs. Bulk Density

    ax14 = plt.subplot2grid(shape=(no_rows, no_cols), loc=(4, 8), rowspan=1, colspan=1) #Porsity Histogram
    ax15 = plt.subplot2grid(shape=(no_rows, no_cols), loc=(5, 8), rowspan=1, colspan=1) #Density Histogram
    ax16 = plt.subplot2grid(shape=(no_rows, no_cols), loc=(6, 8), rowspan=1, colspan=1) #Gamma Ray Histogram
    ax17 = plt.subplot2grid(shape=(no_rows, no_cols), loc=(7, 8), rowspan=1, colspan=1) #Permeability Histogram

    ax8 = ax2.twiny()                                                                   #Density Correction
    ax20 = ax19.twiny()                                                                 #neutron Porosity

    axes_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20]

    axes_curves_dict = {
                            ax1: [["GR"],                                "DEPT", ["p"],                  ["Gamma Ray", "Gamma Ray, GAPI"], [0.8]],
                            ax2: [["ZDEN", "ZDENQH", "ZDNC", "ZDNCQH"],  "DEPT", ["p", 's', 's', 'p'],   ["Density Logs", "ZDEN/ZDENQH/ZDNC/ZDNCQH, G/C3"], [0.8, 2, 3, 0.8]],
                            ax3: [["CN", "CNC", "CNCQH", "CNQH"],        "DEPT", ["s", 'p', 'p', 's'],   ["Neutron Porosity", "CN/CNC/CNCQH/CNQH, PU"], [4, 1, 1, 6]],
                            ax4: [["PORZ", "PORZC"],                     "DEPT", ["s", 'p'],             ["SELECT/Correc. Porosity Logs", "PORZ/PORZC, PU"], [3, 0.8]],
                            ax5: [["CAL"],                               "DEPT", ['p'],                  ["Caliper", "CAL, in"], [2]],
                            ax6: [["BHT", "WTBH"],                       "DEPT", ['s', 's'],             ["BoreHole Temp.", "BTH/WTBH, DEGC"], [4, 4]],
                            ax7: [["CHT", "TEN", "TTEN"],                "DEPT", ['p', 'p', 'p'],        ["Tension", "CHT/TEN/TTEN, LBF"], [1, 1, 1]],
                            ax8: [["ZCORQH"],                            "DEPT", ['p'],                  ["", "Correction in Density ZCORQH, G/C3"], [1]],
                            ax9: [["MBVI", "MBVM"],        "DEPT", ['p', 'p'],        ["MR Moveable vs Irreducible Fluids", "Fluids (PU)"], [1, 1, 1]],
                            ax10: [["MCBW"],                              "DEPT", ['p'],                  ['Clay Fluids', "Fluids (PU)"], [1]],
                            ax11: [["MPHE", "MPHS"],                      "MPRM", ['s', 's'],            ['Porosity/Permeability Scatter Plot', 'eff./tot. Porosity %'], [5, 5]],
                            ax12: [["PEQH"],                             "DEPT", ['p'],                     ['Photoelectric Cross-Section', 'PEQH, PU'], [1]],
                            ax13: [["CNCQH"],                            "ZDNCQH", ['s'],                     ['Neutron Porosity vs. Bulk Density with GR', 'Neutron Porosity, PU'], [7]],
                            ax14: [["MPHE", "MPHS"],                      "DEPT", ['h', 'h'],                     ['Porosity', 'MPHE/MPHS, PU'], [1]],
                            ax15: [["ZDNCQH"],                             "DEPT", ['h'],                     ['Density', 'ZDNCQH, G/C3'], [1]],
                            ax16: [["GR"],                                   "DEPT", ['h'],                     ['Gamma Ray', 'GR, GAPI'], [1]],
                            ax17: [["MPRM"],                             "DEPT", ['h'],                     ['Permeability', 'MPRM, mD'], [1]],
                            ax18: [["MPRM"],                             "DEPT", ['s'],                     ['Permeability Scatter Plot', 'Permeability, mD'], [5]],
                            ax19: [["ZDNCQH"],                             "DEPT", ['p'],                     ['Bulk Density vs. Neutron Porosity', 'Bulk Density, G/C3'], [1]],
                            ax20: [["CNCQH"],                             "DEPT", ['p'],                     ['', 'Neutron Porosity'], [1]]
    }


    for i, ax in enumerate(axes.flatten()):
            ax.set_xlabel('')  
            ax.set_xticklabels([])
            ax.set_yticklabels([])  

    for ax in axes_curves_dict:
        curves = axes_curves_dict[ax][0]
        y = axes_curves_dict[ax][1]
        if (y != "MPRM"):
            y_inv = True
        else:
            y_inv = False
        plot = axes_curves_dict[ax][2]
        names = axes_curves_dict[ax][3]
        sizes = axes_curves_dict[ax][4]
        for i, curve in enumerate(curves): 
            if y != 'ZDNCQH':
                if plot[i] == 'p':
                    graph_plot(df, ax, curve, y, title= names[0], label= names[1], width = sizes[i], invert_y = y_inv, data_dict=curves_data)
                elif plot[i] == 's':
                    graph_scatter(df, ax, curve, y, title= names[0], label= names[1], width = sizes[i], invert_y = y_inv, data_dict=curves_data)
                else:
                    graph_histogram(df, ax, curve, title= names[0], label= names[1], data_dict=curves_data)
            else:
                graph_scatter(df, ax, curve, y, title= names[0], label= names[1], width = sizes[i], invert_y = y_inv, invert_x=True, color=df["GR"], add_color=True, max=150, data_dict=curves_data)
                cbar = plt.colorbar(ax.collections[0], ax=ax, orientation='vertical')
                cbar.set_label('Gamma Ray', fontsize=10)   
        

        ax.legend(curves, loc = 'upper right')


    ax11.semilogy()
    ax17.semilogx()
    ax18.semilogx()


    for ax in [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax12, ax18, ax19]:
        ax.xaxis.set_ticks_position("top")
        ax.xaxis.set_label_position("top")
        ax.grid(True, linestyle='--')

    shift = 1.1
    for twin_ax in [ax8, ax20]:
        twin_ax.spines["top"].set_position(("axes", shift))
        twin_ax.spines["top"].set_visible(False)
        twin_ax.spines["top"].set_visible(True)

    for i, ax in enumerate(axes_list):
        plt.setp(ax.get_xticklabels(), rotation=45, ha="left")
        if i != 0 and i != 6 and i != 10 and i != 12 and i != 13 and i != 14 and i != 15 and i != 16:  
            plt.setp(ax.get_yticklabels(), visible=False)

    fig.subplots_adjust(wspace=0.04)

    plt.tight_layout()
    st.pyplot(fig)
