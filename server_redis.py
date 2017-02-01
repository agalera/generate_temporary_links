import sys, os, uuid
import redis
from bottle import default_app, run, get, response, static_file, abort

r = redis.StrictRedis(host='localhost', port=6379, db=0)
base_source = "/tmp/test/originals/"
permit_generate = ['127.0.0.1']


@get('/file_id/<file_id>')
def send_file(file_id):
    path = r.get(file_id)
    filename = path.split('/')[-1]
    return static_file(path, root=base_source, download=filename)

@get('/generate_link/<path:path>')
def generate_link(path):
    for x in range(10):
        random_id = uuid.uuid4().hex
        try:
            r.set(random_id, path)
            return random_id
        except:
            print "identical id"
    abort("identical id x10")

if __name__ == "__main__":
    print "Debug Mode"
    run(host='127.0.0.1', port=1234, debug=True, reloader=True)

#prod: gunicorn -w 3 -k gevent server:app -b 127.0.0.1:1234
app = default_app()
