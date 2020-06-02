#!/usr/bin/python3
# -*- encoding: utf-8 -*-

# @author     Raúl Caro Pastorino
# @email      dev@fryntiz.es
# @web        https://fryntiz.es
# @gitlab     https://gitlab.com/fryntiz
# @github     https://github.com/fryntiz
# @twitter    https://twitter.com/fryntiz
# @telegram   https://t.me/fryntiz

# Create Date: 2020/06/01
# Project Name:
# Description:
#
# Dependencies:
#
# Revision 0.01 - File Created
# Additional Comments:

# @copyright  Copyright © 2020 Raúl Caro Pastorino
# @license    https://wwww.gnu.org/licenses/gpl.txt

# Copyright (C) 2020  Raúl Caro Pastorino
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

# Guía de estilos aplicada: PEP8

# #           Descripción           # #
# Ejemplo de uso para la librería, mostrará humedad, temperatura, presión y gas.

from time import sleep
from BME680 import BME680
from BME680_air_quality import BME680_air_quality
from BME680_humidity import BME680_humidity
from BME680_pressure import BME680_pressure
from BME680_temperature import BME680_temperature

#bme680 = BME680(primary=False, mode_debug=True, calibrate=True)
#sleep(2)
air_quality = BME680_air_quality(primary=False, mode_debug=True, calibrate=True)
sleep(2)
humidity = BME680_humidity(primary=False, mode_debug=True)
sleep(2)
pressure = BME680_pressure(primary=False, mode_debug=True)
sleep(2)
temperature = BME680_temperature(primary=False, mode_debug=True)
sleep(2)

try:
    while True:
        #print('Debug Clase Padre')
        #bme680.debug()

        sleep(3)
        print('')

        print('Debug de cada Clase Hija')

        air_quality.debug()

        sleep(1)

        humidity.debug()

        sleep(1)

        pressure.debug()

        sleep(1)

        temperature.debug()

        sleep(10)

except KeyboardInterrupt:
    pass
