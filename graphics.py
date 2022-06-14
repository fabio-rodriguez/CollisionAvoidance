import json
import math
import numpy as np
import os
import plotly.graph_objects as go

from plotly.graph_objs import *
from sklearn.metrics import euclidean_distances


COLORS = ['rgb(255,0,0)', "rgb(0,0,255)", "rgb(0,255,0)", "rgb(255,255,0)", "rgb(255,0,255)", "rgb(0,0,0)"]


def orca_figures(path_to_exp_folder):

    waypoints = []
    for file_name in os.listdir(path_to_exp_folder):
        with open(f"{path_to_exp_folder}/{file_name}", "r") as file:
            waypoints.append([np.array(list(map(float, l.split()))) for l in file.readlines()])

    plot_waypoints(waypoints)


def cank_figures(path_to_exp_json):
    
    with open(f"{path_to_exp_json}", "r") as file:
        dict = json.loads(file.read())

    waypoints_dict = dict["waypoints"]
    waypoints = [list(zip(v["X"], v["Y"])) for v in waypoints_dict.values()]

    plot_waypoints(waypoints)


def waypoint_cleaning(waypoints):
    wps2 = [waypoints[0]]
    for point in waypoints[1:]:
        if euclidean_dist(point, wps2[-1]) > 10**-4:
            wps2.append(point)

    return wps2


def euclidean_dist(v1, v2):
    return math.sqrt(sum([(xi - xj)**2  for xi, xj in zip(v1, v2)]))


def plot_waypoints(waypoints):

    layout = Layout(
        margin=go.layout.Margin(
            l=0,  # left margin
            r=0,  # right margin
            b=0,  # bottom margin
            t=0,  # top margin
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        # xaxis=dict(mirror=True, ticks='outside', showline=True, linecolor = 'rgba(0,0,0,1)', gridcolor='rgba(0,0,0,1)', zerolinecolor='rgba(150,150,150,1)'),
        # yaxis=dict(mirror=True, ticks='outside', showline=True, linecolor = 'rgba(0,0,0,1)', gridcolor='rgba(0,0,0,1)', zerolinecolor='rgba(150,150,150,1)'),
        xaxis=dict(mirror=True, ticks='outside', showline=True, linecolor='rgba(0,0,0,1)'),
        yaxis=dict(mirror=True, ticks='outside', showline=True, linecolor='rgba(0,0,0,1)'),
    )

    fig = go.Figure(layout=layout)
    # fig.update_xaxes(zeroline=True, zerolinewidth=1)
    # fig.update_yaxes(zeroline=True, zerolinewidth=1)
    # fig.update_xaxes(showgrid=True, gridwidth=1)
    # fig.update_yaxes(showgrid=True, gridwidth=1)
    # fig.update_xaxes(showline=True, linewidth=2, linecolor='black', gridcolor='Red')
    # fig.update_yaxes(showline=True, linewidth=2, linecolor='black', gridcolor='Red')


    for wps, c in zip(waypoints, COLORS):

        initx, inity = wps[0]
        goalx, goaly = wps[-1]

        wps=waypoint_cleaning(wps)

        Xs, Ys = zip(*wps)

        fig.add_trace(
            # go.Scatter(x=[initx], y=[inity], mode='markers', line_color='rgba(230,0,0,1)', name="Initial state", marker_size=11))
            go.Scatter(x=[initx], y=[inity], mode='markers', line_color=c, marker_size=11, showlegend=False))

        fig.add_trace(
            go.Scatter(x=[goalx], y=[goaly], mode='markers', marker_symbol="x", line_color=c, marker_size=11, showlegend=False))

        fig.add_trace(
            go.Scatter(x=Xs, y=Ys, mode='lines, markers', line=dict(color=c,), line_width=3, showlegend=False))
                                                                            # dash='dash'), name="OSPA", line_width=3))
        # fig.add_trace(
        #     go.Scatter(x=ann_Xs, y=ann_Zs, name="ANN prediction", mode='lines, markers', line_color='rgba(0,0,250,0.8)',
        #             line_width=3, ))

        # fig.add_trace(
        #     go.Scatter(x=rnn_Xs, y=rnn_Zs, name="RNN prediction", mode='lines, markers', line_color='rgba(0,180,0,0.8)',
        #             line_width=3, ))

        # fig.add_trace(
        #     go.Scatter(x=[0,250], y=[0,96.5], mode='markers', name="", line_color='rgba(255,0,0,1)', showlegend=False, marker_size=8))

    # fig.update_layout(legend=dict(x=0.708, y=1, traceorder="normal", font=dict(family="sans-serif",
    #                                                                         size=16, color="black"), bgcolor="White",
    #                             borderwidth=2))
    fig.update_layout(showlegend=False)

    # ['solid', 'dot', 'dash', 'longdash', 'dashdot',
    #  'longdashdot']

    # fig.update_layout(
    #     autosize=False,
    #     width=1000,
    #     height=500,
    #     )

    # fig.update_yaxes(range=[-52, 2])
    # fig.update_yaxes(autorange="reversed", zeroline=True, zerolinewidth=1, zerolinecolor='rgba(0,0,0,0.4)')

    # fig.update_layout(xaxis_title="x(m)", yaxis_title="z(m)",
    #                   font=dict(family="Courier New, monospace", size=18, color="Black"))
    # fig.update_xaxes(range=[-2, 89])

    fig.show()
    # fig.write_image("5DTU.pdf")


if __name__=="__main__":

    # exp_5AA = r"C:\Users\jmesca\Desktop\CollisionAvoidance\orca\TimeStep0.25\5AA"
    # exp_6A = r"C:\Users\jmesca\Desktop\CollisionAvoidance\orca\TimeStep0.25\6A"
    exp_6AAO = r"C:\Users\jmesca\Desktop\CollisionAvoidance\orca\TimeStep0.25\6AAO"
    # exp_5DTU = r"C:\Users\jmesca\Desktop\CollisionAvoidance\orca\TimeStep0.25\5DTU"
    orca_figures(exp_6AAO)

    # exp_6A = r"C:\Users\jmesca\Desktop\CollisionAvoidance\outputs\radio 0.5\experiments1.json"
    # exp_5DTU = r"C:\Users\jmesca\Desktop\CollisionAvoidance\outputs\radio 0.5\experiments2.json"
    # exp_6AAO = r"C:\Users\jmesca\Desktop\CollisionAvoidance\outputs\radio 0.5\experiments3.json"
    # exp_5AA = r"C:\Users\jmesca\Desktop\CollisionAvoidance\outputs\radio 0.5\experiments4.json"
    # cank_figures(exp_6AAO)
