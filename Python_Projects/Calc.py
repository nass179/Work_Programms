import math


def absolute_humidity(relative_luftfeuchtigkeit, temperatur, luftdruck):
    saettigungsdampfdruck = 6.1078 * math.pow(10, ((7.5 * temperatur) / (237.3 + temperatur)))

    relative_humidity_decimal = relative_luftfeuchtigkeit / 100.0
    abs_humidity = math.pow(10, 5) * (18.016/8314.3) * luftdruck / (temperatur * relative_humidity_decimal)
    abs_humidity = (relative_humidity_decimal * saettigungsdampfdruck) / (
            0.62198 * (luftdruck - (relative_humidity_decimal * saettigungsdampfdruck)))

    return abs_humidity
