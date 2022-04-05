from time import sleep

import connexion
from connexion import NoContent 
import json
import datetime 
import os
import yaml 
import logging, logging.config
import random
from pykafka import KafkaClient

FILE_NAME = "password_manager_file.json"
MAX_EVENT = 10
HEADERS = {'Content-Type': 'application/json'}

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())
    password_user = app_config["passworduser"]["url"]
    user_password = app_config["userpasswords"]["url"]
    kafka_server = app_config["events"]["hostname"]
    kafka_port = app_config["events"]["port"]
    event_topic = app_config["events"]["topic"]

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    logger = logging.getLogger("basicLogger")

retry_count = 0
hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
while retry_count < app_config["connect_kafka"]["retry_count"]:
    try:
        logger.info('trying to connect, attempt: %d' % retry_count)
        client = KafkaClient(hosts=hostname)
        topic = client.topics[str.encode(app_config['events']['topic'])]
        producer = topic.get_sync_producer()
    except:
        logger.error('attempt %d failed, reconnecting in 3 seconds...' % retry_count)
        retry_count = retry_count + 1
        sleep(app_config["connect_kafka"]["sleep_time"])
    else:
        break
logger.info("Running Kafka")


def make_file():
    """This will create a file with an empty list to host the JSON data"""
    
    if os.path.isfile(FILE_NAME) == False:
        new_file = open(FILE_NAME, "w")
        new_file.write("[]")
        new_file.close()


def create_new_user(body):
    """This will add a user to Password Manager"""
    trace_id = random.randint(100000, 200000)
    event_name = password_user.split("/")[-1]
    body['trace_id'] = str(trace_id)
    logger.info("Received event {} reading with a trace id of {}".format(event_name, trace_id))
    # trace_id = body['trace_id']
    client = KafkaClient(hosts='{}:{}'.format(kafka_server, kafka_port))
    # topic = client.topics[str.encode(event_topic)]
    # producer = topic.get_sync_producer()

    msg = {"type": "passworduser",
           "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
           "payload": body}
    msg_str = json.dumps(msg)
    logger.info("Received event %s request with a unique id of %s"
                % ("Password Manager account", body['trace_id']))
    producer.produce(msg_str.encode('utf-8'))

    # response = requests.post(app_config["passworduser"]["url"], json=body, headers=HEADERS)
    logger.info("Returned event %s response %s with status %s"
                % ("Password Manager account", body['trace_id'], 200))

    return NoContent, 200


def add_new_password(body):
    """This will add a password account with description"""
    trace_id = random.randint(100000, 200000)
    body['trace_id'] = str(trace_id)
    event_name = user_password.split("/")[-1]
    logger.info("Received event {} reading with a trace id of {}".format(event_name, trace_id))
    client = KafkaClient(hosts='{}:{}'.format(kafka_server, kafka_port))
    # topic = client.topics[str.encode(event_topic)]
    # producer = topic.get_sync_producer()

    msg = {"type": "userpassword",
           "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
           "payload": body}
    msg_str = json.dumps(msg)
    logger.info("Received event %s request with a unique id of %s"
                % ("User Passwords", body['trace_id']))
    producer.produce(msg_str.encode('utf-8'))

    # response = requests.post(app_config["userpasswords"]["url"], json=body, headers=HEADERS)
    logger.info("Returned event %s response %s with status %d"
                % ("User Passwords", body['trace_id'], 200))

    return NoContent, 200
 

app = connexion.FlaskApp(__name__, specification_dir='') 
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)
 
if __name__ == "__main__": 
    app.run(port=8080)
