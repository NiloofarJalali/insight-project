# import pickle
# from datetime import date, timedelta
# import datetime
# import plotly
# import numpy as np
# import plotly.graph_objs as go
# import chart_studio.plotly as py
# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# import plotly.graph_objs as go
# import dash
# from dash.dependencies import Input, Output
# import dash_html_components as html
# import dash_core_components as dcc
# import seaborn as sns
# import pandas as pd


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


# from sklearn.metrics import r2_score
# from rfpimp import permutation_importances
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.model_selection import train_test_split
# import lime
# import lime.lime_tabular






with open("/Users/niloofar/Documents/insight/data/cleaned/hotel1/Final_res",'rb') as f:
        df=pickle.load(f,encoding='latin1')


sdate = date(2015, 8, 3)   # start date
edate = date(2017, 8,4)   # end date
delta = edate - sdate
month=(delta/30).days
L=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]

P=[]
for i in range(0,month):
    pt=sdate + timedelta(days=30)
    P.append([sdate,pt])
    sdate=pt




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
    app_name='dash-hotelwatch/'



app.layout = html.Div([html.Div([html.H1("Dynamic Hotel Review")], style={'textAlign': "center"}),
                       html.Div([dcc.Dropdown(id="selected period", multi=False,
                                              options=[ { "label": i ,"value": i} for i in L])]),
                       html.Div([dcc.Graph(id="my-graph")])])


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

    dd=df[(df.Review_Date>=P[index][0]) & (df.Review_Date<P[index][1])]
    print(dd)
    # colnames=['Document_No','sum','Review_Date']
    dd=dd.drop(colnames,axis=True)
#     x_column=[i  for i in dd.columns if i!="Reviewer_Score"]
#
#
#     y = dd.Reviewer_Score
#     print(y)
#     X = pd.DataFrame(dd, columns = x_column)
#     print(X)
# #     np.random.seed(seed = 42)
#     # X['random'] = np.random.random(size = len(X))
#
#     def r2(rf, X_train, y_train):
#         return r2_score(y_train, rf.predict(X_train))
#
#
#     X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size = 0.8, random_state = 42)
#
#     rf = RandomForestRegressor(n_estimators = 100,
#                                n_jobs = -1,
#                                oob_score = True,
#                                bootstrap = True,
#                                random_state = 42)
#
#     rf.fit(X_train, y_train)
#     model=permutation_importances(rf, X_train, y_train, r2)
#
#
#
#     explainer = lime.lime_tabular.LimeTabularExplainer(X_train.values,
#                                                        mode = 'regression',
#                                                        feature_names = X_train.columns,
#                                                        categorical_features = [8],
#                                                        categorical_names = ['CHAS'],
#                                                        discretize_continuous = True)
#
#     np.random.seed(42)
#     exp = explainer.explain_instance(X_valid.values[number], rf.predict, num_features = len(x_column))
#     exp.show_in_notebook(show_all=False) #only the features used in the explanation are displayed
#
# #     exp = explainer.explain_instance(X_valid.values[1], rf.predict, num_features = len(x_column))
# #     exp.show_in_notebook(show_all=False)
#
#
#
#     days=dd[Review_Date]
#

    dr=dd[['Review_Date','Reviewer_Score']]
    dr=dr.groupby(['Review_Date']).mean()

    x=np.array(list(dr.index))
    y=np.array(dr.Reviewer_Score)


    fig = go.Figure()
    traces = []
    traces.append(go.Scatter(
        x=x,
        y=y,
        line_color='rgb(0,176,246)',
        showlegend=False,
        name='Day',
    ))


    return {"data": traces,
            "layout": go.Layout(title="Average Review Score per day", colorway=['#fdae61'],
                                yaxis={"title": "Average Score"}, xaxis={"title": "Time"})}



if __name__ == '__main__':

    app.run_server(debug=True,port=8059,host="0.0.0.0")
