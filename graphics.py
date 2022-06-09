import plotly.graph_objects as go
from plotly.graph_objs import *


def ml_figures():

    sfx, sfz = 86.50167201927657, -46.300493489627755
    
    # tr_actions = [[-0.0, 0.0, 31.53455812455641], [-0.0, 0.0, 31.53455812455641], [-0.0, 0.0, 31.53455812455641], [-0.01745, 0.0, 31.53455812455641], [-0.0, 0.0, 31.53455812455641], [-0.01745, 0.0, 31.53455812455641], [-0.01745, 0.0, 31.53455812455641], [-0.01745, 0.0, 31.53455812455641]]
    # tr_Xs, tr_Zs = get_real_trajectory2(s_0, s_f, tr_actions)
    tr_ospa = [[0.0, 0.0, 4.257165346815115, 0.0, 0, 0],
               [4.833593742993324, -1.9561447297269416, 7.023492212473488, 0.33250685111525674, -0.53210536563414,
                -0.011984719408558431],
               [11.979867312536674, -8.052150652242632, 11.837087637947002, 0.17058715791727982, -0.77292302029129,
                -0.004711596121476739],
               [22.511835593727465, -16.768358878203404, 15.074550404138355, 0.32423317901361076, -0.5556242464104221,
                0.008234261347403083],
               [35.447795112493615, -26.019937449884303, 16.772024184421124, 0.13954272468859089, -0.6595011463038636,
                -0.002783436365483963],
               [48.78006604550103, -37.40500473372655, 18.289066061256698, 0.12396689507965677, -0.7338448868221312,
                -0.001983431245918755],
               [64.3113548624202, -47.05209759839953, 18.031847614639734, 0.34897122716215834, -0.34744646168529486,
                0.011363554731315012],
               [80.24330895808401, -47.4702615024728, 13.762353813199736, 0.49185759116700484, 0.34287721698637286,
                0.016868848767523693],
               [86.49951362549281, -45.680102912094526, 11.068440228456327, 0.23738270753001495, 0.24098250632297044,
                -0.007211796854206375]]

    ospa_Xs, ospa_Zs = [s[0] for s in tr_ospa], [s[1] for s in tr_ospa]
    ann_states = [(0.0, 0.0, 4.257165346815115, 0.0, 0, 0), (
        4.83359374299332, -1.956144729726941, 7.023492212473483, 0.332506851115255, -0.5321053656341397,
        -0.01198471940855843), (
                      11.979867312536655, -8.052150652242604, 11.837087637947024, 0.17058715791724038,
                      -0.7729230202912865,
                      -0.004711596121477775), (
                      21.292890374353842, -18.51371814409633, 16.015517041688202, 0.12034007333374941,
                      -0.8756890507219356,
                      -0.0021869901384044235), (
                      34.182430027566845, -29.692869943606816, 17.729530066166088, 0.33682512895155253,
                      -0.5187235994632516,
                      0.011392939086453295), (
                      49.17571107876908, -39.30308962529452, 18.022399382996188, 0.13694017289836047,
                      -0.6032475843644117,
                      -0.0025006996204138543), (
                      65.16450384901142, -46.86713410918026, 17.133931633174925, 0.3499180535269267,
                      -0.2489763957495634,
                      0.010113919893935243), (
                      80.81280435699195, -48.97056272383181, 14.37071081081039, 0.3511295187664961,
                      0.013771200594079578,
                      0.006333244729127564), (
                      86.49172632690383, -48.829566877856436, 13.010823334017624, 0.3530654251463786,
                      0.08423751289761942,
                      0.004415043261014019)]
    ann_Xs, ann_Zs = [s[0] for s in ann_states], [s[1] for s in ann_states]

    rnn_states = [[86.50167202, -46.30049349],
                  [80.82680096, -42.87318874],
                  [72.89104217, -36.47088772],
                  [61.77720766, -28.19834474],
                  [48.67542665, -19.39333519],
                  [34.64522757, -10.1580709],
                  [20.30878114, -2.08958486],
                  [4.69899879, 0.89272503],
                  [0, 0.20620407]]
    rnn_Xs, rnn_Zs = [sfx - s[0] for s in rnn_states], [sfz - s[1] for s in rnn_states]

    # _, _ , spline_Xs, spline_Zs, _, _ = save_splines_fig(s_0, tr_actions, tr_Xs, tr_Zs,)

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

    fig.add_trace(
        go.Scatter(x=[0], y=[0], mode='markers', line_color='rgba(230,0,0,1)', name="Initial state", marker_size=11))

    fig.add_trace(
        go.Scatter(x=[sfx], y=[sfz], mode='markers', marker_symbol="x", line_color='rgba(230,0,0,1)', name="Target state", marker_size=11))

    fig.add_trace(
        go.Scatter(x=ospa_Xs, y=ospa_Zs, mode='lines, markers', line=dict(color='rgba(230,0,0,0.8)',
                                                                          dash='dash'), name="OSPA", line_width=3))
    fig.add_trace(
        go.Scatter(x=ann_Xs, y=ann_Zs, name="ANN prediction", mode='lines, markers', line_color='rgba(0,0,250,0.8)',
                   line_width=3, ))

    fig.add_trace(
        go.Scatter(x=rnn_Xs, y=rnn_Zs, name="RNN prediction", mode='lines, markers', line_color='rgba(0,180,0,0.8)',
                   line_width=3, ))

    # fig.add_trace(
    #     go.Scatter(x=[0,250], y=[0,96.5], mode='markers', name="", line_color='rgba(255,0,0,1)', showlegend=False, marker_size=8))

    fig.update_layout(legend=dict(x=0.708, y=1, traceorder="normal", font=dict(family="sans-serif",
                                                                               size=16, color="black"), bgcolor="White",
                                  borderwidth=2))
    fig.update_layout(showlegend=True)

    # ['solid', 'dot', 'dash', 'longdash', 'dashdot',
    #  'longdashdot']

    # fig.update_layout(
    #     autosize=False,
    #     width=1000,
    #     height=500,
    #     )

    fig.update_yaxes(range=[-52, 2])
    # fig.update_yaxes(autorange="reversed", zeroline=True, zerolinewidth=1, zerolinecolor='rgba(0,0,0,0.4)')

    # fig.update_layout(xaxis_title="x(m)", yaxis_title="z(m)",
    #                   font=dict(family="Courier New, monospace", size=18, color="Black"))
    fig.update_xaxes(range=[-2, 89])

    fig.write_image("cmp f1.pdf")
    # fig.show()

    sfx, sfz = 66.06196846974954, -7.160890902459571
    
    # tr_actions = [[-0.0, 0.0, 31.53455812455641], [-0.0, 0.0, 31.53455812455641], [-0.0, 0.0, 31.53455812455641], [-0.01745, 0.0, 31.53455812455641], [-0.0, 0.0, 31.53455812455641], [-0.01745, 0.0, 31.53455812455641], [-0.01745, 0.0, 31.53455812455641], [-0.01745, 0.0, 31.53455812455641]]
    # tr_Xs, tr_Zs = get_real_trajectory2(s_0, s_f, tr_actions)
    tr_ospa = [[0.0, 0.0, 4.257165346815115, 0.0, 0, 0],
               [4.79506777490283, -1.4638811882184906, 6.2839991154031045, 0.5314843830004248, -0.32338538143675755,
                -0.00500913924473525],
               [11.693976127283648, -2.886236765604612, 7.083755405271106, 0.7465383962392173, 0.14022887943528753,
                0.01487875174052424],
               [18.21050783617125, -2.867348731967174, 6.184278005106781, 0.5534226549847824, 0.00863446478244077,
                -0.005719836049241177],
               [24.420225227847816, -3.509565954064236, 6.292771546212997, 0.6155290933610574, -0.014536841033369576,
                -0.0003678990687097975],
               [30.78516875055082, -4.219290530207691, 6.455945561138071, 0.6110477004919678, -0.011464375380114572,
                0.00048486030575454553],
               [37.54565859701106, -6.2434614232419605, 8.269760670864718, 0.29795273811914563, -0.4224434174570917,
                -0.010207603668499945],
               [46.18728254475367, -8.045376381853337, 8.65967502980998, 0.6771579310647498, 0.16120916467315854,
                0.017216346444852423],
               [54.20327920170923, -8.461456544417455, 8.07579247651758, 0.3245252264043659, -0.19176451672034478,
                -0.01118403544775037],
               [61.80652355109008, -8.32643280322925, 6.441084892958119, 0.7237434859636129, 0.39390981900511524,
                0.012084968400437995],
               [66.05892304330395, -7.817939702046915, 5.077739348801904, 0.5092712997224509, -0.028100789452073408,
                -0.019468311228632757]]

    ospa_Xs, ospa_Zs = [s[0] for s in tr_ospa], [s[1] for s in tr_ospa]
    ann_states = [(0.0, 0.0, 4.257165346815115, 0.0, 0, 0), (
        4.646300694829413, -0.9288265457656706, 5.3189225978776316, 0.7632488542210144, -0.0659040231615018,
        0.0020554660519761674), (
                      10.279469424121674, -1.6750905088618984, 5.687910758809455, 0.7547629264746634, 0.08421981011775263,
                      0.005324638323115884), (
                      15.616750319786494, -1.6928324010736198, 4.822522645234317, 0.7768661295367164, 0.16195917248740377,
                      -0.001243755445614223), (
                      20.257663711758752, -1.970676314203565, 4.5928421279505365, 0.7946911395178458, 0.04165570951798995,
                      -0.004121769605910526), (
                      25.170453132027895, -2.7258428523804517, 5.247358863304302, 0.7668642802376254, 0.0006384297912681819,
                      0.0015986300559152772), (
                      30.559103041962658, -3.267468930309012, 5.338021031141986, 0.7628909489443848, 0.08640279967608512,
                      0.0026356830010171254), (
                      35.976290642170426, -3.945624028906698, 5.764719251750047, 0.6328621272412375, -0.081311722586595,
                      -0.0034030331505513676), (
                      42.181537901249484, -5.201663198923586, 6.804833769474803, 0.6012229164008447, -0.0937085463643636,
                      0.0021862173681960495), (
                      49.15321932326208, -6.120275985926842, 7.047613227370539, 0.5985885522107122, 0.007521867030785466,
                      0.0033932446592212194), (
                      56.13647016210785, -6.850354205997051, 7.086584571056233, 0.5221270161385564, -0.06510317745391113,
                      -0.0020299784749185402), (
                      63.20783751467042, -7.495385218744379, 6.915850280357584, 0.6006145656696426, 0.04741161939800061,
                      0.0028354131594125827), (
                      66.05836998992064, -7.781287055135797, 6.964038612221277, 0.376430379915691, -0.13117547334677063,
                      -0.013458349668135172)]

    ann_Xs, ann_Zs = [s[0] for s in ann_states], [s[1] for s in ann_states]

    rnn_states = [[66.06196847, -7.1608909],
                  [62.09713624, -5.905042],
                  [54.77146715, -4.01170512],
                  [46.90027078, -3.0926993],
                  [39.95778144, -2.90187751],
                  [33.59619543, -2.51127802],
                  [27.18410418, -1.59934953],
                  [20.18830067, -0.4582306],
                  [12.88963203, 0.5081864],
                  [6.18308349, 0.92196426],
                  [1.2235539, 0.81411415],
                  [0, 0.61990601]]
    rnn_Xs, rnn_Zs = [0] + [sfx - s[0] for s in rnn_states], [0] + [sfz - s[1] for s in rnn_states]
    # _, _ , spline_Xs, spline_Zs, _, _ = save_splines_fig(s_0, tr_actions, tr_Xs, tr_Zs,)


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

    fig.add_trace(
        go.Scatter(x=[0], y=[0], mode='markers', line_color='rgba(230,0,0,1)', name="Initial state", marker_size=11))

    fig.add_trace(
        go.Scatter(x=[sfx], y=[sfz], mode='markers', marker_symbol="x", line_color='rgba(230,0,0,1)', name="Target state", marker_size=11))

    fig.add_trace(
        go.Scatter(x=ospa_Xs, y=ospa_Zs, mode='lines, markers', line=dict(color='rgba(230,0,0,0.8)',
                                                                          dash='dash'), name="OSPA", line_width=3))
    fig.add_trace(
        go.Scatter(x=ann_Xs, y=ann_Zs, name="ANN prediction", mode='lines, markers', line_color='rgba(0,0,250,0.8)',
                   line_width=3, ))

    fig.add_trace(
        go.Scatter(x=rnn_Xs, y=rnn_Zs, name="RNN prediction", mode='lines, markers', line_color='rgba(0,180,0,0.8)',
                   line_width=3, ))

    # fig.add_trace(
    #     go.Scatter(x=[0,250], y=[0,96.5], mode='markers', name="", line_color='rgba(255,0,0,1)', showlegend=False, marker_size=8))

    fig.update_layout(legend=dict(x=0.708, y=1, traceorder="normal", font=dict(family="sans-serif",
                                                                               size=16, color="black"), bgcolor="White",
                                  borderwidth=2))
    fig.update_layout(showlegend=True)

    # ['solid', 'dot', 'dash', 'longdash', 'dashdot',
    #  'longdashdot']

    # fig.update_layout(
    #     autosize=False,
    #     width=1000,
    #     height=500,
    #     )

    fig.update_yaxes(range=[-9, 0.5])
    # fig.update_yaxes(autorange="reversed", zeroline=True, zerolinewidth=1, zerolinecolor='rgba(0,0,0,0.4)')

    # fig.update_layout(xaxis_title="x(m)", yaxis_title="z(m)",
    #                   font=dict(family="Courier New, monospace", size=18, color="Black"))
    fig.update_xaxes(range=[-2, 68])

    fig.write_image("cmp f2.pdf")
    # fig.show()

    sfx, sfz = 53.04666590815438, -11.15627190194964
    
    # tr_actions = [[-0.0, 0.0, 31.53455812455641], [-0.0, 0.0, 31.53455812455641], [-0.0, 0.0, 31.53455812455641], [-0.01745, 0.0, 31.53455812455641], [-0.0, 0.0, 31.53455812455641], [-0.01745, 0.0, 31.53455812455641], [-0.01745, 0.0, 31.53455812455641], [-0.01745, 0.0, 31.53455812455641]]
    # tr_Xs, tr_Zs = get_real_trajectory2(s_0, s_f, tr_actions)
    tr_ospa = [[0.0, 0.0, 4.257165346815115, 0.0, 0, 0],
               [4.745068697222255, -1.2437566999243914, 5.915146749566081, 0.6180499312841097, -0.22818002319939584,
                -0.00242293497127862],
               [11.340265584650075, -4.808308579295759, 9.458643202613153, 0.23948448844563003, -0.5979603954845759,
                -0.007738665851972252],
               [21.072353159630815, -9.838886606633467, 11.923622839326567, 0.47910996198299965, -0.26010697770327734,
                0.0124236437395039],
               [32.569713663174724, -14.39418416208291, 13.071659927300889, 0.19281679155861695, -0.45012593631662823,
                -0.005323543614889928],
               [44.877744979840124, -15.75820266015874, 11.209460538900727, 0.5976001570963321, 0.3124058994730166,
                0.01974481685450948],
               [52.426556090656995, -12.111717197810199, 5.4210340525931615, 0.5525606503908194, 0.655909558141902,
                -0.00021822449156843433]
               ]

    ospa_Xs, ospa_Zs = [s[0] for s in tr_ospa], [s[1] for s in tr_ospa]
    ann_states = [(0.0, 0.0, 4.257165346815115, 0.0, 0, 0), (
    4.83359374299332, -1.956144729726941, 7.023492212473483, 0.332506851115255, -0.5321053656341397, -0.01198471940855843),
                  (12.372279371580733, -7.233444356472296, 11.197549274327296, 0.3278740088241256, -0.5645339019823639,
                   0.0027356080372407726), (
                  23.542173172121124, -11.875390832646731, 12.464853132393936, 0.4878313849060076, -0.14387558901677358,
                  0.013533686999395908), (
                  35.45580936574809, -15.069270591439368, 12.565003814992124, 0.20800589592630125, -0.3419279527014634,
                  -0.0059630264979553035), (
                  47.56335700444633, -17.102412131593134, 11.573349518989273, 0.48591045546024925, 0.07818632555066314,
                  0.01135906794374555), (
                  53.04385208392214, -16.143281473672545, 9.59619504495319, 0.574797606453968, 0.37119133413778393,
                  0.014509156850548495)]
    ann_Xs, ann_Zs = [s[0] for s in ann_states], [s[1] for s in ann_states]

    rnn_states = [[53.04666591, -11.1562719],
                  [47.86521455, -9.40183758],
                  [39.87841609, -5.50307403],
                  [29.43250651, -1.27855526],
                  [17.78884408, 1.84935378],
                  [6.59019876, 2.44417836],
                  [0, 0.80359116]]
    rnn_Xs, rnn_Zs = [0] + [sfx - s[0] for s in rnn_states], [0] + [sfz - s[1] for s in rnn_states]
    # _, _ , spline_Xs, spline_Zs, _, _ = save_splines_fig(s_0, tr_actions, tr_Xs, tr_Zs,)


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

    fig.add_trace(
        go.Scatter(x=[0], y=[0], mode='markers', line_color='rgba(230,0,0,1)', name="Initial state", marker_size=11))

    fig.add_trace(
        go.Scatter(x=[sfx], y=[sfz], mode='markers', marker_symbol="x", line_color='rgba(230,0,0,1)', name="Target state", marker_size=11))

    fig.add_trace(
        go.Scatter(x=ospa_Xs, y=ospa_Zs, mode='lines, markers', line=dict(color='rgba(230,0,0,0.8)',
                                                                          dash='dash'), name="OSPA", line_width=3))
    fig.add_trace(
        go.Scatter(x=ann_Xs, y=ann_Zs, name="ANN prediction", mode='lines, markers', line_color='rgba(0,0,250,0.8)',
                   line_width=3, ))

    fig.add_trace(
        go.Scatter(x=rnn_Xs, y=rnn_Zs, name="RNN prediction", mode='lines, markers', line_color='rgba(0,180,0,0.8)',
                   line_width=3, ))

    # fig.add_trace(
    #     go.Scatter(x=[0,250], y=[0,96.5], mode='markers', name="", line_color='rgba(255,0,0,1)', showlegend=False, marker_size=8))

    fig.update_layout(legend=dict(x=0.708, y=1, traceorder="normal", font=dict(family="sans-serif",
                                                                               size=16, color="black"), bgcolor="White",
                                  borderwidth=2))
    fig.update_layout(showlegend=True)

    # ['solid', 'dot', 'dash', 'longdash', 'dashdot',
    #  'longdashdot']

    # fig.update_layout(
    #     autosize=False,
    #     width=1000,
    #     height=500,
    #     )

    fig.update_yaxes(range=[-18, 1])
    # fig.update_yaxes(autorange="reversed", zeroline=True, zerolinewidth=1, zerolinecolor='rgba(0,0,0,0.4)')

    # fig.update_layout(xaxis_title="x(m)", yaxis_title="z(m)",
    #                   font=dict(family="Courier New, monospace", size=18, color="Black"))
    fig.update_xaxes(range=[-2, 55])

    fig.write_image("cmp f3.pdf")
    # fig.show()

    sfx, sfz = 52.684860713298576, -8.060745519438429
    
    # tr_actions = [[-0.0, 0.0, 31.53455812455641], [-0.0, 0.0, 31.53455812455641], [-0.0, 0.0, 31.53455812455641], [-0.01745, 0.0, 31.53455812455641], [-0.0, 0.0, 31.53455812455641], [-0.01745, 0.0, 31.53455812455641], [-0.01745, 0.0, 31.53455812455641], [-0.01745, 0.0, 31.53455812455641]]
    # tr_Xs, tr_Zs = get_real_trajectory2(s_0, s_f, tr_actions)
    tr_ospa = [[0.0, 0.0, 4.257165346815115, 0.0, 0, 0],
               [4.825840764969672, -1.7019249877721245, 6.654846780400203, 0.4363682118768771, -0.4247275532176861,
                -0.00819497199749176],
               [12.319618755807564, -5.385809329137704, 9.735793908603066, 0.47035886926476095, -0.3306307208759724,
                0.006981340202779672],
               [22.04754931475757, -6.857692220196215, 9.37091506578385, 0.5867400879843752, 0.1420388426163739,
                0.013042974814647881],
               [29.67849396936547, -5.238200142005848, 6.0436924222482435, 0.5944607150199018, 0.3734893963996824,
                9.056802852867168e-05],
               [34.815226727297826, -5.185167898005929, 5.361982024129863, 0.4814801469163179, -0.20307321969738412,
                -0.018493291468500733],
               [41.0071791792107, -7.204657100195395, 7.476306745863678, 0.5858849050450504, -0.1850236736079168,
                0.005406053215594175],
               [48.72605440139513, -8.414928854824145, 7.7847505396465095, 0.5897442164857066, 0.029035930432562775,
                0.006682550713239219],
               [52.67838958314, -8.86527598908204, 7.82441362713253, 0.3357197748773158, -0.16350547532784673,
                -0.011662587084496606]
               ]

    ospa_Xs, ospa_Zs = [s[0] for s in tr_ospa], [s[1] for s in tr_ospa]
    ann_states = [(0.0, 0.0, 4.257165346815115, 0.0, 0, 0), (
        4.745068697222255, -1.2437566999243914, 5.915146749566081, 0.6180499312841097, -0.22818002319939584,
        -0.0024229349712786208), (
                      11.413287187173996, -3.2286208003297543, 7.716290207938156, 0.5863441176240125, -0.13762325519833657,
                      0.006390388872633141), (
                      19.344324435113958, -4.684804757056733, 8.286528193180866, 0.49708792294376086, -0.09170843850958782,
                      0.0021984412107229944), (
                      27.571205797865982, -5.648892657051463, 8.165756444407254, 0.5001408896692795, -0.023434168377686932,
                      0.0018032925501616705), (
                      35.47720320218804, -6.180277113183978, 7.645822481785346, 0.5094057179366829, 0.0075366320637598365,
                      6.6592729197717e-05), (
                      43.15810189831722, -7.937807953300269, 8.705087871235248, 0.29090545725567996, -0.35244091008321626,
                      -0.009809528691926037), (
                      51.944974845884786, -9.087737490529072, 8.32315329588036, 0.6703643028159391, 0.23430439034327288,
                      0.01583673334236004), (
                      52.684836096171345, -8.963124671094805, 8.077809265232165, 0.3480743888988693, 0.20597187048091625,
                      -0.013276895302781248)]
    ann_Xs, ann_Zs = [s[0] for s in ann_states], [s[1] for s in ann_states]

    rnn_states = [[52.68486071, -8.06074552],
                  [47.5563571, -6.54064214],
                  [39.73977374, -3.54424597],
                  [30.20467655, -0.63021033],
                  [20.05882781, 1.3180298],
                  [10.30889076, 1.93234365],
                  [2.81430929, 1.20069074],
                  [0, 0.33638894]]
    rnn_Xs, rnn_Zs = [0] + [sfx - s[0] for s in rnn_states], [0] + [sfz - s[1] for s in rnn_states]
    # _, _ , spline_Xs, spline_Zs, _, _ = save_splines_fig(s_0, tr_actions, tr_Xs, tr_Zs,)


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

    fig.add_trace(
        go.Scatter(x=[0], y=[0], mode='markers', line_color='rgba(230,0,0,1)', name="Initial state", marker_size=11))

    fig.add_trace(
        go.Scatter(x=[sfx], y=[sfz], mode='markers', marker_symbol="x", line_color='rgba(230,0,0,1)', name="Target state", marker_size=11))

    fig.add_trace(
        go.Scatter(x=ospa_Xs, y=ospa_Zs, mode='lines, markers', line=dict(color='rgba(230,0,0,0.8)',
                                                                          dash='dash'), name="OSPA", line_width=3))
    fig.add_trace(
        go.Scatter(x=ann_Xs, y=ann_Zs, name="ANN prediction", mode='lines, markers', line_color='rgba(0,0,250,0.8)',
                   line_width=3, ))

    fig.add_trace(
        go.Scatter(x=rnn_Xs, y=rnn_Zs, name="RNN prediction", mode='lines, markers', line_color='rgba(0,180,0,0.8)',
                   line_width=3, ))

    # fig.add_trace(
    #     go.Scatter(x=[0,250], y=[0,96.5], mode='markers', name="", line_color='rgba(255,0,0,1)', showlegend=False, marker_size=8))

    fig.update_layout(legend=dict(x=0.708, y=1, traceorder="normal", font=dict(family="sans-serif",
                                                                               size=16, color="black"), bgcolor="White",
                                  borderwidth=2))
    fig.update_layout(showlegend=True)

    # ['solid', 'dot', 'dash', 'longdash', 'dashdot',
    #  'longdashdot']

    # fig.update_layout(
    #     autosize=False,
    #     width=1000,
    #     height=500,
    #     )

    fig.update_yaxes(range=[-10.5, 0.5])
    # fig.update_yaxes(autorange="reversed", zeroline=True, zerolinewidth=1, zerolinecolor='rgba(0,0,0,0.4)')

    # fig.update_layout(xaxis_title="x(m)", yaxis_title="z(m)",
    #                   font=dict(family="Courier New, monospace", size=18, color="Black"))
    fig.update_xaxes(range=[-1, 54.1])

    fig.write_image("cmp f4.pdf")
    # fig.show()


def orca_figures():
    
    sfx, sfz = 86.50167201927657, -46.300493489627755
    
    # tr_actions = [[-0.0, 0.0, 31.53455812455641], [-0.0, 0.0, 31.53455812455641], [-0.0, 0.0, 31.53455812455641], [-0.01745, 0.0, 31.53455812455641], [-0.0, 0.0, 31.53455812455641], [-0.01745, 0.0, 31.53455812455641], [-0.01745, 0.0, 31.53455812455641], [-0.01745, 0.0, 31.53455812455641]]
    # tr_Xs, tr_Zs = get_real_trajectory2(s_0, s_f, tr_actions)
    tr_ospa = [[0.0, 0.0, 4.257165346815115, 0.0, 0, 0],
               [4.833593742993324, -1.9561447297269416, 7.023492212473488, 0.33250685111525674, -0.53210536563414,
                -0.011984719408558431],
               [11.979867312536674, -8.052150652242632, 11.837087637947002, 0.17058715791727982, -0.77292302029129,
                -0.004711596121476739],
               [22.511835593727465, -16.768358878203404, 15.074550404138355, 0.32423317901361076, -0.5556242464104221,
                0.008234261347403083],
               [35.447795112493615, -26.019937449884303, 16.772024184421124, 0.13954272468859089, -0.6595011463038636,
                -0.002783436365483963],
               [48.78006604550103, -37.40500473372655, 18.289066061256698, 0.12396689507965677, -0.7338448868221312,
                -0.001983431245918755],
               [64.3113548624202, -47.05209759839953, 18.031847614639734, 0.34897122716215834, -0.34744646168529486,
                0.011363554731315012],
               [80.24330895808401, -47.4702615024728, 13.762353813199736, 0.49185759116700484, 0.34287721698637286,
                0.016868848767523693],
               [86.49951362549281, -45.680102912094526, 11.068440228456327, 0.23738270753001495, 0.24098250632297044,
                -0.007211796854206375]]

    ospa_Xs, ospa_Zs = [s[0] for s in tr_ospa], [s[1] for s in tr_ospa]
    ann_states = [(0.0, 0.0, 4.257165346815115, 0.0, 0, 0), (
        4.83359374299332, -1.956144729726941, 7.023492212473483, 0.332506851115255, -0.5321053656341397,
        -0.01198471940855843), (
                      11.979867312536655, -8.052150652242604, 11.837087637947024, 0.17058715791724038,
                      -0.7729230202912865,
                      -0.004711596121477775), (
                      21.292890374353842, -18.51371814409633, 16.015517041688202, 0.12034007333374941,
                      -0.8756890507219356,
                      -0.0021869901384044235), (
                      34.182430027566845, -29.692869943606816, 17.729530066166088, 0.33682512895155253,
                      -0.5187235994632516,
                      0.011392939086453295), (
                      49.17571107876908, -39.30308962529452, 18.022399382996188, 0.13694017289836047,
                      -0.6032475843644117,
                      -0.0025006996204138543), (
                      65.16450384901142, -46.86713410918026, 17.133931633174925, 0.3499180535269267,
                      -0.2489763957495634,
                      0.010113919893935243), (
                      80.81280435699195, -48.97056272383181, 14.37071081081039, 0.3511295187664961,
                      0.013771200594079578,
                      0.006333244729127564), (
                      86.49172632690383, -48.829566877856436, 13.010823334017624, 0.3530654251463786,
                      0.08423751289761942,
                      0.004415043261014019)]
    ann_Xs, ann_Zs = [s[0] for s in ann_states], [s[1] for s in ann_states]

    rnn_states = [[86.50167202, -46.30049349],
                  [80.82680096, -42.87318874],
                  [72.89104217, -36.47088772],
                  [61.77720766, -28.19834474],
                  [48.67542665, -19.39333519],
                  [34.64522757, -10.1580709],
                  [20.30878114, -2.08958486],
                  [4.69899879, 0.89272503],
                  [0, 0.20620407]]
    rnn_Xs, rnn_Zs = [sfx - s[0] for s in rnn_states], [sfz - s[1] for s in rnn_states]

    # _, _ , spline_Xs, spline_Zs, _, _ = save_splines_fig(s_0, tr_actions, tr_Xs, tr_Zs,)

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

    fig.add_trace(
        go.Scatter(x=[0], y=[0], mode='markers', line_color='rgba(230,0,0,1)', name="Initial state", marker_size=11))

    fig.add_trace(
        go.Scatter(x=[sfx], y=[sfz], mode='markers', marker_symbol="x", line_color='rgba(230,0,0,1)', name="Target state", marker_size=11))

    fig.add_trace(
        go.Scatter(x=ospa_Xs, y=ospa_Zs, mode='lines, markers', line=dict(color='rgba(230,0,0,0.8)',
                                                                          dash='dash'), name="OSPA", line_width=3))
    fig.add_trace(
        go.Scatter(x=ann_Xs, y=ann_Zs, name="ANN prediction", mode='lines, markers', line_color='rgba(0,0,250,0.8)',
                   line_width=3, ))

    fig.add_trace(
        go.Scatter(x=rnn_Xs, y=rnn_Zs, name="RNN prediction", mode='lines, markers', line_color='rgba(0,180,0,0.8)',
                   line_width=3, ))

    # fig.add_trace(
    #     go.Scatter(x=[0,250], y=[0,96.5], mode='markers', name="", line_color='rgba(255,0,0,1)', showlegend=False, marker_size=8))

    fig.update_layout(legend=dict(x=0.708, y=1, traceorder="normal", font=dict(family="sans-serif",
                                                                               size=16, color="black"), bgcolor="White",
                                  borderwidth=2))
    fig.update_layout(showlegend=True)

    # ['solid', 'dot', 'dash', 'longdash', 'dashdot',
    #  'longdashdot']

    # fig.update_layout(
    #     autosize=False,
    #     width=1000,
    #     height=500,
    #     )

    fig.update_yaxes(range=[-52, 2])
    # fig.update_yaxes(autorange="reversed", zeroline=True, zerolinewidth=1, zerolinecolor='rgba(0,0,0,0.4)')

    # fig.update_layout(xaxis_title="x(m)", yaxis_title="z(m)",
    #                   font=dict(family="Courier New, monospace", size=18, color="Black"))
    fig.update_xaxes(range=[-2, 89])

    fig.write_image("cmp f1.pdf")
    # fig.show()



if __name__=="__main__":

    orca_figures()