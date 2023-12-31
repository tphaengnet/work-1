# -*- coding: utf-8 -*-
"""6670096521_aissignment_8.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hcl28HFg4tBhMLFyN1veFlYKApC_pRLv
"""

!pip install kafka-python

!pip install avro

# import required libraries
from kafka import KafkaConsumer, KafkaProducer
import avro.schema
import avro.io
import io
import hashlib, json

def serialize(schema, obj):
    bytes_writer = io.BytesIO()
    encoder = avro.io.BinaryEncoder(bytes_writer)
    writer = avro.io.DatumWriter(schema)
    writer.write(obj, encoder)
    return bytes_writer.getvalue()

def deserialize(schema, raw_bytes):
    bytes_reader = io.BytesIO(raw_bytes)
    decoder = avro.io.BinaryDecoder(bytes_reader)
    reader = avro.io.DatumReader(schema)
    return reader.read(decoder)

!apt install subversion

!wget https://raw.githubusercontent.com/pvateekul/2110531_DSDE_2023s1/main/code/Week09_DataIngestion/Assignment/transaction.avsc

!wget https://raw.githubusercontent.com/pvateekul/2110531_DSDE_2023s1/main/code/Week09_DataIngestion/Assignment/submit.avsc

!wget https://raw.githubusercontent.com/pvateekul/2110531_DSDE_2023s1/main/code/Week09_DataIngestion/Assignment/result.avsc

schema_file = '/content/transaction.avsc'
txschema = avro.schema.parse(open(schema_file).read())
schema_file = '/content/submit.avsc'
submitschema = avro.schema.parse(open(schema_file).read())
schema_file = '/content/result.avsc'
resultschema = avro.schema.parse(open(schema_file).read())

# Connect to kafka broker running in your local host (docker). Change this to your kafka broker if needed
kafka_broker = 'lab.aimet.tech:9092'
#kafka_broker = 'ip_or_hostname_of_kafka_server:9092'

producer = KafkaProducer(bootstrap_servers=[kafka_broker])

txconsumer = KafkaConsumer(
    'transaction',
     bootstrap_servers=[kafka_broker],
     enable_auto_commit=True,
     value_deserializer=lambda x: deserialize(txschema, x))
resultconsumer = KafkaConsumer(
    'result',
     bootstrap_servers=[kafka_broker],
     enable_auto_commit=True,
     value_deserializer=lambda x: deserialize(resultschema, x))

vid = "V878613"
token = "c6f697f7d57d6cc9bed218454300ddcd"

def gen_signature(txid, payer, payee, amount, token):
    o = {'txid': txid, 'payer': payer, 'payee': payee, 'amount': amount, 'token': token}
    return hashlib.md5(json.dumps(o, sort_keys=True).encode('utf-8')).hexdigest()

for message in txconsumer:
    print(message.value)
    signature=gen_signature(message.value['txid'],message.value['payer'],message.value['payee'],message.value['amount'],token)
    o = {
        'vid': vid,
        'txid': message.value['txid'],
        'signature': signature
    }
    data = serialize(submitschema, o)
    print(o)
    print(data)
    producer.send('submit', data)
    time.sleep(2)

print('Running result')
print('Running result with AVRO')
for message in resultconsumer:
    print(message.value)

