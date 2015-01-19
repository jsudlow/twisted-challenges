import sys

from twisted.internet.defer import Deferred

def got_poem(poem):
  print poem
  return 'Alex jone for president'
def poem_failed(err):
  print "OHHH M Y GOD WE GOT AN ERROR"
  return "UFO JUST LANDED"

def poem_done(_):
  print _
  from twisted.internet import reactor
  reactor.stop()

d = Deferred()
d.addCallbacks(got_poem,poem_failed)
d.addBoth(poem_done)

from twisted.internet import reactor

#reactor.callWhenRunning(d.callback, 'Another poem test')
reactor.callWhenRunning(d.errback, Exception('Conspiracy Error'))

reactor.run()