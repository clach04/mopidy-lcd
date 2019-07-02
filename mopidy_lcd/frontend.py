import pykka

from mopidy.core import CoreListener

import RPi_I2C_driver

from ticker import Ticker
from smbus import SMBus
from bme280 import BME280


class LCDFrontend(pykka.ThreadingActor, CoreListener):
    def __init__(self, config, core):
        super(LCDFrontend, self).__init__()

        self.lcd = RPi_I2C_driver.lcd()

        if config['lcd']['display_temperature']:
            bus = SMBus(config['lcd']['bme280_i2c_bus'])
            self.bme280 = BME280(i2c_dev=bus)
        else:
            self.bme280 = None

        self.ticker = Ticker(self.actor_ref, LCDFrontend.TICK_INTERVAL)
        self.ticker.start()

        self.stream_title = ""
        self.st_pos = 0
        self.lifetime = 0
        self.lcd_on = True
        self.volume = 0

    def stream_title_changed(self, title):
        self.stream_title = title
        self.st_pos = 0
        self.turn_on()

    def volume_changed(self, volume):
        self.volume = volume
        self.turn_on()

    def turn_on(self):
        self.lcd_on = True
        self.lifetime = 0

    def turn_off(self):
        self.lcd.backlight(0)
        self.lcd_on = False

    def display(self):
        self.lcd.lcd_display_string("%-16.16s" % (self.stream_title[self.st_pos:],), LCDFrontend.LINE_1)
        self.st_pos = self.st_pos + 16 if self.st_pos + 16 < len(self.stream_title) else 0
        change_time = (self.lifetime / LCDFrontend.CHANGE_DISPLAY_TIME) % 2
        if change_time == 0 or self.bme280 is None:
            self.lcd.lcd_display_string("Volume: %-4d" % (self.volume,), LCDFrontend.LINE_2)
        else:
            temp = self.bme280.get_temperature()
            self.lcd.lcd_display_string("Temp.: %-5.2f" % (temp,), LCDFrontend.LINE_2)

    def tick(self):
        self.lifetime += LCDFrontend.TICK_INTERVAL
        if self.lifetime >= LCDFrontend.MAX_LIFETIME:
            self.turn_off()
            return

        self.display()

    def on_receive(self, message):
        if message.get(Ticker.TICK) and self.lcd_on:
            self.tick()

    LINE_1 = 1
    LINE_2 = 2

    TICK_INTERVAL = 2
    MAX_LIFETIME = 600
    CHANGE_DISPLAY_TIME = 6
