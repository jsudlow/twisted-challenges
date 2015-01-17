# This is the Twisted Get Poetry Now! client, version 3.1.

# NOTE: This should not be used as the basis for production code.

import optparse, sys

from twisted.internet.protocol import Protocol, ClientFactory


def parse_args():
    usage = """usage: %prog [options] [hostname]:port ...

This is the Get Poetry Now! client, Twisted version 3.1
Run it like this:

  python get-poetry-1.py port1 port2 port3 ...

If you are in the base directory of the twisted-intro package,
you could run it like this:

  python twisted-client-3/get-poetry-1.py 10001 10002 10003

to grab poetry from servers on ports 10001, 10002, and 10003.

Of course, there need to be servers listening on those ports
for that to work.
"""

    parser = optparse.OptionParser(usage)

    _, addresses = parser.parse_args()

    if not addresses:
        print parser.format_help()
        parser.exit()

    def parse_address(addr):
        if ':' not in addr:
            host = '127.0.0.1'
            port = addr
        else:
            host, port = addr.split(':', 1)

        if not port.isdigit():
            parser.error('Ports must be integers.')

        return host, int(port)

    return map(parse_address, addresses)


class PoetryProtocol(Protocol):

    poem = ''

    def dataReceived(self, data):
        self.poem += data
        self.factory.download_active(self.transport.getPeer().port)
        

    def connectionLost(self, reason):
        self.poemReceived(self.poem)
        self.factory.download_finished(self.transport.getPeer().port)

    def poemReceived(self, poem):
        self.factory.poem_finished(poem)
   

class PoetryClientFactory(ClientFactory):

    protocol = PoetryProtocol

    def __init__(self, callback, errback,download_active,download_finished):
        self.callback = callback
        self.errback = errback
        self.download_active = download_active
        self.download_finished = download_finished

    def poem_finished(self, poem):
        self.callback(poem)
    def clientConnectionFailed(self, connector, reason):
        self.errback(reason)
    def download_active(self, port):
        self.download_active(port)
    def download_finished(self,port):
        self.download_finished(port)    

def get_poetry(host, port, callback, errback,download_active,download_finished,timeoutCheck):
    """
    Download a poem from the given host and port and invoke

      callback(poem)

    when the poem is complete. If there is a failure, invoke:

      errback(err)

    instead, where err is a twisted.python.failure.Failure instance.
    """
    from twisted.internet import reactor
    factory = PoetryClientFactory(callback, errback,download_active, download_finished)

    reactor.connectTCP(host, port, factory)
    reactor.callLater(4,timeoutCheck,port)

def poetry_main():
    addresses = parse_args()

    from twisted.internet import reactor

    poems = []
    errors = []
    connections_downloading = []
    
    def download_active(port):
        print "Hey we actually got called back! Downloading is happening"
        
        if port in connections_downloading:
            print "Already Downloading"
        else:
            print "Ahh a new one"
            connections_downloading.append(port)
        print connections_downloading

    def download_finished(port):
        print "The connection just closed, that means were done downloading and should remove this port from active"
        connections_downloading.remove(port)
        print connections_downloading

    def got_poem(poem):
        poems.append(poem)
        poem_done()

    def poem_failed(err):
        print >>sys.stderr, 'Poem failed:', err
        errors.append(err)
        poem_done()

    def poem_done():
        if len(poems) + len(errors) == len(addresses):
            if reactor.running:
                reactor.stop()
    def timeoutCheck(port):
        print "checking timeout"
        if port in connections_downloading:
            print "Time Exceeded - SHUTTING DOWN CONNECTIONS"
            poem_failed("Timeout")


    for address in addresses:
        host, port = address
        get_poetry(host, port, got_poem, poem_failed,download_active,download_finished,timeoutCheck)

    reactor.run()

    for poem in poems:
        print poem


if __name__ == '__main__':
    poetry_main()
