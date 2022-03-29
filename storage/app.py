import connexion
from connexion import NoContent
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from create_account import Passworduser
from create_password import Userpasswords
import datetime
import yaml
import logging, logging.config
from pykafka import KafkaClient
import json
from pykafka.common import OffsetType
from threading import Thread

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())
    db_info = app_config["datastore"]["db"]
    user = app_config["datastore"]["user"]
    password = app_config["datastore"]["password"]
    hostname = app_config["datastore"]["hostname"]
    port = app_config["datastore"]["port"]

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger("basicLogger")
DB_ENGINE = create_engine("mysql+pymysql://%s:%s@%s:%d/%s" % (user, password, hostname, port, db_info))
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

logger.info("Connecting to DB. Hostname:{}, Port:{}".format(hostname, port))


# DB_ENGINE = create_engine("sqlite:///readings.sqlite")
# Base.metadata.bind = DB_ENGINE
# DB_SESSION = sessionmaker(bind=DB_ENGINE)


def create_new_user(body):
    """ Initialize a password manager user """

    session = DB_SESSION()
    # trace_id = random.randint(100000, 200000)
    # print(trace_id)
    password_user = Passworduser(body['user_id'],
                                 body['name'],
                                 body['password'],
                                 body['email'],
                                 body['trace_id'])
    # print(password_user)
    session.add(password_user)

    session.commit()
    session.close()
    # logger.info("Stored event %s request with a unique id of %s"
    #             % ("Password Manager account", body['trace_id']))

    return NoContent, 201


def add_new_password(body):
    """ Initialize a password of a user """

    session = DB_SESSION()
    # trace_id = random.randint(100000, 200000)
    # print(trace_id)

    user_password = Userpasswords(body['password_id'],
                                  body['password'],
                                  body['password_hint'],
                                  body['description'],
                                  body['trace_id'])

    session.add(user_password)

    session.commit()
    session.close()
    # logger.info("Stored event %s request with a unique id of %s"
    #             % ("User Passwords", body['trace_id']))

    return NoContent, 201


def get_password_user(timestamp):
    """ Gets user password readings after the timestamp """

    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    # timestamp_datetime2 = datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S.%f")
    # logger.info("password user current time:{}".format(timestamp_datetime))
    readings = session.query(Passworduser).filter(Passworduser.date_created >= timestamp_datetime)
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
        # logger.info("user reading:{}".format(reading))
        # print(results_list)
    # logger.info("user reading list:{}".format(results_list))
    session.close()

    logger.info("User Timestamp %s returns %d results" %
                (timestamp, len(results_list)))
    return results_list, 200


def get_user_password(timestamp):
    """ Gets user password readings after the timestamp """

    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    logger.info("user password current time:{}".format(timestamp_datetime))
    readings = session.query(Userpasswords).filter(Userpasswords.date_created >= timestamp_datetime)
    # logger.info("user password reading:{}".format(readings))
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
        # logger.info("password reading:{}".format(reading))
        # print(results_list)
    # logger.info("password reading list:{}".format(results_list))
    session.close()

    logger.info("Password Timestamp %s returns %d results" %
                (timestamp, len(results_list)))
    return results_list, 200


def process_messages():
    """ Process event messages """
    process_hostname = "%s:%d" % (app_config["events"]["hostname"],
                                  app_config["events"]["port"])
    logger.info("Access process hostname")
    client = KafkaClient(hosts=process_hostname)
    logger.info("Access client")
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    logger.info("Access topics")
    consumer = topic.get_simple_consumer(consumer_group=b'event_group',
                                         reset_offset_on_start=False,
                                         auto_offset_reset=OffsetType.LATEST)
    logger.info("Access consumer")
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)

        payload = msg["payload"]

        if msg["type"] == "passworduser":
            logger.info("Storing new user event")
            create_new_user(payload)
        elif msg["type"] == "userpassword":
            logger.info("Storing new password event")
            add_new_password(payload)
        consumer.commit_offsets()

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon = True
    t1.start()
    app.run(port=8090)
