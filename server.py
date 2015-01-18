import sys, os, uuid
from bottle import default_app, run, get, response

base_source = "/tmp/test/originals/"
base_link = "/tmp/test/links/"

@get('/generate_link/<path:path>')
def generate_link(path):
    filename = path.split('/')[-1]
    link_name = uuid.uuid4().hex
    for x in range(10):
        try:
            os.mkdir(os.path.join(base_link, link_name))
            os.symlink(os.path.join(base_source, path),
                       os.path.join(base_link, link_name, filename))
            return link_name
        except:
            pass
    return "internal error"

if __name__ == "__main__":
    print "Debug Mode"
    run(host='0.0.0.0', port=1234, debug=True, reloader=True)

#prod: gunicorn -w 3 -k gevent server:app -b 127.0.0.1:1234
app = default_app()