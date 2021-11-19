#! /usr/bin/env python3
'''
Create Gantt chart with csv file of tasks and dates
'''

from pathlib import Path
import datetime

import matplotlib.axes as axes
import datasense as ds
import pandas as pd


def main():
    # data for the example, comment out when using csv file
    data = {
        'start': ['2021-11-01', '2021-11-03', '2021-11-04', '2021-11-08'],
        'end': ['2021-11-08', '2021-11-16', '2021-11-11', '2021-11-13'],
        'task': ['task 1', 'task 2', 'task 3', 'task 4']
    }
    columns = ['task', 'start', 'end', 'duration', 'start_relative']
    graph_file = Path('gantt_chart.svg')
    # data_file = Path('gantt_chart.csv'), uncomment to use csv file
    parse_dates = ['start', 'end']
    data_types = {
        'start': 'datetime64[ns]',
        'end': 'datetime64[ns]',
        'task': 'str'
    }
    fig_title = 'figure title'
    ax_title = 'axes title'
    y_axis_label = 'tasks'
    x_axis_label = 'date'
    # uncomment when using csv filee
    # df = ds.read_file(
    #     file_name=data_file,
    #     parse_dates=parse_dates
    # )
    df = (pd.DataFrame(data=data)).astype(dtype=data_types)
    # create duration of tasks, dtype = 'int64'
    df[columns[3]] = (df[columns[2]] - df[columns[1]]).dt.days + 1
    # sort start dates in ascending order
    df = df.sort_values(
        by=[columns[1]],
        axis=0,
        ascending=[True]
    )
    # create project variables
    start = df[columns[1]].min()
    end = df[columns[2]].max()
    duration = (end - start).days + 1
    # create xticks and labels
    x_ticks = [x for x in range(duration + 1)]
    x_labels = [
        (start + datetime.timedelta(days=x)).strftime('%Y-%m-%d')
        for x in x_ticks
    ]
    # create relative start column, dtype = 'int64'
    df[columns[4]] = (df[columns[1]] - start).dt.days
    # plot Gantt chart
    fig, ax = ds.plot_horizontal_bars(
        y=df[columns[0]],
        width=df[columns[3]],
        left=df[columns[4]]
    )
    ax.invert_yaxis()
    ax.set_xticks(
        ticks=x_ticks
    )
    ax.set_xticklabels(labels=x_labels, rotation=45)
    fig.suptitle(
        t=fig_title,
        horizontalalignment='center',
        verticalalignment='top',
        fontsize=15,
        fontweight='bold'
    )
    ax.grid(
        axis='x',
        alpha=0.25
    )
    ax.set_title(
        label=ax_title,
        loc='center',
        horizontalalignment='center',
        verticalalignment='top',
        fontsize=12,
        fontweight='semibold'
    )
    ax.set_ylabel(
        ylabel=y_axis_label,
        loc='center',
        fontsize=12,
        fontweight='semibold'
    )
    ax.set_xlabel(
        xlabel=x_axis_label,
        loc='center',
        fontsize=12,
        fontweight='semibold'
    )
    fig.savefig(
        fname=graph_file,
        bbox_inches='tight'
    )
    print(df)
    print()
    print(df.dtypes)


if __name__ == '__main__':
    main()
