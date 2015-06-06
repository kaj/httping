# httping
Measure http fetch times, send results to graphite

    Usage: httping.py [options] url ...
    Options:
      -h, --help       show this help message and exit
      --base=BASE      Prefix for metric series name [httping]
      -v, --verbose    
      -n, --nocarbon   Disable carbon, only show measurments on stdout
      --server=SERVER  Carbon server to send messages to [localhost]
      --port=PORT      Carbon port to send messages to [2003]
      --delay=DELAY    Seconds to wait between measurments [60]
