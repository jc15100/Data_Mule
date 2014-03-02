from IoTkitSimpleExample import *
def upload(filename):
    file = open(filename, 'r')
    try:
        name = file.readline()
        uom = file.readline()
        data = file.readlines()
    finally:
        file.close()
    register_metric(name,"float",uom)
    for d in data:
        send_data(name,d)