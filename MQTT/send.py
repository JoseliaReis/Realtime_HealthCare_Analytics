
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
data_block_size=200000
fo=open(filename,"rb")
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
    if len(msg)==200: #is header or end
        msg_in=msg.decode("utf-8")
        msg_in=msg_in.split(",,")
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
        return True
#define callback
def on_message(client, userdata, message):
    #time.sleep(1)
    #print("received message =",str(message.payload.decode("utf-8")))
    if process_message(message.payload):
        fout.write(message.payload)
def on_publish(client, userdata, mid):
    #logging.debug("pub ack "+ str(mid))
    client.mid_value=mid
    client.puback_flag=True

## waitfor loop
def wait_for(client,msgType,period=0.25,wait_time=40,running_loop=False):
    client.running_loop=running_loop #if using external loop
    wcount=0
    #return True
    while True:
        #print("waiting"+ msgType)
        if msgType=="PUBACK":
            if client.on_publish:
                if client.puback_flag:
                    return True

        if not client.running_loop:
            client.loop(.01)  #check for messages manually
        time.sleep(period)
        #print("loop flag ",client.running_loop)
        wcount+=1
        if wcount>wait_time:
            print("return from wait loop taken too long")
            return False
    return True
def send_header(filename):

    file_data={"filename":filename}
    file_data_csv=csv.dumps(file_data)
    header="header"+",,"+file_data_csv + ",,"
    header=bytearray(header,"utf-8")
    header.extend(b'x'*(200-len(header)))
    print(header)
    c_publish(client,topic,header,qos)
def send_end(filename):
    end="end"+",,"+filename+",,"+out_hash_md5.hexdigest()+",,"
    end=bytearray(end,"utf-8")
    end.extend(b'x'*(200-len(end)))
    print(end)
    c_publish(client,topic,end,qos)
def send_end(filename):
    end="end"+",,"+filename+",,"+out_hash_md5.hexdigest()
    end=bytearray(end,"utf-8")
    end.extend(b','*(200-len(end)))
    print(end)
    c_publish(client,topic,end,qos)
def c_publish(client,topic,out_message,qos):
    res,mid=client.publish(topic,out_message,qos)#publish
    #return

    if res==0: #published ok
        if wait_for(client,"PUBACK",running_loop=True):
            if mid==client.mid_value:
                print("match mid ",str(mid))
                client.puback_flag=False #reset flag
            else:
                print("quitting")
                raise SystemExit("not got correct puback mid so quitting")

        else:
            raise SystemExit("not got puback so quitting")

client= paho.Client("client-001")  #create client object client1.on_publish = on_publish                          #assign function to callback client1.connect(broker,port)                                 #establish connection client1.publish("data/files","on")
######
#client.on_message=on_message
client.on_publish=on_publish
client.puback_flag=False #use flag in publish ack
client.mid_value=None
#####
print("connecting to broker ",broker)
client.connect(broker)#connect
client.loop_start() #start loop to process received messages
print("subscribing ")
client.subscribe(topic)#subscribe
time.sleep(2)
start=time.time()
print("publishing ")
send_header(filename)
Run_flag=True
count=0
out_hash_md5 = hashlib.md5()
in_hash_md5 = hashlib.md5()
bytes_out=0

while Run_flag:
    chunk=fo.read(data_block_size)
    if chunk:
        out_hash_md5.update(chunk) #update hash
        out_message=chunk
        #print(" length =",type(out_message))
        bytes_out=bytes_out+len(out_message)

        c_publish(client,topic,out_message,qos)


    else:
        #end of file so send hash
        out_message=out_hash_md5.hexdigest()
        send_end(filename)
        Run_flag=False
time_taken=time.time()-start
print("took ",time_taken)
print("bytes sent =",bytes_out)
time.sleep(10)
client.disconnect() #disconnect
client.loop_stop() #stop loop
fout.close()
fo.close()