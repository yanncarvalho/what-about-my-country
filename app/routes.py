from .__init__ import app
from .jobs_req_data import *

@app.route('/')
def hello_world():
  return "<p>Hello, World!</p>"
