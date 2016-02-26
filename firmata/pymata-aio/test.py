from flask import Flask
from driver import Driver
import signal

app = Flask(__name__)

driver = Driver()
signal.signal(signal.SIGINT, driver.shutdown)
driver.start()

print("Here!!")

@app.route("/")
def hello():
  # driver = Driver()
  # Graceful shutdown on ctrl-c
  # signal.signal(signal.SIGINT, driver.shutdown)
  # driver.start()
  return "Hello World!"

if __name__ == "__main__":
#   # driver = Driver()
#   # driver.start()

#   app.debug = True
  app.run(host='0.0.0.0')
