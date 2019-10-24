from System import AsyncCallback
from System.Net import HttpListener, HttpListenerException

from errors import ServerException

class SimpleServer:
    def __init__(self, router, port):
        self.port = port
        self.router = router

    def serve(self):
        listener = HttpListener()
        prefix = 'http://*:%s/' % str(self.port)
        listener.Prefixes.Add(prefix)
        try:
            listener.Start()
        except HttpListenerException:
            raise ServerException("Error starting server")

        print "Listening on port %s" % str(self.port)

        while True:
            result = listener.BeginGetContext(AsyncCallback(self.handleRequest), listener)
            result.AsyncWaitHandle.WaitOne()


    def handleRequest(self, result):
        listener = result.AsyncState
        try:
            context = listener.EndGetContext(result)
        except:
            return
        request = context.Request
        response = context.Response
        
        url = request.RawUrl
        method = request.HttpMethod

        view, params = self.router.get_view(url, method)
        view(request, response, params)
