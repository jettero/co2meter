# coding: utf-8

import click
import simplejson as json
import time

from co2meter.obj import CO2meter

DT_FORMAT = '%Y-%m-%d %H:%M:%S %Z'

class MeterOutput:
    def __init__(self, output):
        self.dtime, self.co2, self.temp = output
        self.dtime = self.dtime.astimezone()

    @property
    def as_text(self):
        return f'{self.dtime:{DT_FORMAT}} {self.temp:2.0f}C {self.co2}ppm'

    @property
    def as_json(self):
        return json.dumps({'_time':f'{self.dtime:{DT_FORMAT}}',
            'temp':self.temp, 'CO₂':self.co2}, ensure_ascii=False)

@click.command()
@click.option('-j', '--json', is_flag=True, default=False)
@click.option('-c', '--continuous', is_flag=True, default=False)
@click.option('-f', '--frequency', type=int, default=60)
def co2meter(json, continuous, frequency):
    if frequency < 10:
        print("NOTE: it can take 10 or 15 seconds to get a reading from the instrument,\n"
            f"      so -f {frequency} may be a little aggressive.")
    cobj = CO2meter()
    last = 0
    while True:
        now = time.time()
        if now - last >= frequency:
            last = now
            mo = MeterOutput( cobj.read_data() )
            if json:
                print( mo.as_json )
            else:
                print( mo.as_text )
            if not continuous:
                break
        else:
            time.sleep(0.3)

def run():
    co2meter()
