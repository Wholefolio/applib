import os
import sys
import pickle
import logging
from concurrent.futures import ThreadPoolExecutor
from socket import (socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR)
from socket import timeout as SOCKET_TIMEOUT


class Manager(object):
    """Provide base TCP connection handling capabilities for apps."""
    def __init__(self):
        """Some default values - these are to be overriden"""
        self.worker_limit = 5
        self.socket_port = 5000
        self.logger = logging.getLogger("Manager")

    def handleConfigEvent(self, **request):
        """Configure the running manager instance."""
        pass

    def handleStatusEvent(self, request_id):
        """Get the status of the adapter manager process and db."""
        response = {"id": request_id,
                    "type": "status-response",
                    "data": "running"}
        return response

    def handler(self, connection, addr):
        """Handle an incoming request:

        Receive all the data, load it and work with it(dict format).
        ."""
        pid = os.getpid()
        BUFFER = 1024
        self.logger.info("Handling connection [%s].", pid)
        received = bytes()
        while True:
            try:
                data = connection.recv(BUFFER)
            except SOCKET_TIMEOUT:
                break
            received += data
            # There is an extra 33 bytes that comes through the connection
            if sys.getsizeof(data) < (BUFFER + 33):
                break
            else:
                # Set a timeout. This is needed if the data is exactly the
                # length of the buffer - in that case without a timeout
                # we will get stuck in the recv part of the loop
                connection.settimeout(0.5)
        loaded_data = pickle.loads(data)
        self.logger.debug("Data loaded: %s", loaded_data)
        if not isinstance(loaded_data, dict):
            response = pickle.dumps("Bad request - expected dictionary.")
            connection.send(response)
            self.logger.debug("Bad request - expected dictionary")
            return False
        if loaded_data["type"] == "status":
            response = self.handleStatusEvent(loaded_data["id"])
            self.logger.debug("Response to status request: %s", response)
        elif loaded_data["type"] == "configure":
            response = self.handleConfigEvent(loaded_data["data"])
            self.logger.debug("Response to configure request: %s", response)
        connection.send(pickle.dumps(response))
        connection.close()

    def incoming(self):
        """Loop upon the incoming queue for incoming requests.

        Incoming request types: ['status', 'configure']
        Workflow:
        1) Get the request from the queue
        2) Sanitize it by checking the request type
        3) Pass it to the appropriate method for execution
        4) Put the response in the outbound queue and loop again
        """
        with ThreadPoolExecutor(max_workers=self.worker_limit) as executor:
            with socket(AF_INET, SOCK_STREAM) as sock:
                sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                sock.bind(("0.0.0.0", self.socket_port))
                sock.listen(10)
                self.logger.info("Server listening on local TCP port %s",
                                 self.socket_port)
                while True:
                    conn, addr = sock.accept()
                    executor.submit(self.handler, conn, addr)
                self.logger.info("Server shutting down")
