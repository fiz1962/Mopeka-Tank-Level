#!/usr/bin/python

import asyncio
import struct

from bleak import BleakScanner

timeout_seconds = 30
service_uuids=['0000fee5-0000-1000-8000-00805f9b34fb']
devices=['AA:BB:CC:DD:EE:FF']

tc1=0.573045
tc2=-0.002822
tc3=-0.00000535

def detection_callback(device, advertisement_data):
    if device.address in devices:
        print(device.address, advertisement_data.rssi)
        print(advertisement_data.service_uuids)
        print(advertisement_data.manufacturer_data)
        v_raw = advertisement_data.manufacturer_data[89][1] & 0x7f
        v_volt = v_raw / 32
        v_per  = (v_volt - 2.2)/0.65*100
 
        t_raw = advertisement_data.manufacturer_data[89][2] & 0x7f
        t_c   = t_raw - 40

        l_raw = (advertisement_data.manufacturer_data[89][4] * 256 + advertisement_data.manufacturer_data[89][3]) & 0x3fff
        l_cm  = l_raw * (tc1 + tc2 * t_raw + tc3 * t_raw * t_raw)/10

        reading_quality = advertisement_data.manufacturer_data[89][4] >> 6

        print('Signal quality ', reading_quality)
        print('volts       ', v_raw,'(raw),',round(v_volt,2),'(volts),',round(v_per,2),'(%)')
        print('temperature ', t_raw, '(raw),',round(t_c,2),'(C)')
        print('level       ', l_raw, '(raw),', round(l_cm,2),'(cm)')
        print('')

        devices.remove(device.address)

async def run():
    scanner = BleakScanner(detection_callback=detection_callback, service_uuids=service_uuids)
    await scanner.start()
    await asyncio.sleep(timeout_seconds)
    await scanner.stop()

if __name__=='__main__':    
    asyncio.run(run())
