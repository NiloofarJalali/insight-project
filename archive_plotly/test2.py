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

############### Loading the file

with open("/Users/niloofar/Documents/insight/data/cleaned/hotel1/Final_res",'rb') as f:
        df=pickle.load(f,encoding='latin1')


sdate = date(2015, 8, 3)   # start date
edate = date(2017, 8,4)   # end date
delta = edate - sdate
month=(delta/30).days
L=['Aug-15','Sep-15','Oct-15','Nov-15','Dec-15','Jan-16','Feb-16','Mar-16','Apr-16','May-16','Jun-16','Jul-16',
'Aug-16','Sep-16','Oct-16','Nov-16','Dec-16','Jan-17','Feb-17','Mar-17','Apr-17','May-17','Jun-17','Jul-17']
# L=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]

P=[]
for i in range(0,month):
    pt=sdate + timedelta(days=30)
    P.append([sdate,pt])
    sdate=pt

# print(P)

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
                                              options=[ { "label": i ,"value": i} for i in L])]),
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
        index=L.index(selected)

    # dt=df[index]
    import pandas as pd
    dd=df[(df.Review_Date>=P[index][0]) & (df.Review_Date<P[index][1])]
    dr=dd[['Review_Date','Reviewer_Score']]
    dr=dr.groupby(['Review_Date']).mean()
    dr=pd.DataFrame({'Date':dr.index,'Score':dr.Reviewer_Score})
    print(dr.columns)
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
    print(model)


    import datetime
    x= set(dr.Date)
    x=sorted([i.strftime("%Y-%m-%d") for i in  x])
    y=list(dr.Score)
    # fig = go.Figure()





    fig = go.Figure(make_subplots(rows=2, cols=1))
    # ,     specs=[[{"secondary_y": True}, {"secondary_y": True}],
    #                        [{"secondary_y": True}, {"secondary_y": True}]]))
    traces = []


#     traces.append(go.Scatter(
#     # fig.add_trace(go.Scatter(
#         x=x,
#         y=y,
# #	mode='lines',
#         #fill='tozerox',
#         #fillcolor='rgba(0,100,80,0.2)',
#         line_color='rgb(0,176,246)',
#         showlegend=False,
#         name='average rating'
#
#         # yaxis={"title": "Temperature ( degree Farenheit )"},
#         # xaxis={"title": "Time"}
#
#     ))
    traces.append(
    # fig.add_trace(
    {
      "fill": "toself",
      "mode": "markers+lines",
      "name": "Feature importance",
      "r":list(model.Importance),
      "type": "scatterpolar",
      "marker": {"size": 5},
      "theta":list(model.index)
    })

    fig.update_layout(height=600, width=600, title_text="Stacked subplots")



    return {"data": traces,
    # "data": traces,
            "layout": go.Layout(title="Feature importance", colorway=['#fdae61', '#abd9e9', '#2c7bb6'])}
                                # yaxis={"title": "Temperature ( degree Farenheit )"}, xaxis={"title": "Time"})}



if __name__ == '__main__':

    app.run_server(debug=True,port=8049,host="0.0.0.0")
