import pykka

from mopidy.core import CoreListener

import RPi_I2C_driver

from ticker import Ticker


class LCDFrontend(pykka.ThreadingActor, CoreListener):
    def __init__(self, config, core):
        super(LCDFrontend, self).__init__()

        self.lcd = RPi_I2C_driver.lcd()

        self.ticker = Ticker(self.actor_ref, LCDFrontend.TICK_INTERVAL)
        self.ticker.start()

        self.stream_title = ""
        self.st_pos = 0
        self.lifetime = 0
        self.lcd_on = True

    def stream_title_changed(self, title):
        self.stream_title = title
        self.st_pos = 0
        self.turn_on()

    def volume_changed(self, volume):
        self.lcd.lcd_display_string("Volume: %-3d" % (volume,), LCDFrontend.LINE_2)
        self.turn_on()

    def turn_on(self):
        self.lcd_on = True
        self.lifetime = 0

    def turn_off(self):
        self.lcd.backlight(0)
        self.lcd_on = False

    def display_stream_title(self):
        self.lcd.lcd_display_string("%-16.16s" % (self.stream_title[self.st_pos:],), LCDFrontend.LINE_1)
        self.st_pos = self.st_pos + 16 if self.st_pos + 16 < len(self.stream_title) else 0

    def tick(self):
        self.lifetime += LCDFrontend.TICK_INTERVAL
        if self.lifetime >= LCDFrontend.MAX_LIFETIME:
            self.turn_off()
            return

        self.display_stream_title()

    def on_receive(self, message):
        if message.get(Ticker.TICK) and self.lcd_on:
            self.tick()

    LINE_1 = 1
    LINE_2 = 2

    TICK_INTERVAL = 2
    MAX_LIFETIME = 600
