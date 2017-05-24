import socket
import logging
from colorlog import ColoredFormatter

# from lib.core.settings import LOGGER
# from lib.core.settings import RESERVED_PORTS
# from core.settings import LOGGER

__all__ = [
	'PortScanner'
]

RESERVED_PORTS = {
	1, 5, 7, 18, 20, 21, 22, 23, 25, 29, 37, 42, 43, 49,
	53, 69, 70, 79, 80, 103, 108, 109, 110, 115, 118, 119, 137, 139,
	143, 150, 156, 161, 179, 190, 194, 197, 389, 396, 443, 444, 445, 458,
	546, 547, 563, 569, 1080
}

log_level = logging.INFO
logger_format = "[%(log_color)s%(asctime)s %(levelname)s%(reset)s] %(log_color)s%(message)s%(reset)s"
logging.root.setLevel(log_level)
formatter = ColoredFormatter(logger_format, datefmt="%I:%M:%S")
stream = logging.StreamHandler()
stream.setLevel(log_level)
stream.setFormatter(formatter)
LOGGER = logging.getLogger('pybeltConfig')
LOGGER.setLevel(log_level)
LOGGER.addHandler(stream)

class PortScanner(object):
	connection_made = []  # Connection made in list form

	def __init__(self, host):
		self.host = host
		self.ports = RESERVED_PORTS

	def connect_to_host(self):
		""" Attempt to make a connection using the most common ports 443, 445, etc.. """
		host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		for port in self.ports:
			try:
				LOGGER.info("Attempting to connect to port: {}".format(port))
				attempt = host.connect_ex((self.host, port))  # Connect to the host
				if attempt:  # If connection fails
					pass
				else:
					self.connection_made.append(port)
			except socket.error:
				pass
		host.close()
		if not self.connection_made:
			LOGGER.fatal("No connections could be made.")
		else:
			return "Connection made on port: {}.".format(''.join(str(self.connection_made)))
