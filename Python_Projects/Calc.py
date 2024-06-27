import math


def absolute_humidity(relative_luftfeuchtigkeit, temperatur):
    relative_humidity_decimal = relative_luftfeuchtigkeit / 100.0
    saettigungsdampfdruck = relative_humidity_decimal*6.1078 * math.pow(10, ((7.5 * temperatur) / (237.3 + temperatur)))

    abs_humidity = math.pow(10, 5) * (18.016 / 8314.3) * saettigungsdampfdruck / (
                (temperatur + 273.15))
    #formatted_abs_humidity = "{:.2f}".format(abs_humidity)
    '''abs_humidity = (relative_humidity_decimal * saettigungsdampfdruck) / (
            0.62198 * (luftdruck - (relative_humidity_decimal * saettigungsdampfdruck)))'''

    return abs_humidity #formatted_abs_humidity


# print(absolute_humidity(43.64, 23.37))
