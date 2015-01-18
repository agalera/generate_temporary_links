import bottle
import sys, os, uuid
from bottle import default_app, run, get, response
base_source = "/tmp/test/originals/"
base_link = "/tmp/test/links/"

@get('/generate_link/<path:path>')
def generate_link(path):
    link_name = uuid.uuid4().hex
    for x in range(10):
        try:
            os.symlink(os.path.join(base_source, path),
                       os.path.join(base_link, link_name))
            return link_name
        except:
            pass
    return "epic error"

if __name__ == "__main__":
    if sys.argv[1] == "g":
        print "gunicorn"
        run(server='gunicorn', host='0.0.0.0', port=1234,workers=4, worker_class='gevent', debug=False,reloader=False)
    else:
        print "bottle normal"
        run(host='0.0.0.0', port=1234, debug=True, reloader=True)
app = default_app()