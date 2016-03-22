from flask import Flask
from flask import Response
import json
#from driver import Driver
#import signal

app = Flask(__name__)

#driver = Driver()
#signal.signal(signal.SIGINT, driver.shutdown)
#driver.start()

#print("Here!!")

@app.route("/")
def hello():
  # driver = Driver()
  # Graceful shutdown on ctrl-c
  # signal.signal(signal.SIGINT, driver.shutdown)
  # driver.start()
  return "<h2>YOOOOOOO</h2>"

@app.route("/test")
def test():
  # driver = Driver()
  # Graceful shutdown on ctrl-c
  # signal.signal(signal.SIGINT, driver.shutdown)
  # driver.start()
  data = {
      'hello'  : 'world',
      'number' : 3
  }
  js = json.dumps(data)
  resp = Response(js, status=200, mimetype='application/json')
  print "hit test endpoint"
  return resp

if __name__ == "__main__":
#   # driver = Driver()
#   # driver.start()

#   app.debug = True
  app.run(host='0.0.0.0')
