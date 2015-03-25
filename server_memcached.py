import sys, os, uuid
import memcache
from bottle import default_app, run, get, response, static_file, abort

m = memcache.Client(['127.0.0.1:11211'])
base_source = "/tmp/test/originals/"
permit_generate = ['127.0.0.1']
time_temporal_link = 60*4 # seconds

@get('/file_id/<file_id>')
def send_file(file_id):
    path = m.get(file_id)
    filename = path.split('/')[-1]
    return static_file(path, root=base_source, download=filename)

@get('/generate_link/<path:path>')
def generate_link(path):
    if not request['REMOTE_ADDR'] in permit_generate:
        abort(401, "Sorry, access denied.")

    for x in range(10):
        random_id = uuid.uuid4().hex
        if r.add(str(random_id), path, time=time_temporal_link):
            return random_id
        else:
            print "identical id"
    abort("identical id x10")

if __name__ == "__main__":
    print "Debug Mode"
    run(host='0.0.0.0', port=1234, debug=True, reloader=True)

#prod: gunicorn -w 3 -k gevent server:app -b 127.0.0.1:1234
app = default_app()
