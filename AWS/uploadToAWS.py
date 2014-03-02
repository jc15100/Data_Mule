from IoTkitSimpleExample import *
def upload(filename):
    with open(filename) as file:
        name = file.readline()
        uom = file.readline()
        data = file.readlines()
    register_metric(name,"float",uom)
    for d in data:
        send_data(name,d)