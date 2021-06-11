from socket import socket, AF_INET, SOCK_STREAM
import pickle


class Client(object):
    """This class interacts with a daemon via socket file."""

    def __init__(self, connection):
        """Read the scheduler config and connect to the daemon."""
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.connection = connection

    def connect(self):
        self.sock.connect(self.connection)

    def sendRequest(self, request):
        """Send the given request to scheduler."""
        self.sock.sendall(pickle.dumps(request))
        response = self.sock.recv(1024)
        return pickle.loads(response)

    def getStatus(self, request_id):
        """Get the current status of the scheduler daemon."""
        status_request = {'id': request_id, 'type': 'status'}
        self.sock.sendall(pickle.dumps(status_request))
        response = self.sock.recv(1024)
        return pickle.loads(response)
