# import json
#
# from weather_forecast import Forecast
# from weather_logic import Logic
# from weather_graphics import Graphics
# from weather_site.weather_graphics import Graphics
# graph = Graphics({'error':'error'})
# print(graph.get_cities())
city = ['q','w','z','e']
city.pop(0)
city.pop(0)
print(city)

# forecast = Forecast('Moscow','London')
# forecast.get_data_start()
# forecast.get_data_end()
# data = forecast.get_all_data()
# message = forecast.get_scpecific('Moscow',4)
# print(data)
# print(message)
# logic = Logic(data)
# print(logic.get_res('Moscow',3))
# forecast.get_data('Omsk')
# data = forecast.get_all_data()
# message = forecast.get_scpecific('Moscow',2)
# print(data)
# print(message)
# logic = Logic(data)
# print(logic.get_res('Omsk',1))
# forecast.get_data('Tomsk')
# with open('data.json','r') as f:
#     data = json.load(f)

#
# start_city = 'Dubai'
# end_city = 'Moscow'
# day = 3
# forecast = Forecast(start_city, end_city)
# forecast.get_data_start()
# forecast.get_data_end()
# logic = Logic(forecast.get_all_data())
# start_color, start_res = logic.get_res(start_city,day)
# end_color, end_res = logic.get_res(end_city,day)
# start_weather = forecast.get_scpecific(start_city,day)
# end_weather = forecast.get_scpecific(end_city,day)


# graph = Graphics(data,list(data.keys()))
# fig = graph.create_map(1)
#
# import dash
# from dash import dcc, html
# import dash_bootstrap_components as dbc
#
#
#
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# app.layout = dbc.Container([
#     html.H1('Дашборд данных ирисов', className='text-center text-primary mb-4'),
#     dbc.Row([
#         dbc.Col(dcc.Graph(id='scatter-graph',figure=fig), md=12)
#     ]),
# ], fluid=True)
# if __name__ == '__main__':
#     app.run_server(debug=True)