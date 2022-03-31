import random
import connexion
from apscheduler.schedulers.background import BackgroundScheduler
from connexion import NoContent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from stats import Stats
import datetime
import yaml
import logging, logging.config
import requests
import json

with open('app_conf.yml', 'r') as f: 
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read()) 
    logging.config.dictConfig(log_config) 
    logger = logging.getLogger('basicLogger')

DB_ENGINE = create_engine("sqlite:///%s" % app_config["datastore"]["filename"])
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def populate_stats(): 
    """ Periodically update stats """ 
    logger.info("Start Periodic Processing")

    session = DB_SESSION()

    results = session.query(Stats).order_by(Stats.last_updated.desc()).first()

    session.close()

    if not results:
        stats = {
            "num_of_name": 0,
            "num_of_password": 0,
            "trace_id": 0,
            # "max_length_password": 0,
            "last_updated": "2016-08-29T09:12:33Z"
            # "last_updated": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    else:
        stats = results.to_dict()

    old_datetime = stats['last_updated']

    #response
    get_name = requests.get(app_config['passworduser']['url'] + '?timestamp=' + old_datetime)
    get_password = requests.get(app_config['userpasswords']['url'] + '?timestamp=' + old_datetime)

    #json data
    # passworduser_dict = json.loads(get_name.text)
    # userpassword_dict = json.loads(get_password.text)

    if get_name.status_code != 200:
        logger.error("Received a status code of {}.".format(get_name.status_code,))
    # elif get_name.json() == 0:
        # logger.info("Received {} events with a status code of {}.".format(len(get_name.json()), get_name.status_code))
        # logger.info("Received {} events with a status code of {}.".format(len(get_name.json()), get_name.status_code))
    else:
        # logger.info("Received {} events with a status code of {}. (Trace ID: {})".format(len(get_name.json()), get_name.status_code, passworduser_dict[0]["trace_id"]))
        logger.info("Received {} events with a status code of {}.".format(len(get_name.json()), get_name.status_code))

    if get_password.status_code != 200:
        logger.error("Received a status code of {}.".format(get_password.status_code))
    # elif get_password.json() == 0:
    #     logger.info("Received {} events with a status code of {}.".format(len(get_password.json()), get_password.status_code))

    else:
        # logger.info("Received {} events with a status code of {}. (Trace ID: {})".format(len(get_password.json()), get_password.status_code, userpassword_dict[0]["trace_id"]))
        logger.info("Received {} events with a status code of {}.".format(len(get_password.json()), get_password.status_code))

    #total amount of name and password

    stats['num_of_name'] = stats['num_of_name'] + len(get_name.json())
    logger.info("Populate total count of user: {}. Stored into Database.".format(len(get_name.json())))

    stats['num_of_password'] = stats['num_of_password'] + len(get_password.json())
    logger.info("Populate total count of passwords: {}. Stored into Datebase.".format(len(get_password.json())))
    #max length of password
    # list_password = []
    # print(userpassword_dict.value["password"])
    # for password in userpassword_dict.value["password"]:
    #     print(password)
    #     list_password.append(len(password))
    # print(list_password)



    # password_json = json.dumps(userpassword_dict, indent=4)
    # pass_json = json.loads(password_json)
    #
    # # print(type(password_json))
    # # print(len(pass_json[0]['password']))
    # logger.info("Populate max length of password. Stored into Datebase.")
    # if pass_json == 0:
    #     # return stats["max_length_password"]
    #     stats["max_length_password"] = len(pass_json[0]['password'])
    # else:
    #     # stats["max_length_password"] = len(pass_json[0]['password'])
    #     return stats["max_length_password"]
    # stats["max_length_password"] = len(pass_json[0]['password'])
    # stats["trace_id"] = passworduser_dict[0]["trace_id"] + ":" + userpassword_dict[0]["trace_id"]

    session = DB_SESSION()

    new_stats = Stats(stats["num_of_name"],
                      stats["num_of_password"],
                      # stats["max_length_password"],
                      stats["trace_id"],
                      datetime.datetime.now())

    session.add(new_stats)

    session.commit()
    session.close()

    logger.info("Periodic Processing Ending...")


def init_scheduler():
    """Set up background scheduler event that will record by seconds"""
    sched = BackgroundScheduler(daemon=True) 
    sched.add_job(populate_stats, 'interval', seconds=app_config['scheduler']['period_sec'])
    sched.start()


def get_stats():
    """Gets User and Password processed statistics"""
    session = DB_SESSION()

    results = session.query(Stats).order_by(Stats.last_updated.desc()).first()

    session.close()

    if not results:
        stats = {
            "num_of_name": 0,
            "num_of_password": 0,
            "max_length_password": 0,
            "trace_id": 0,
            "last_updated": "2016-08-29T09:12:33Z"
            # "last_updated": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    else:
        stats = results.to_dict()

    return stats, 200


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    # run our standalone gevent server
    init_scheduler() 
    app.run(port=8100, use_reloader=False)
    # app.run(port=8100)
