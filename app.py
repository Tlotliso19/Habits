from dash import Dash, dash,dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

""" modules to help with objects and sql operations """
##important modules 
import sqlite3 # for data recording 
import calendar # for time and take 
from datetime import datetime,timedelta # for time and take
import pickle # for serialization 

""" modules for objects and functions for sqlite """
#importing of objects 
from habit_objects import Habits_101,Good_habits_101,serialize_object,deserialize_object,Bad_habits_101

#importing of functions 
from sqlite_101 import database_connect,save_object_to_db,load_object_from_db1,delete_habit_from_database,select_all,update_habit
'''connect to the database'''
database_connect()

habits=select_all('bad_habits')+select_all('good_habits')

##progress bar 
progress_bars=[]
progress_btn=[]
labels=[]
for i in habits:
    color=''
    if isinstance(i[1],Good_habits_101):
        color='blue'
    else:
        color='red'
    values=i[1].display_data()
    value=values[0]+2/values[1]*100
    label=i[1].name
    labels.append(label)
    buttom=dbc.Button(label,style={'height':'30px','display':'inline','backgroundColor':color},id=label) #,color=color
    progress = dbc.Progress(label=label, value=value,color=color,
                            style={"height": "30px","width": "90%","contentJustify": "center"}, className="mb-3")
    progress_bars.append(progress)
    progress_btn.append(buttom)

##progress bar and buttom
components=[]
for i in range(len(progress_bars)):
    component=html.Div([progress_bars[i],progress_btn[i]],style={'display':'grid','gridTemplateColumns':'5fr 1fr'})
    components.append(component)


## NAVBAR 


nav = dbc.Nav(
    [    dbc.NavLink(dcc.Dropdown(id='names',
        options=['Good Habits', 'Bad Habits','All'],
        value='All', clearable=False,style={"marginRight": "100px","width":"200px"},className="text-primary"
    )),
        dbc.NavLink("Analyse", active=True , style={"marginRight": "100px"},className="text-primary",id='analyse'),
        dbc.NavLink("Add Habit" , style={"marginRight": "100px"},className="text-success",id='add_habit'),  
        dbc.NavLink("More", style={"marginRight": "100px"},className="text-info"),
        dbc.NavLink("Daily tasks", style={"marginRight": "100px"},className="text-info",id="daily"),
        dbc.NavLink("Delete" , style={"marginRight": "100px"},className="text-danger",id='delete'),
    ]
)
##TABLE JUST FOR TESTING PEPURSES 

table_header = [
    html.Thead(html.Tr([html.Th("ID"), html.Th("NAME"),html.Th("FREQUENCY"), html.Th("STREAK")]))
]

rows=[]
for i in habits:
    row = html.Tr([html.Td(i[0]), html.Td(i[1].name), html.Td(i[1].frequency), html.Td(i[1].streak)])
    rows.append(row)

#for a dropdown of habits to be shown when delete is pressed 





delete_options=[]
for i in habits:
    row={'label':i[1].name, 'value': i[1].name}
    delete_options.append(row)


""" for the daily taks """
task_rows=[]
for i in habits:
    if i:
        if i[1].performed() !=True:
            task_row= dbc.Row([dbc.Col(
                dbc.Label(i[1].name, width="auto")),
                dbc.Col(
                dbc.Label(str(i[1].performed()), width="auto")),
        
                dbc.Col(dbc.Button("Complete", color="primary",active=True), width="auto",), ] ,
            className="g-2",style={"marginBottom": "20px"})
            task_rows.append(task_row)
        else:
            task_row= dbc.Row([dbc.Col(
                dbc.Label(i[1].name, width="auto")),
                dbc.Col(
                dbc.Label(str(i[1].performed()), width="auto")),
        
                dbc.Col(dbc.Button("Done", color="primary",active=False), width="auto",), ] ,
                className="g-2",style={"marginBottom": "20px"})
            task_rows.append(task_row)
   

    




daily_tasks = dbc.Form( task_rows,style={"width":"40%" })








## the delete options 
options = dcc.Dropdown(
        delete_options,
        
        id='my-select',
        value='running',
        searchable=True
        ,style={'width':"30%"} # Default value
    )

table_body = [html.Tbody(rows)]

table = dbc.Table(table_header + table_body, bordered=True)


form = dbc.Row([
    dbc.Col([   
        dbc.Input(
            type="text",
            id="habit_name",
            placeholder="Habit name",)],className="me-3"),
    dbc.Col([  
        dbc.Input(
            type="text",
            id="habit_frequency",
            placeholder="Habit frequency")],className="me-3"),
dbc.Col(  dcc.RadioItems(
        id='radio-buttons',
        options=[
            {'label': 'Good Habit', 'value': 'good_habit'},
            {'label': 'Bad Habit', 'value': 'bad_habit'}
        ],
        value='option1',  # Default value
        labelStyle={'display': 'block'}  # Display each radio button on a new line
    ),),
            dbc.Col(dbc.Button("Submit",id="submit_btn", color="primary"), width="auto"),

    
])

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(children=[html.H1('Habit App',style={"textAlign":"center"}, className="text-primary"),
                                   dbc.Col(   nav , class_name="d-flex justify-content-center"),
                     html.Div(form,id="form",n_clicks=0),
                     html.Div(id="form_message"),html.Div(table,id='table',n_clicks=0),
                      html.Div(options,id='my_select_container'),html.Div(id="form_message1"),
                     html.Div(components,id="daily_tasks"),html.Div(id='update-habit-output'),
                      html.Div(id="habit analysis",
                               style={'display': 'grid', 'gridTemplateColumns': 'repeat(3, 1fr)', 'gap': '10px', 'padding': '20px'})
                        
                              
                    
                     ]),


##to collect the habit data into the database
@callback(
    Output('form_message', 'children'),
    Input('submit_btn', 'n_clicks'),
    Input('radio-buttons', 'value'),
    State('habit_name', 'value'),
    State('habit_frequency', 'value'),
   
)
def collect_habits(n_clicks,value,name,frequency):
    if value =="good_habit":
        if n_clicks:
            if name and frequency:
                a=Good_habits_101(name,frequency)
                save_object_to_db(a,'good_habits')

            return "habit saved good luck"
    else:
        if n_clicks:
            if name and frequency:
                a=Bad_habits_101(name,frequency)
                save_object_to_db(a,'bad_habits')

            return "habit saved good luck"
##show and hide the table   
@callback(
    Output('table', 'style'),
    Input('analyse', 'n_clicks'),)

def show_table(n_clicks):
    if n_clicks is None:
    #if n_clicks==0:
        return {'display': 'none'}
    
   
        
    if n_clicks % 2 == 1: 
        return {'display': 'block'}
    else:
        return {'display': 'none'}
        
##show the form and hide it 
@callback(
    Output('form', 'style'),
    Input('add_habit', 'n_clicks'),)

def show_form(n_clicks):
    if n_clicks is None:
    #if n_clicks==0:
        return {'display': 'none'}
    
   
        
    if n_clicks % 2 == 1: 
        return {'display': 'block'}
    else:
        return {'display': 'none'}

## to only show the drop down when the delete is pressed
@callback(
    Output('my_select_container', 'style'),
    Input('delete', 'n_clicks'),)

def show_form(n_clicks):
    if n_clicks is None:
    #if n_clicks==0:
        return {'display': 'none'}
    
   
        
    if n_clicks % 2 == 1: 
        return {'display': 'flex', 'justifyContent': 'flex-end','marginRight': '40px'}
    else:
        return {'display': 'none'}
    
    ## to only show the daily tasks when daily habit button is clicked 

  

@callback(
    Output('daily_tasks', 'style'),
    Input('daily', 'n_clicks'),)

def show_form(n_clicks):
    if n_clicks is None:
    #if n_clicks==0:
        return {'display': 'none'}
    
   
        
    if n_clicks % 2 == 1: 
        return {'display': 'block', 'justifyContent': 'center','marginRight': 'auto','marginLeft': '90px'}
    else:
        return {'display': 'none'}



##call back for the drop down on delete
@callback(
    Output('form_message1', 'children'),
    Input('my-select', 'value'),)

def show_selected(value):
    if value:
        a=delete_habit_from_database(value,'good_habits')
        a=delete_habit_from_database(value,'bad_habits')
        return a
       

##callback to deal with the plotting 
@callback(Output("habit analysis","children"),Input("names","value"))

def plot_habits(value):
    habits=[]
    if value == 'Good Habits':
        habits=select_all('good_habits')
    elif value == 'Bad Habits':
        habits=select_all('bad_habits')
    elif value == 'All':
        good_habits=select_all('bad_habits')
        bad_habits=select_all('good_habits')
        habits=bad_habits + good_habits
    graphs=[]
    for i in habits:
        colors=[]
        values=i[1].display_data()
        values=(3,67)
        labels=['current','target']
        if isinstance (i[1],Good_habits_101):
            colors = ['#d62728', '#ffbb78']
        else:
            colors = ['#1f77b4', '#ff7f0e']
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.8, marker=dict(colors=colors))])
        fig.update_layout( 
             annotations=[
                dict(text=i[1].name,font_size=20,showarrow=False)])
        graphs.append(dcc.Graph(figure=fig))
    return graphs


@app.callback(
    Output('update-habit-output', 'children'),
    [Input(f'{i}', 'n_clicks') for i in labels] 
    , [State(label, 'style') for label in labels]
)
def update_output(*args):
    # Determine which button was clicked
    n_clicks = args[:len(labels)]
    styles = args[len(labels):]
    #print(styles)
    for i, click_count in enumerate(n_clicks ):
    
        if click_count is not None:
            #habit_object=load_object_from_db1(labels[i],'bad_habits')
            
            #color1 = styles[i]['KeyError: 'backgroundColor'']
            color = styles[i].get('backgroundColor','unknown')
            if color =='red' and n_clicks!=0:
                
                habit_object=load_object_from_db1(format(labels[i]),'bad_habits')
                if isinstance (habit_object,bad_habits_101):
                    performed_habit=habit_object.perform()
                    update_habit(labels[i],performed_habit,'bad_habits')
                #return f'You clicked {labels[i]} {n_clicks} times! which is number {color} in color'
                    print(habit_object)
            else: 
                
                habit_object=load_object_from_db1(labels[i],'good_habits')
                if isinstance(habit_object,Good_habits_101):
                    performed_habit=habit_object.perform()
                    update_habit(labels[i],performed_habit,'good_habits')
                    print(habit_object)
    return 'Click a button!'



if __name__ == '__main__':
    app.run(debug=True)



                

