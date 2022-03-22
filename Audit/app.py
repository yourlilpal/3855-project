import connexion
from connexion import NoContent
from pykafka import KafkaClient
import yaml
import json
import logging, logging.config

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    logger = logging.getLogger('basicLogger')


def get_password_user(index):
    """ Get User Reading in History """
    hostname = "%s:%d" % (app_config["events"]["hostname"],
                          app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,
                                         consumer_timeout_ms=1000)
    counter = 0
    logger.info("Retrieving User at index %d" % index)
    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            payload = msg["payload"]
            if msg['type'] == 'passworduser':
                if counter == index:
                    return payload, 200
                counter += 1

    except:
        logger.error("No more messages found")

    logger.error("Could not find User at index %d" % index)
    return {"message": "Not Found"}, 404


def get_user_password(index):
    """ Get Password Reading in History """
    hostname = "%s:%d" % (app_config["events"]["hostname"],
                          app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,
                                         consumer_timeout_ms=1000)
    counter = 0
    logger.info("Retrieving Password at index %d" % index)
    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            payload = msg["payload"]
            if msg['type'] == 'userpassword':
                if counter == index:
                    return payload, 200
                counter += 1

    except:
        logger.error("No more messages found")

    logger.error("Could not find Password at index %d" % index)
    return {"message": "Not Found"}, 404


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)


if __name__ == "__main__":
    app.run(port=8110)
