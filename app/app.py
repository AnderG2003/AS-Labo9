import time
import redis
from flask import Flask
import os

app = Flask(__name__)
redis_host = os.environ.get("REDISHOST")
cache = redis.Redis(host=redis_host, port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    #os._exit(0)
    count = get_hit_count()
    return 'Hola Andertxu! Este sitio se ha visitado {} veces.\n'.format(count)
