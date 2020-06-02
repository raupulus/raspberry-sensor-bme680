#!/usr/bin/python3
# -*- encoding: utf-8 -*-

# @author     Raúl Caro Pastorino
# @email      dev@fryntiz.es
# @web        https://fryntiz.es
# @gitlab     https://gitlab.com/fryntiz
# @github     https://github.com/fryntiz
# @twitter    https://twitter.com/fryntiz
# @telegram   https://t.me/fryntiz

# Create Date: 2020
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
# Modelo que implementa las clases básicas para todos los sensores y asegurar
# de esta forma que funciona la aplicación al cargarlos dinámicamente.


import bme680
import datetime
import time


class BME680:
    table_name = 'table_weather'
    sensor = None

    # Set the humidity baseline to 40%, an optimal indoor humidity.
    # Outdoor → 50%
    hum_baseline = 50.0

    # This sets the balance between humidity and gas reading in the
    # calculation of air_quality_score (25:75, humidity:gas)
    hum_weighting = 0.25


    # TODO → Tomar 50 muestras al iniciar y añadir ese valor aquí,
    # quitarlo de funciones para resistencia y calidad de aire.
    # https://github.com/pimoroni/bme680-python/blob/master/examples/indoor-air-quality.py
    gas_baseline = 250000.00

    def __init__(self, primary=True):
        # Instanciando sensor.
        if primary:
            self.sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        else:
            self.sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

        # Calibrando datos
        self.calibrate_sensor()

        # Configurando datos
        # These oversampling settings can be tweaked to change the balance
        # between accuracy and noise in the data.

        self.sensor.set_humidity_oversample(bme680.OS_2X)
        self.sensor.set_pressure_oversample(bme680.OS_4X)
        self.sensor.set_temperature_oversample(bme680.OS_8X)
        self.sensor.set_filter(bme680.FILTER_SIZE_3)
        self.sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

        # Lectura inicial de todos los datos
        print('\nBME680 → Lectura inicial:')
        for name in dir(self.sensor.data):
            value = getattr(self.sensor.data, name)

            if not name.startswith('_'):
                print('{}: {}'.format(name, value))

        # Estableciendo perfiles
        print('\nBME680 → Estableciendo perfiles:')
        self.sensor.set_gas_heater_temperature(320)
        self.sensor.set_gas_heater_duration(150)
        self.sensor.select_gas_heater_profile(0)

    def calibrate_sensor(self):
        """
        Calibra el sensor.
        :return:
        """
        sensor = self.sensor

        print('\nBME680 → Calibrando sensor:')

        for name in dir(self.sensor.calibration_data):

            if not name.startswith('_'):
                value = getattr(self.sensor.calibration_data, name)

                if isinstance(value, int):
                    print('{}: {}'.format(name, value))

    def read_temperature(self):
        """
        Devuelve la lectura de la temperatura.
        :return: Float|None
        """
        if self.sensor.get_sensor_data():
            return self.sensor.data.temperature

        return None

    def read_pressure(self):
        """
        Devuelve la lectura de la presión.
        :return: Float|None
        """
        if self.sensor.get_sensor_data():
            return self.sensor.data.pressure

        return None

    def read_humidity(self):
        """
        Devuelve la lectura de la humedad.
        :return: Float|None
        """
        if self.sensor.get_sensor_data():
            return self.sensor.data.humidity

        return None

    def read_gas_resistance(self):
        """
        Devuelve la lectura de la resistencia a gases.
        :return: Float|None
        """
        time.sleep(0.2)
        if self.sensor.get_sensor_data() and self.sensor.data.heat_stable:
            gas_resistance = self.sensor.data.gas_resistance

            # Actualizo el valor del gas base como referencia
            if gas_resistance > self.gas_baseline:
                self.gas_baseline = gas_resistance

            return gas_resistance

        return None

    def air_quality(self):
        """
        Devuelve la lectura de la resistencia a gases y devuelve la calidad
        en porcentaje del 1-100%.
        :return: Float|None
        """

        time.sleep(0.2)

        if self.sensor.get_sensor_data() and self.sensor.data.heat_stable:
            gas = self.sensor.data.gas_resistance

            # Actualizo el valor del gas base como referencia
            if gas > self.gas_baseline:
                self.gas_baseline = gas

            gas_offset = self.gas_baseline - gas

            hum = self.sensor.data.humidity
            hum_offset = hum - self.hum_baseline

            # Calculate hum_score as the distance from the hum_baseline.
            if hum_offset > 0:
                hum_score = (100 - self.hum_baseline - hum_offset)
                hum_score /= (100 - self.hum_baseline)
                hum_score *= (self.hum_weighting * 100)

            else:
                hum_score = (self.hum_baseline + hum_offset)
                hum_score /= self.hum_baseline
                hum_score *= (self.hum_weighting * 100)

            # Calculate gas_score as the distance from the gas_baseline.
            if gas_offset > 0:
                gas_score = (gas / self.gas_baseline)
                gas_score *= (100 - (self.hum_weighting * 100))

            else:
                gas_score = 100 - (self.hum_weighting * 100)

            # Calculate air_quality_score.
            air_quality_score = hum_score + gas_score

            return air_quality_score

        return None

    def get_all_data(self):
        """
        Devuelve un diccionario con todas las lecturas si se han podido tomar.
        :return:
        """
        if self.sensor.get_sensor_data() and self.sensor.data.heat_stable:
            return {
                "temperature": self.sensor.data.temperature,
                "pressure": self.sensor.data.pressure,
                "humidity": self.sensor.data.humidity,
                "gas_resistance": self.sensor.data.gas_resistance,
                "air_quality": self.air_quality()
            }

        return None

    def tablemodel(self):
        """
        Plantea campos como modelo de datos para una base de datos y poder ser
        tomados desde el exterior.
        """
        return {
            'temperature': {
                'type': 'Numeric',
                'params': {
                    'precision': 15,
                    'asdecimal': True,
                    'scale': 4
                },
                'others': None,
            },
            'pressure': {
                'type': 'Numeric',
                'params': {
                    'precision': 15,
                    'asdecimal': True,
                    'scale': 4
                },
                'others': None,
            },
            'humidity': {
                'type': 'Numeric',
                'params': {
                    'precision': 15,
                    'asdecimal': True,
                    'scale': 4
                },
                'others': None,
            },
            'gas_resistance': {
                'type': 'Numeric',
                'params': {
                    'precision': 22,
                    'asdecimal': True,
                    'scale': 11
                },
                'others': None,
            },
            'air_quality': {
                'type': 'Numeric',
                'params': {
                    'precision': 15,
                    'asdecimal': True,
                    'scale': 4
                },
                'others': None,
            },
            'created_at': {
                'type': 'DateTime',
                'params': None,
                'others': {
                    'default': datetime.datetime.utcnow
                },
            },
        }

    def debug(self):
        """
        Función para depurar funcionamiento del modelo proyectando datos por
        consola.
        """
        datas = self.get_all_data()

        if datas:
            print('Pintando debug para BME680')

            for sensor, data in datas.items():
                print('Valor del sensor ' + str(sensor) + ': ' + str(data))

