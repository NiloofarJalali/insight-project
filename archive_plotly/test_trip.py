import pickle
from datetime import date, timedelta
import datetime
import plotly
import numpy as np
import plotly.graph_objs as go
import chart_studio.plotly as py
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from plotly.subplots import make_subplots
from plotly.graph_objs import *
import math as m


############### Loading the file

with open("/Users/niloofar/Documents/insight/data/cleaned/hotel2/sentiment_topic_final",'rb') as f:
        df=pickle.load(f,encoding='latin1')


# sdate = date(2013, 3, 1)   # start date
# edate = date(2020, 1, 1)   # end date
# delta = edate - sdate
# season=(delta/90).days
# Date=[]
# for i in range(0,season):
#     pt=sdate + timedelta(days=90)
#     Date.append([sdate,pt])
#     sdate=pt
#
# flatten = lambda l: [item for sublist in l for item in sublist]
# # converting the date as string
# P=flatten(Date)
# P=[i.strftime('%Y-%m') for i in P]
# K=[]
# for i in range(0, m.ceil(len(P)/2)):
#     a= P[:2]
#     K.append(a)
#     P=P[2:]

# L=['Aug-15','Sep-15','Oct-15','Nov-15','Dec-15','Jan-16','Feb-16','Mar-16','Apr-16','May-16','Jun-16','Jul-16',
# 'Aug-16','Sep-16','Oct-16','Nov-16','Dec-16','Jan-17','Feb-17','Mar-17','Apr-17','May-17','Jun-17','Jul-17']
# # L=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]

# P=[]
# for i in range(0,month):
#     pt=sdate + timedelta(days=30)
#     P.append([sdate,pt])
#     sdate=pt
#
# print(P)


import datetime
from datetime import date, timedelta

sdate = date(2013, 1, 1)   # start date
edate = date(2020, 1, 1)   # end date
delta = edate - sdate
year=(delta/365).days

Date=[]
for i in range(0,year):
    if i==3:
        pt=sdate + timedelta(days=366)
    else:
        pt=sdate + timedelta(days=365)
    Date.append([sdate,pt])
    sdate=pt

K=[Date[i][0].year for i in range(0,len(Date))]



######setting up the app
import os
DASH_APP_NAME = 'dash-lineplot'
DASH_APP_PRIVACY = 'public'
PATH_BASED_ROUTING = True
os.environ['PLOTLY_USERNAME'] = 'n2jalali'
os.environ['PLOTLY_API_KEY'] = 'U0HbiPxFhLv32E60m7M4'
os.environ['PLOTLY_DOMAIN'] = 'https://chart-studio.plot.ly/~n2jalali'
os.environ['PLOTLY_API_DOMAIN'] = os.environ['PLOTLY_DOMAIN']
PLOTLY_DASH_DOMAIN='https://chart-studio.plot.ly/~n2jalali'
os.environ['PLOTLY_SSL_VERIFICATION'] = 'True'


app = dash.Dash(__name__)
server = app.server
app.config.suppress_callback_exceptions = True


if 'DYNO' in os.environ:
    app_name = os.environ['DASH_APP_NAME']

else:
#     app = JupyterDash('dash-lineplot/')
    app_name='dash-lineplot/'



app.layout = html.Div([html.Div([html.H1("Average Hotel Review per Day")], style={'textAlign': "center"}),
                       html.Div([dcc.Dropdown(id="selected-value", multi=False,
                                              options=[ { "label": i ,"value": i} for i in K])]),
                       html.Div([dcc.Graph(id="my-graph")])
                       # html.Div([dcc.Graph(id="my-graph2")])
                       ])


@app.callback(
    Output('my-graph', 'figure'),

    [Input('selected-value', 'value')])
def update_figure(selected):
#     for type in selected:
    print("<{}> is selected in the Dropdown menu".format(selected))
    if selected is None:
        index = 0
    else:
        index=K.index(selected)

    # dt=df[index]
    import pandas as pd
    dd=df[(df.Review_Date>=Date[index][0]) & (df.Review_Date<Date[index][1])]
    dr=dd[['Review_Date','Reviewer_Score']]
    dr = dr.set_index('Review_Date')
    dr.Reviewer_Score=[int(i) for i in dr.Reviewer_Score]
    dr=pd.DataFrame(dr.groupby(['Review_Date'])['Reviewer_Score'].mean())
    dr=pd.DataFrame({'Date':dr.index,'Score':dr.Reviewer_Score/10})
    # print(dr.columns)
    from sklearn.model_selection import train_test_split
    colnames=['Document_No','sum','Review_Date']
    dnew=dd.drop(colnames,axis=True)
    x_column=[i  for i in dnew.columns if i!="Reviewer_Score"]
    y = dnew.Reviewer_Score
    X = pd.DataFrame(dnew, columns = x_column)
    np.random.seed(seed = 42)
    # X['random'] = np.random.random(size = len(X))
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size = 0.8, random_state = 42)

    from sklearn.metrics import r2_score
    from rfpimp import permutation_importances
    from sklearn.ensemble import RandomForestRegressor

    rf = RandomForestRegressor(n_estimators = 100,
                               n_jobs = -1,
                               oob_score = True,
                               bootstrap = True,
                               random_state = 42)

    rf.fit(X_train, y_train)

    def r2(rf, X_train, y_train):
        return r2_score(y_train, rf.predict(X_train))

    model=permutation_importances(rf, X_train, y_train, r2)
    model=pd.DataFrame(model)
    print(model.index)
    import lime
    import lime.lime_tabular

    explainer = lime.lime_tabular.LimeTabularExplainer(X_train.values,
                                                       mode = 'regression',
                                                       feature_names = X_train.columns,
                                                       categorical_features = [8],
                                                       categorical_names = ['CHAS'],
                                                       discretize_continuous = True)

    np.random.seed(42)
    for i in range(0,2):
            exp = explainer.explain_instance(X_valid.values[i], rf.predict, num_features = len(x_column))
            exp.show_in_notebook(show_all=True)



    from datetime import datetime

    x= list(set(dr.Date))
    # x=sorted([str(i)for i in  x])

    x=sorted([i.strftime("%Y-%m") for i in  x])
    y=list(dr.Score)
    fig = go.Figure()




    # fig = go.Figure(make_subplots(rows=1, cols=2))
    #
    # fig.add_trace(
    # go.Scatter(
    #
    #     x=x,
    #     y=y,
    #
    #     line_color='rgb(0,176,246)',
    #     showlegend=False,
    #     name='average rating'
    #
    # ),
    # row=1, col=1)
    #
    # fig.add_trace(
    #
    #     go.Scatter(
    #
    #         x=x,
    #         y=y,
    #
    #         line_color='rgb(0,176,246)',
    #         showlegend=False,
    #         name='average rating'
    #
    #     ),
    #     row=1, col=2)
    #
    # fig.update_layout(height=600, width=800, title_text="Subplots")
    # fig.show()


    traces = []


    traces.append(go.Scatter(
    # fig.add_trace(go.Scatter(
        x=x,
        y=y,
#	mode='lines',
        #fill='tozerox',
        #fillcolor='rgba(0,100,80,0.2)',
        line_color='rgb(0,176,246)',
        showlegend=False,
        name='average rating'

        # yaxis={"title": "Temperature ( degree Farenheit )"},
        # xaxis={"title": "Time"}

    ))
    trace2=[]
    traces.append(
    # fig.add_trace(
    {
      "fill": "toself",
      "type":"bar",
      "mode": "markers+lines",
      "name": "Feature importance",
      "r":list(model.Importance),
      "type": "scatterpolar",
      # "x1":list(model.Importance),
      # "y1":list(model.index),

      "marker": {"size": 5, "colorscale": "Viridis"},
       # "orientation": "h",
      "theta":list(model.index)

    })

    fig.update_layout(height=600, width=600, title_text="Stacked subplots")



    return {"data": traces,
    # "data": traces,
            "layout": go.Layout(title="Feature importance", colorway=['#fdae61', '#abd9e9', '#2c7bb6'])}
                                # yaxis={"title": "Temperature ( degree Farenheit )"}, xaxis={"title": "Time"})}



if __name__ == '__main__':

    app.run_server(debug=True,port=8059,host="0.0.0.0")
