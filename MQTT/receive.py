
""" Send File Using MQTT """
import csv
import time
import paho.mqtt.client as paho
import hashlib
broker="broker.hivemq.com"
broker="iot.eclipse.org"
broker="192.168.1.158"
filename="healthcare_data.csv"
topic="data/files"
qos=1
data_block_size=2000
file_out="copy-"+filename
fout=open(file_out,"wb") #use a different filename
# for outfile as I'm running sender and receiver together
filename = ['id',
              'name',
              'age',
              'e-mail',
              'phone',
              'address',
              'condition',
              'bmi',
              'status',
              'device_id',
              'reading_id',
              'heart_rate',
              'blood_pressure_top',
              'blood_pressure_bottom',
              'body_temperature',
              'blood_sugar_level',
              'time_of_measurement',
              'coordinates']
def process_message(msg):
    """ This is the main receiver code
    """
    print("received ")
    global bytes_in
    if len(msg)==200: #is header or end
        print("found header")
        msg_in=msg.decode("utf-8")
        msg_in=msg_in.split(",,")
        if msg_in[0]=="end": #is it really last packet?
            in_hash_final=in_hash_md5.hexdigest()
            if in_hash_final==msg_in[2]:
                print("File copied OK -valid hash  ",in_hash_final)
                return -1
            else:
                print("Bad file receive   ",in_hash_final)
            return False
        else:
            if msg_in[0]!="header":
                in_hash_md5.update(msg)
                return True
            else:
                return False
    else:
        bytes_in=bytes_in+len(msg)
        in_hash_md5.update(msg)
        print("found data bytes= ",bytes_in)
        return True
#define callback
def on_message(client, userdata, message):
    global fout
    #time.sleep(1)
    #print("received message =",str(message.payload.decode("utf-8")))
    if process_message(message.payload):
        fout.write(message.payload)
############
def extract_file_data(file_data):
    data=csv.loads(file_data)
    filename=data["filename"]
    return filename
def process_message(msg):
    """ This is the main receiver code
    """
    global fout
    print("received ")
    if len(msg)==200: #is header or end
        msg_in=msg.decode("utf-8","ignore")
        msg_in=msg_in.split(",,")
        if msg_in[0]=="header": #header
            filename=extract_file_data(msg_in[1])
            file_out="copy-"+filename
            fout=open(file_out,"wb") #use a different filename

        if msg_in[0]=="end": #is it really last packet?
            in_hash_final=in_hash_md5.hexdigest()
            if in_hash_final==msg_in[2]:
                print("File copied OK -valid hash  ",in_hash_final)
            else:
                print("Bad file receive   ",in_hash_final)
            return False
        else:
            if msg_in[0]!="header":
                in_hash_md5.update(msg)
                return True
            else:
                return False
    else:
        in_hash_md5.update(msg)
        #msg_in=msg.decode("utf-8","ignore")
        if len(msg) <100:
            print(msg)
        return True


bytes_in=0
client= paho.Client("client-receive-001")  #create client object client1.on_publish = on_publish                          #assign function to callback client1.connect(broker,port)                                 #establish connection client1.publish("data/files","on")
######
client.on_message=on_message
client.mid_value=None
#####
print("connecting to broker ",broker)
client.connect(broker)#connect
#client.loop_start() #start loop to process received messages
print("subscribing ")
client.subscribe(topic)#subscribe
time.sleep(2)
start=time.time()
time_taken=time.time()-start
in_hash_md5 = hashlib.md5()
run_flag=True
while run_flag:
    client.loop(00.1)  #manual loop
    pass
client.disconnect() #disconnect
#client.loop_stop() #stop loop
fout.close()
