from twisted.web import server, resource
from twisted.internet import reactor
from twisted.application import internet, service
class HelloResource(resource.Resource):
    isLeaf = True
    numberRequests = 0
    
    def render_GET(self, request):
        self.numberRequests += 1
        request.setHeader("content-type", "text/plain")
        return "I am request #" + str(self.numberRequests) + "\n"

factory = server.Site(HelloResource())


# this is the important bit
application = service.Application("sms_card_sender")  # create the Application
senderService = internet.TCPServer(8880, factory) # create the service
# add the service to the application
senderService.setServiceParent(application)