import math


def absolute_humidity(relative_luftfeuchtigkeit, temperatur):
    molMassH2O = 18.015  # g/mol
    relative_humidity_decimal = relative_luftfeuchtigkeit / 100.0
    saettigungsdampfdruck = 603.28 * math.exp((17.1485 * 24) / (234.69 + 24))

    abs_humidity = (relative_humidity_decimal * saettigungsdampfdruck * molMassH2O) / (8.314 * (temperatur + 273.15))
    #formatted_abs_humidity = "{:.2f}".format(abs_humidity)
    '''abs_humidity = (relative_humidity_decimal * saettigungsdampfdruck) / (
            0.62198 * (luftdruck - (relative_humidity_decimal * saettigungsdampfdruck)))'''

    return abs_humidity #formatted_abs_humidity


# print(absolute_humidity(43.64, 23.37))
