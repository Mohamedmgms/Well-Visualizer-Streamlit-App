import numpy as np
from scipy.optimize import curve_fit
import pandas as pd
import streamlit as st

def smooth(df, window, names_list):

    clean_df = df[(df[names_list[3]] > 0) & (df[names_list[0]] == names_list[1])]
    clean_df['smooth_prod'] = clean_df[names_list[3]].rolling(window=window, center=True).mean()
    clean_df["days"] = (clean_df[names_list[2]] - clean_df[names_list[2]].min()).dt.days
    clean_df["smooth_cum_prod"] = clean_df["smooth_prod"].cumsum()

    return clean_df

def exponential_model(t, qi, Di): #b = 0
    Q = qi * np.exp(-Di * t)  
    return  Q
def exponential_cum_from_rate(Q, qi, Di):
    G = (qi-Q)/Di
    return G
def exponential_rate_from_cum(G, qi, Di):
    Q = qi - Di*G
    return Q
def exponential_time_from_rate(q, qi, Di):
    t = np.log(qi / q) / Di
    return t


def harmonic_model(t, qi, Di): #b = 1
    Q= qi / (1 + Di * t) 
    return Q
def harmonic_rate_from_cum(G, qi, Di):
    Q = qi / np.exp(Di * G / qi)
    return Q
def harmonic_cum_from_time(T, qi, Di):
    G = (qi / Di) * np.log(1 + Di * T)
    return G
def harmonic_cum_from_rate(q, qi, Di):
    G = (qi / Di) * np.log(qi / q)
    return G
def harmonic_time_from_rate(q, qi, Di):
    t = (qi - q) / (q * Di)
    return t

def hyperbolic_model(t, qi, Di, b):
    Q = qi / (1 + b * Di * t)**(1/b)
    # st.write(Q)
    return Q
def hyperbolic_rate_from_cum(Gp, qi, Di, b):
    if b != 1:
        t1 = qi ** (1-b)
        t2 = Gp * Di * (1-b) / (qi ** b)
        Qt = (t1 - t2) ** ( 1/ (1-b))
    else:
        Qt = qi * np.exp(- (Gp * Di) / qi)
    return Qt
def hyperbolic_cum_from_rate(q, qi, Di, b):
    if b != 1:
        t1 = (q ** b)/(Di * (1-b))
        t2 = qi ** (1-b)
        t3 = q ** (1-b)
        Gp = t1 * (t2-t3)
    else:
        Gp = (qi/Di) * np.log(qi/q)

    return Gp

def hyperbolic_cum_from_time(t, qi, Di, b):
    if b != 1:
        t1 = qi/(Di*(1-b))
        t2 = ((1+b*Di*t)**(1-1/b) - 1)
        Gp = t1 * t2
    else:
        t1 = qi/Di
        t2 = (1-np.exp(-Di*t))
        Gp = t1 * t2
    return Gp

def hyperbolic_time_from_rate(q, qi, Di, b):
    t1 = ((qi/q) ** b) - 1
    t2 = b * Di

    return t1 / t2

def error(orig, fitted):
    n = len(orig)
    t1 = (orig-fitted)**2
    t2 = np.sum(t1)
    t3 = t2/n
    err = np.sqrt(t3)
    return err

def exponential_fit(T, Q, G):
    T_norm = T/max(T)
    Q_norm = Q/max(Q)
    G_norm = G/max(G)    
    params, _ = curve_fit(exponential_model, T_norm, Q_norm, maxfev=2000)
    qi, Di = params
    qi = qi*max(Q)
    Di = Di/max(T)
    b = 0
    params = qi, Di, b
    Q_fitted = exponential_model(T, qi, Di)
    return params, Q_fitted

def harmonic_fit(T, Q, G):
    T_norm = T/max(T)
    Q_norm = Q/max(Q) 
    G_norm = G/max(G)   
    params, _ = curve_fit(harmonic_model, T_norm, Q_norm, maxfev=2000)
    qi, Di = params
    qi = qi*max(Q)
    Di = Di/max(T)
    b = 1
    params = qi, Di, b
    Q_fitted = harmonic_model(T, qi, Di)
    return params, Q_fitted

def hyperbolic_fit(T, Q, G):
    T_norm = T/max(T)
    Q_norm = Q/max(Q)
    G_norm = G/max(G)
    params, _ = curve_fit(hyperbolic_model, T_norm, Q_norm, maxfev=2000)
    qi, Di, b = params
    qi = qi*max(Q)
    Di = Di/max(T)
    params = qi, Di, b
    Q_fitted = hyperbolic_model(T, qi, Di, b)
    return params, Q_fitted

def exponential_cum_fit(T, Q, G):
    T_norm = T/max(T)
    Q_norm = Q/max(Q)
    G_norm = G/max(G)    
    params, _ = curve_fit(exponential_rate_from_cum, G_norm, Q_norm, maxfev=2000)
    qi, Di = params
    qi = qi*max(Q)
    Di = Di/max(T)
    b = 0
    params = qi, Di, b
    Q_fitted = exponential_rate_from_cum(G, qi, Di)
    return params, Q_fitted

def harmonic_cum_fit(T, Q, G):
    T_norm = T/max(T)
    Q_norm = Q/max(Q) 
    G_norm = G/max(G)   
    params, _ = curve_fit(harmonic_rate_from_cum, G_norm, Q_norm, maxfev=2000)
    qi, Di = params
    qi = qi*max(Q)
    Di = Di/max(T)
    b = 1
    params = qi, Di, b
    Q_fitted = harmonic_rate_from_cum(G, qi, Di)
    return params, Q_fitted


def hyperbolic_cum_fit(T, Q, G):
    T_norm = T/max(T)
    Q_norm = Q/max(Q)
    G_norm = G/max(G)
    params, _ = curve_fit(hyperbolic_rate_from_cum, G_norm, Q_norm, maxfev=2000)
    qi, Di, b = params
    qi = qi*max(Q)
    Di = Di/max(T)
    params = qi, Di, b
    Q_fitted = hyperbolic_rate_from_cum(G, qi, Di, b)
    return params, Q_fitted

def arps(df, window, x_axis, names_list):
    df = smooth(df, window, names_list)

    df = df[[names_list[2], "days", names_list[3], "smooth_prod", "smooth_cum_prod"]].dropna()
    T = df["days"]
    Q = df["smooth_prod"]
    G = df["smooth_cum_prod"]
    if x_axis == "Days":
        ex_param, Q_fitted_exp = exponential_fit(T, Q, G)
        ha_param, Q_fitted_har = harmonic_fit(T, Q, G)
        hy_param, Q_fitted_hyp = hyperbolic_fit(T, Q, G)
    else:
        ex_param, Q_fitted_exp = exponential_fit(T, Q, G)
        ha_param, Q_fitted_har = harmonic_fit(T, Q, G)
        hy_param, Q_fitted_hyp = hyperbolic_cum_fit(T, Q, G)
    arps_param = {"Exponential": ex_param,
                "Harmonic": ha_param,
                "Hyperbolic": hy_param}
    arps_param = pd.DataFrame(arps_param)
    df["Exponential Fitted"] = Q_fitted_exp
    df["Harmonic Fitted"] = Q_fitted_har
    df["Hyperbolic Fitted"] = Q_fitted_hyp
    arps_param.index = ["qi", "Di", "b"]
 
    return arps_param, df[[names_list[2], "days", names_list[3], "smooth_prod", "smooth_cum_prod",
                            "Exponential Fitted", "Harmonic Fitted", "Hyperbolic Fitted"]]

