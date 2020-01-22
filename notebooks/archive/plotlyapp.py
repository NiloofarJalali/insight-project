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

############### Loading the file
with open('./Heatwaves/mylist','rb') as f:
        df=pickle.load(f,encoding='latin1')



sdate = date(2018, 6, 1)   # start date
edate = date(2018, 8, 31)   # end date

delta = edate - sdate
Date=[]
for i in range(delta.days + 1):
    day = sdate + timedelta(days=i)
    Date.append(day)

Date=[i.strftime('%Y-%m-%d') for i in Date]


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



app.layout = html.Div([html.Div([html.H1("Comparing the Indoor Temprature of Households with/without AC")], style={'textAlign': "center"}),
                       html.Div([dcc.Dropdown(id="selected-value", multi=False,
                                              options=[ { "label": i ,"value": i} for i in Date])]),
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
        index=Date.index(selected)
    
    dt=df[index]

    
    dt_lower=dt[dt.value=="Min"]
    dt_higher=dt[dt.value=="Max"]
    dt_med= dt[dt.value=="Average"]
#    print(list(zip(dt_lower.Temp, dt_med.Temp, dt_higher.Temp)))
    y1_low=list(dt_lower[dt_lower.status=="AC"]['Temp'])
    y1_low=y1_low[::-1]
    y2_low=list(dt_lower[dt_lower.status=="noAC"]['Temp'])
    y2_low=y2_low[::-1]
    y1_high=list(dt_higher[dt_higher.status=="AC"]['Temp'])
    y2_high=list(dt_higher[dt_higher.status=="noAC"]['Temp'])
    y1=list(dt_med[dt_med.status=="AC"]['Temp'])
    y2=list(dt_med[dt_med.status=="noAC"]['Temp'])
    #y1=dt[dt.status=="AC"]['Temp']
    #y2=dt[dt.status=="noAC"]['Temp']
    #yac=dt[dt.status=="AC"]['Temp']
    #ynoac=dt[dt.status=="noAC"]['Temp']
    import datetime
    x= set(dt.index)
    x=sorted([i.strftime("%H:%M:%S") for i in  x])
    x_rev=x[::-1]
    
    # print(list(zip(x, y1_low+y1_high)))
    fig = go.Figure()
    traces = []

    traces.append(go.Scatter(
    	x=x+x_rev,
        y=y1_low+y1_high,
        fill='toself',
        fillcolor='rgba(0,176,246,0.2)',
        line_color='rgba(255,255,255,0)',
        showlegend=False,
        name='AC',
   ))
    traces.append(go.Scatter(
        x=x,
        y=y1,
#	mode='lines',
        #fill='tozerox',
        #fillcolor='rgba(0,100,80,0.2)',
        line_color='rgb(0,176,246)',
        showlegend=False,
        name='AC',
    ))
    traces.append(go.Scatter(
        x=x+x_rev,
        y=y2_low+y2_high,
    	fill='toself',
        fillcolor='rgba(231,107,243,0.2)',
        line_color='rgba(255,255,255,0)',
        showlegend=False,
        name='noAC',
    ))
   
    traces.append(go.Scatter(
        x=x,
        y=y2,
#	mode='lines',
#        fill='tozerox',
        #fillcolor='rgba(0,176,246,0.2)',
        line_color='rgb(231,107,243)',
        name='noAC',
        showlegend=False,
    ))

    #traces.append(go.Scatter(
     #   x=x,
     #   y=y2_high,
     #   fill='toself',
     #   fillcolor='rgba(0,176,246,0.2)',
     #   line_color='rgba(255,255,255,0)',
     #   showlegend=False,
      #  name='noAC',
    #))



#    traces.append(go.Scatter(
 #       x=x, y=y1,
 #       line_color='rgb(0,100,80)',
 #       name='AC',
 #   ))
 #   traces.append(go.Scatter(
 #       x=x, y=y2,
 #       line_color='rgb(0,176,246)',
 #       name='noAC',
 #   ))

    # fig.update_traces(mode='lines')
######################    fig.show()

    # trace = []
    # trace.append(go.Scatter(x=dt.index, y=dt.Temp, name=dt.status, mode='lines',
    #                             marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}}, ))
    return {"data": traces,
            "layout": go.Layout(title="Temperature Variations Over Time", colorway=['#fdae61', '#abd9e9', '#2c7bb6'],
                                yaxis={"title": "Temperature ( degree Farenheit )"}, xaxis={"title": "Time"})}



if __name__ == '__main__':
  
    app.run_server(debug=True,port=8049,host="0.0.0.0")
