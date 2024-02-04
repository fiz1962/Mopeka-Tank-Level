import asyncio
import struct

from bleak import BleakScanner

timeout_seconds = 30

def detection_callback(device, advertisement_data):
            print(device.address, advertisement_data.rssi)
            print(advertisement_data)
            print('-----------------')

async def run():
    scanner = BleakScanner(detection_callback=detection_callback)
    await scanner.start()
    await asyncio.sleep(timeout_seconds)
    await scanner.stop()

if __name__=='__main__':    
    asyncio.run(run())
