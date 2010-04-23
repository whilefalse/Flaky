import urllib2
import json
import sys
import time
import logging

log = logging.getLogger("errors")
log.setLevel(logging.INFO)
fh = logging.FileHandler('log.txt')
fh.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
log.addHandler(fh)

host = 'localhost'
port = '1234'

def go(interval):
    counters = {}
    while True:
        try:
            req = urllib2.urlopen("http://%s:%s" % (host, port))
            data = req.read()
        except urllib2.URLError:
            print 'Reading URL Failed'
            log.error('Reading URL Failed')
            time.sleep(interval)
            continue

        try:
            js = json.loads(data)
            prev = counters.get(js['uid'], 0)
            print "%s [Expecting %s]" % (js, str(prev+1)),
            if js['count'] != prev + 1:
                print ' [WRONG]'
                log.error("For UID [%s], expected [%s], got [%s]" % (js['uid'], prev+1, js['count']))
            else:
                print ' [OK]'
            counters[js['uid']] = js['count']

        except ValueError:
            print 'Couldn\'t decode JSON: %s' % data
            log.error('Couldn\'t decode JSON: %s' % data)

        time.sleep(interval)

if __name__ == "__main__":
    log.info('===STARTING===')
    try:
        go(float(sys.argv[1]))
    except KeyboardInterrupt:
        log.info('===STOPPING===')
