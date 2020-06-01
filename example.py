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

# Copyright (C) 2019  Raúl Caro Pastorino
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
# Ejemplo de uso para la librería, mostrará el índice de CO2 y TVOC en el aire.

from time import sleep
from CJMCU811 import B
from CJMCU811_eco2 import CJMCU811_eco2
from CJMCU811_tvoc import CJMCU811_tvoc

cjmcu811 = CJMCU811()
cjmcu811_eco2 = CJMCU811_eco2()
cjmcu811_tvoc = CJMCU811_tvoc()

# Variables para simular variación de humedad y temperatura.
humidity = 60 #int
temperature = 25.0 #float

sleep(2)

while True:
    try:
        print('Debug Clase Padre')
        cjmcu811.set_temperature_humidity(humidity, temperature)
        cjmcu811.debug()
        sleep(3)
        print('')
        print('Debug de cada Clase Hija')
        cjmcu811_eco2.debug()
        sleep(3)
        cjmcu811_tvoc.debug()
        sleep(3)
        print('')
    except:
        print('>>>>>>>>>>>> | <<<<<<<<<<<<')
        print('Ha ocurrido un error y se reiniciará el sensor')
        #cjmcu811.sensor.reset()
        print('Esperando 30 segundos antes de continuar')
        print('>>>>>>>>>>>> | <<<<<<<<<<<<')
        sleep(30)
