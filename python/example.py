import asyncio
from lib.cortex import Cortex
import json
import serial
import time
import threading


ser = None

async def do_stuff(cortex, headset):


    # await cortex.inspectApi()
    #print("** USER LOGIN **")
    await cortex.get_user_login()
    #print("** GET CORTEX INFO **")
    await cortex.get_cortex_info()
    #print("** HAS ACCESS RIGHT **")
    await cortex.has_access_right()
    #print("** REQUEST ACCESS **")
    await cortex.request_access()
    #print("** AUTHORIZE **")
    await cortex.authorize(debit=1000)
    #print("** GET LICENSE INFO **")
    await cortex.get_license_info()
    #print("** QUERY HEADSETS **")
    await cortex.query_headsets()
    if len(cortex.headsets) > 1:
        print("cortex.headsets = ", cortex.headsets)
        #print("** CREATE SESSION **")
        await cortex.create_session(activate=True, headset_id=cortex.headsets[headset])
        #print("** CREATE RECORD **")
        await cortex.create_record(title="test record 1")
        #print("** SUBSCRIBE POW & MET **")
        await cortex.subscribe(['com'])
        while True:
            resp = await cortex.get_data()
            jsondata = json.loads(resp)
            if 'com' in jsondata:
                cmd = jsondata['com'][0]
                #print(headset, cmd)
                if jsondata['com'][0] == 'push':
                    print(headset, "push")
                    if cortex.headsets[headset] == 'INSIGHT-A2D20076':
                        ser.write(str.encode('a'))
                    if cortex.headsets[headset] == 'INSIGHT-A1D204FC':
                        ser.write(str.encode('s'))
                    time.sleep(0.100)



        #await cortex.inject_marker(label='halfway', value=1,
        #                           time=cortex.to_epoch())
        #while cortex.packet_count < 200:
        #    await cortex.get_data()
        await cortex.close_session()



def thr1():
    cortex = Cortex('./cortex_creds')
    asyncio.run(do_stuff(cortex,0))
    cortex.close()


def thr2():
    cortex = Cortex('./cortex_creds')
    asyncio.run(do_stuff(cortex,1))
    cortex.close()





def test():
    global ser 
    ser = serial.Serial(port='/dev/cu.wchusbserial145210', baudrate=115200)
    ser.isOpen()
    thread1 = threading.Thread(target=thr1)
    thread2 = threading.Thread(target=thr2)

    thread1.start()
    thread2.start()






if __name__ == '__main__':
    test()
