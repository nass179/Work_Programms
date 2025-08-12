import math

pw = 603.28 * math.exp((17.1485 * 24) / (234.69 + 24))  # Pa
print(pw)
molMassH2O = 18.015  # g/mol
relHum = 0.8  # %
rohW = ((relHum/100) * pw * molMassH2O) / (8.314 * 297.15)
print(rohW)