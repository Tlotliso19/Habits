from dash import Dash, dash,dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc

""" modules to help with objects and sql operations """
##important modules 
import sqlite3 # for data recording 
import calendar # for time and take 
from datetime import datetime,timedelta # for time and take
import pickle # for serialization 

""" modules for objects and functions for sqlite """
#importing of objects 
from habit_objects import Habits_101,Good_habits_101,serialize_object,deserialize_object

#importing of functions 
from sqlite_101 import database_connect,save_object_to_db,load_object_from_db1,delete_habit_from_database,select_all
'''connect to the database'''
database_connect()

habits=select_all('habits')
## NAVBAR 


nav = dbc.Nav(
    [
        dbc.NavLink("Analyse", active=True , style={"marginRight": "100px"},className="text-primary",id='analyse'),
        dbc.NavLink("Add Habit" , style={"marginRight": "100px"},className="text-success",id='add_habit'),  
        dbc.NavLink("More", style={"marginRight": "100px"},className="text-info"),
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

            dbc.Col(dbc.Button("Submit",id="submit_btn", color="primary"), width="auto"),

    
])

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(children=[html.H1('Habit App',style={"textAlign":"center"}, className="text-primary"),
                                   dbc.Col(   nav , class_name="d-flex justify-content-center"),
                     html.Div(form,id="form",n_clicks=0),
                     html.Div(id="form_message"),html.Div(table,id='table',n_clicks=0),
                      html.Div(options,id='my_select_container'),html.Div(id="form_message1"),
                    
                     ]),



@callback(
    Output('form_message', 'children'),
    Input('submit_btn', 'n_clicks'),
    State('habit_name', 'value'),
    State('habit_frequency', 'value'),
   
)
def collect_habits(n_clicks,name,frequency):
    if n_clicks:
        if name and frequency:
            a=Good_habits_101(name,frequency)
            save_object_to_db(a)

        return "habit saved good luck"
    
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

##call back for the drop down on delete
@callback(
    Output('form_message1', 'children'),
    Input('my-select', 'value'),)

def show_selected(children):
    if children:
        a=delete_habit_from_database(children)
        return a



if __name__ == '__main__':
    app.run(debug=True)



                

