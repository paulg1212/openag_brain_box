"""
This module consists of code for interacting with a DS18B20 Temperature sensor.
"""

from w1thermsensor import W1ThermSensor
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('main.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class DS18B20:
    """
    Class that represents a DS18B20 Temperature sensor instance and provides functions
    for interfacing with it.
    """

    def __init__(self, pseudo=False):
        logger.debug('Initializing sensor')
        self.pseudo = pseudo
        self.sensor_is_connected = False
        self.temperature = None
        self.connect()

    def connect(self):
        if self.pseudo:
            logger.info('Connected to sensor')
            return
        try:
            self.sensor = W1ThermSensor()
            if not self.sensor_is_connected:
                self.sensor_is_connected = True
                logger.info('Connected to sensor')
        except:
            if self.sensor_is_connected:
                self.sensor_is_connected = False
                logger.warning('Unable to connect to sensor')

    def poll(self):
        if self.pseudo:
            self.temperature = 21.2
            return
        if self.sensor_is_connected:
            try:
                self.temperature = self.sensor.get_temperature()
            except:
                self.temperature = None
                self.sensor_is_connected = False
        else:
            self.connect()

    def transmitToConsole(self, id='Water Temperature'):
        if self.temperature is not None:
            print(id, ': ', self.temperature, 'C')

    def transmitToMemcache(self, memcache_shared, id='water_temperature'):
        if self.temperature is not None:
            memcache_shared.set(id, '{0:.1f}'.format(self.temperature))
