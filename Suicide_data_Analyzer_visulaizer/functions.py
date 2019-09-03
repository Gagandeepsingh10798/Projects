# import libraries
from tkinter import *
import pandas as pd
import tkinter.messagebox as mb
import numpy as np
import matplotlib.pyplot as plt
# import libraries


def sme_plotting(year, state, cause):
    df = pd.read_csv("data.csv")
    df = df[(df["STATE/UT"] == state) & (df["CAUSE"] == cause) & (df["Year"] == year)]
    df.set_index("Year", inplace=True)
    x_pos = np.arange(1, 14)
    df = df[df.columns[2:]]
    y = df.loc[year, :].values
    x = list(df)
    ax = plt.subplot()
    ax.set_xticks(x_pos)
    ax.set_xticklabels(x)
    plt.xticks(rotation="-90")
    p1 = plt.bar(x_pos, y)
    plt.title("Chart for %s and %s" % (state, cause))
    plt.xlabel(year)
    plt.ylabel("Victims", rotation="vertical")
    auto_label(p1, ax)
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()
    plt.tight_layout()
    plt.show()


def pie_state(year, state):
    df = pd.read_csv("data.csv")
    df = df[
        (df["Year"] == year) & (df["STATE/UT"] == state) & (df["CAUSE"] != "Total") & (df["CAUSE"] != "Total Illness")]
    df = df[(df["Total M+F"] > np.percentile(df["Total M+F"], 20))]
    x = sorted(df["Total M+F"].values, reverse=True)
    y = df["CAUSE"].values
    xper = np.array(x)
    lenexp = len(y)
    ax1 = plt.subplot()
    porcent = 100. * xper / xper.sum()
    y = ['{0} - {1:1.2f} %'.format(i, j) for i, j in zip(y, porcent)]
    ax1.pie(x, explode=(0.05, 0) * int(lenexp / 2), startangle=90)
    ax1.axis('equal')
    ax1.legend(y, fontsize=6, ncol=2, loc=3)
    plt.subplots_adjust(top=2.1, bottom=1.8, right=10.5)
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()
    plt.tight_layout()
    plt.show()


def sme_state_growth(year1, year2, state, age):
    df = pd.read_csv("data.csv")
    df = df[(df["STATE/UT"] == state) & ((df["Year"] == year1) | (df["Year"] == year2))]
    df = df[(df["CAUSE"] == "Total")]
    df.set_index('Year', inplace=True)
    df = df[(df.columns[2:16])]
    x_pos = np.arange(1, 3)
    x = np.array([year1, year2])
    y = df[age].values
    ax = plt.subplot()
    ax.set_xticks(x_pos)
    ax.set_xticklabels(x)
    p1 = ax.bar(x_pos, y)
    plt.title("Chart for %s and %s for %s" % (year1, year2, state))
    plt.xlabel(age)
    plt.ylabel("Victims", rotation="vertical")
    auto_label(p1, ax)
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()
    plt.tight_layout()
    plt.show()


def shw_data_all_year(state, age="Total M+F", cause="Total"):
    df = pd.read_csv("data.csv")
    df = df[(df["STATE/UT"] == state) & (df["CAUSE"] == cause)]
    x = np.array(list(set(df['Year'].values)))
    x_pos = np.arange(1, x.size + 1)
    y = df[age].values
    ax = plt.subplot()
    ax.set_xticks(x_pos)
    ax.set_xticklabels(x)
    plt.title("Data for all year for %s and %s" % (state, cause))
    plt.xlabel(age)
    plt.ylabel("Victims", rotation="vertical")
    p1 = ax.bar(x_pos, y)
    auto_label(p1, ax)
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()
    plt.tight_layout()
    plt.show()


def shw_data_all_cause(state, age, year):
    df = pd.read_csv("data.csv")
    df = df[
        (df["STATE/UT"] == state) & (df["Year"] == year) & (df["CAUSE"] != "Total") & (df["CAUSE"] != "Total Illness")]
    df = df[(df[age] > np.percentile(df[age], 20))]
    x = df["CAUSE"].values
    x_pos = np.arange(1, x.size + 1)
    y = df[age].values
    ax = plt.subplot()
    ax.set_xticks(x_pos)
    ax.set_xticklabels(x)
    p1 = ax.bar(x_pos, y)
    plt.title("Data for all cause for %s and %s" % (state, year))
    plt.xlabel(age)
    plt.ylabel("Victims", rotation="vertical")
    plt.xticks(rotation="vertical")
    auto_label(p1, ax)
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()
    plt.tight_layout()
    plt.show()


def shw_data_all_state(year, cause, age):
    df = pd.read_csv("data.csv")
    df = df[(df["Year"] == year) & (df["CAUSE"] == cause) & (df["STATE/UT"] != "TOTAL (STATES)") &
            (df["STATE/UT"] != "TOTAL (UTs)") & (df["STATE/UT"] != "TOTAL (ALL INDIA)") & (df[age] != 0)]

    x = df["STATE/UT"].values
    x_pos = np.arange(1, x.size + 1)
    y = df[age].values
    ax = plt.subplot()
    ax.set_xticks(x_pos)
    ax.set_xticklabels(x)
    p1 = ax.bar(x_pos, y)
    plt.title("Data for all states for %s and %s" % (year, cause))
    plt.xlabel(age)
    plt.ylabel("Victims", rotation=90)
    plt.xticks(rotation="vertical")
    auto_label(p1, ax)
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()
    plt.tight_layout()
    plt.show()


def cmp_two_states(state1, state2, year):
    df = pd.read_csv("data.csv")
    df = df[
        ((df["STATE/UT"] == state1) | (df["STATE/UT"] == state2)) & (df["Year"] == year) & (df["CAUSE"] == "Total")]
    df = df.drop(columns=["Total M", "Total F", "Total M+F"])
    df.set_index("STATE/UT", inplace=True)
    x = df.columns[2:].values
    x_pos = np.arange(x.size)
    df = df.drop(df.columns[0:2], axis=1)
    y1 = df.loc[state1, :].values
    y2 = df.loc[state2, :].values
    fig, ax = plt.subplots()
    width = 0.36
    p1 = ax.bar(x_pos, y1, width, color='#229922', bottom=0)
    p2 = ax.bar(x_pos + width, y2, width, color='#F12217', bottom=0)
    ax.set_xticks(x_pos + width / 2)
    ax.set_xticklabels(x)
    ax.legend((p1[0], p2[0]), (state1, state2))
    plt.ylabel("Victims", rotation=90)
    plt.xticks(rotation="vertical")
    plt.title("Comparison b/w %s and %s for year %s" % (state1, state2, year))
    auto_label(p1, ax)
    auto_label(p2, ax)
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()
    plt.tight_layout()
    plt.show()


def all_year_shw(state, cause):
    df = pd.read_csv("data.csv")
    df = df[(df["STATE/UT"] == state) & (df["CAUSE"] == cause)]
    x = np.array(list(set(df["Year"])))
    x_pos = np.arange(1, x.size + 1)
    y1 = df["Total M"].values
    y2 = df["Total F"].values
    y3 = df["Total M+F"].values
    ax = plt.subplot()
    ax.set_xticks(x_pos)
    ax.set_xticklabels(x)
    p1 = ax.plot(x_pos, y1, marker="o", linewidth=2.3)
    p2 = ax.plot(x_pos, y2, marker="o", linewidth=2.3)
    p3 = ax.plot(x_pos, y3, marker="o", linewidth=2.3)
    ax.legend((p1[0], p2[0], p3[0]), ("Total Male", "Total Female", "Grand Total"))
    plt.title("Trend of suicide rate in %s for %s" % (state, cause))
    plt.ylabel("Victims", rotation=90)
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()
    plt.tight_layout()
    plt.show()


def auto_label(reacts, ax_sub):
    """
    Attach a text label above each bar displaying its height
    """
    ax = ax_sub
    for rect in reacts:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1.005 * height,
                '%d' % int(height),
                ha='center', va='bottom')




