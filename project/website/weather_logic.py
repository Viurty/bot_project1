class Logic():

    def __init__(self,data):
        self.data = data

    def update_data(self,new_data):
        self.data = new_data

    def check_temperature(self,place,day):
        if self.data[place][f"Day {day}"]["min_temperature"] > 10 and self.data[place][f"Day {day}"]["max_temperature"] < 30:
            return True
        else:
            return False

    def check_humidity(self,place,day):
        if 30 < self.data[place][f"Day {day}"]['humidity'] < 70:
            return True
        else:
            return False

    def check_wind(self,place,day):
        if self.data[place][f"Day {day}"]['wind_speed'] < 25:
            return True
        if self.data[place][f"Day {day}"]['wind_speed'] >50:
            return f'Небезопасно, в городе штормовый ветер'
        return False

    def check_probability(self,place,day):
        if max(self.data[place][f"Day {day}"]['probability_snow'],self.data[place][f"Day {day}"]['probability_rain']) < 50:
            return True
        else:
            return False
    def get_res(self,city,day):
        temp = self.check_temperature(city,day)
        humi = self.check_humidity(city,day)
        wind = self.check_wind(city,day)
        if not str(wind) in ['True', "False"]:
            return 'red', wind
        prob = self.check_probability(city,day)
        if not temp or not prob:
            return 'red', 'Неблагоприятная погода'
        elif not humi or not wind:
            return 'yellow', 'Удоволетворительная погода'
        else:
            return 'green', 'Отличная погода'

def days(day):
    if day == 1:
        return '1 день'
    elif day in [2,3,4]:
        return f'{day} дня'
    else:
        return '5 дней'




