import plotly.express as px
import pandas as pd
import os


class Graphics():

    def __init__(self,data):
        self.data = data
        self.df = None
        self.cities = list(self.data.keys())
        self.template = {'layout': {'width': 800,'height': 350,'plot_bgcolor': '#E5ECF6','font': {'color': 'black'},}}

    def update_data(self,data):
        self.data = data

    def get_cities(self):
        self.cities = list(self.data.keys())
        return self.cities

    def concat_df_on_day(self, data):
        new_data = pd.DataFrame({
            'day': data[0],
            'info': data[1],
            'type': data[2]
        })
        self.df = pd.concat([self.df, new_data], ignore_index=True)

    def concat_df_on_city(self,data):
        new_data = pd.DataFrame({
            'city' : data[0],
            'info' : data[1]
        })
        self.df = pd.concat([self.df,new_data],ignore_index=True)

    def fix_data_on_day(self, city, parametr):
        days = []
        need_data = []
        groups = []
        for day, values in self.data[city].items():
            days.append(values["day"])
            need_data.append(values[parametr])
            groups.append(parametr)
        data = [days, need_data, groups]
        self.concat_df_on_day(data)

    def fix_data_on_city(self,day,parametr):
        cities = list(self.data.keys())
        cities.append(cities[1])
        cities.pop(1)
        need_data = []
        for city in cities:
            need_data.append(self.data[city][f"Day {day}"][parametr])
        data = [cities,need_data]
        self.concat_df_on_city(data)

    def create_bargraph(self,day,parametr,y_title,lim):
        self.df = pd.DataFrame({'city': pd.Series(dtype='str'),
                                'info': pd.Series(dtype='float')
                                })
        self.fix_data_on_city(day,parametr)
        fig = px.bar(self.df, x='city', y='info',
                     labels={'info': y_title, 'city': 'Город'},
                     title=f"График {parametr} на {day} день в разных городах")
        fig.update_layout(yaxis_range=lim)
        return fig

    def create_linegraph(self, city, parametrs,y_title):
        self.df = pd.DataFrame({'day': pd.Series(dtype='int'),
                                'info': pd.Series(dtype='float'),
                                'type': pd.Series(dtype='str')})
        for parametr in parametrs:
            self.fix_data_on_day(city, parametr)
        fig = px.scatter(self.df,
                              x='day',
                              y='info',
                              color='type',
                              labels={'info': 'Температура', 'day': 'День'})

        line_traces = px.line(self.df,
                              x='day',
                              y='info',
                              color='type').data

        for line_trace in line_traces:
            line_trace.showlegend = False
            fig.add_trace(line_trace)

        fig.update_layout(title=f"График изменения погоды для {city}",
                               xaxis_title='День',
                               yaxis_title=y_title)
        fig.update_layout(yaxis_range=[-30,40])
        return fig

    def create_map(self,day):
        cities = list(self.data.keys())
        lats = []
        lons = []
        temps = []
        humis = []
        wind_speed = []
        size = []
        for city in cities:
            size.append(100)
            lat = self.data[city][f"Day {day}"]['lat']
            lon = self.data[city][f"Day {day}"]['lon']
            avg_temperature = round(((self.data[city][f"Day {day}"]['min_temperature']+self.data[city][f"Day {day}"]['max_temperature'])/2),1)
            humi = self.data[city][f"Day {day}"]['humidity']
            wind = self.data[city][f"Day {day}"]['wind_speed']
            lats.append(lat)
            lons.append(lon)
            temps.append(avg_temperature)
            humis.append(f"{humi}%")
            wind_speed.append(f"{wind} км/ч")
        df = pd.DataFrame({
            'Город': cities,
            'lat': lats,
            'lon': lons,
            'Средняя температура': temps,
            'Влажность' : humis,
            'Скорость ветра' : wind_speed,
            'size' : size
        })

        map = px.scatter_mapbox(df, lat='lat', lon='lon', hover_name='Город',
                                color='Средняя температура',size='size',hover_data={'Средняя температура': True, 'Влажность': True,'Скорость ветра' : True, 'lat': False,'lon': False,'size':False},
                                zoom=3, height=800, mapbox_style='open-street-map')

        return map
