from optparse import OptionParser

import plotly.plotly as py

parser = OptionParser()

parser.add_option("-u", "--username", dest="username", help="input username for plotly.", metavar="UNAME")
parser.add_option("-k", "--apikey", dest="apikey", help="input apikey for plotly.", metavar="APIKEY")

(options, args) = parser.parse_args()

py.sign_in(options['username'], options['apikey'])