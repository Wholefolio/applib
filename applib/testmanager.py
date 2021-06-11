import unittest
import multiprocessing as mp
import time
import pickle
from socket import socket, AF_INET, SOCK_STREAM

from manager import Manager

class TestManager(unittest.TestCase):
    
    def setUp(self):
        self.manager = Manager()

    def testInit(self):
        """Test that the DB class was created."""
        self.assertIsInstance(self.manager, Manager)

    def testGetStatus(self):
        """Test the get status on empty Coiner."""
        res = self.manager.handleStatusEvent(1)
        self.assertEqual((res['id'], res['type']), (1, "status-response"))

    def testIncoming(self):
        """Test the incoming loop with a status type request."""
        p = mp.Process(target=self.manager.incoming)
        p.start()
        time.sleep(0.1)
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(("localhost", 5000))
        data = pickle.dumps({'id': 1, 'type': 'status'})
        s.sendall(data)
        data = s.recv(1024)
        res = pickle.loads(data)
        s.close()
        self.assertEqual((res["type"], res["id"]), ("status-response", 1))
        p.terminate()


if __name__ == "__main__":
    unittest.main()
