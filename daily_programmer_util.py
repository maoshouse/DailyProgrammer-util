import os.path
import reader
if(not(os.path.isfile('config.cfg'))):
    print ("Missing config file!")
else:
    r = reader.Reader()
    r.read()

