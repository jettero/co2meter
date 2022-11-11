# coding: utf-8

import click
import simplejson as json
import time

from jco2meter.obj import CO2meter

DT_FORMAT = "%Y-%m-%d %H:%M:%S %Z"


class MeterOutput:
    def __init__(self, output, **add):
        self.dtime, self.co2, self.temp = output
        self.dtime = self.dtime.astimezone()
        self._add = add

    def add(self, **x):
        self._add.update(x)

    @property
    def as_text(self):
        return f"{self.dtime:{DT_FORMAT}} {self.temp:2.0f}C {self.co2}ppm"

    @property
    def as_json(self):
        dat = {"_time": f"{self.dtime:{DT_FORMAT}}", "temp": self.temp, "CO₂": self.co2}
        dat.update(self._add)
        return json.dumps(dat, ensure_ascii=False)


@click.command()
@click.option("-v", "--verbose", is_flag=True, default=False)
@click.option("-j", "--json", is_flag=True, default=False)
@click.option("-c", "--continuous", is_flag=True, default=False)
@click.option("-f", "--frequency", type=int, default=60)
def jco2meter(json, continuous, frequency, verbose):
    if frequency < 10:
        print(
            "NOTE: it can take 3-5 seconds to get a reading from the instrument,\n"
            f"      so -f {frequency} may be a little aggressive."
        )
    if verbose:
        print("# connecting")
    cobj = CO2meter()

    if verbose:
        print("# connected {vendor_id}:{product_id} {manufacturer} {product_name} {serial_no}".format(**cobj.info))

    last = 0
    while True:
        now = time.time()
        if now - last >= frequency:
            if verbose:
                print("# reading")
            last = now
            mo = MeterOutput(cobj.read_data())
            mo.add(dt=time.time() - now)
            if json:
                print(mo.as_json)
            else:
                print(mo.as_text)
            if not continuous:
                break
        else:
            time.sleep(0.3)


def run():
    jco2meter()
