import sys
sys.dont_write_bytecode = True
from site import app
from orvsd_central import app
app.run(debug=True)
