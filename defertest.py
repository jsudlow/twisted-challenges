from twisted.internet.defer import Deferred
from twisted.python.failure import Failure

def got_poem(res):
  print 'your poem is served:'
  print res
def poem_failed(err):
  #print err.__class__
  #print err
  #Uncomment code above to really see we do get an actual failure
  #object from the deferred
  print 'No poetry fo you'
def out(s):
  print s
d = Deferred()

#add callback/errback
#d.addCallbacks(got_poem, poem_failed)
d.addCallbacks(out,out)
d.callback('First Result')

#d.errback(Exception('First Error'))
#cant call callback more than one time
#d.callback('This poem is so short babay')
#d.errback(Exception('I have failed you master'))
print "Finished"