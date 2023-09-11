from kortex_api.TCPTransport import TCPTransport
from kortex_api.UDPTransport import UDPTransport
from kortex_api.RouterClient import RouterClient, RouterClientSendOptions
from kortex_api.SessionManager import SessionManager
from kortex_api.autogen.messages import Session_pb2


class RobotConnection:
    """
    Class that manages connection

    """

    TCP_PORT = 10000
    UDP_PORT = 10001

    @staticmethod
    def create_tcp_connection(ip: str = "192.168.2.10",
                              username: str = "admin",
                              password: str = "admin"):
        """
        returns RouterClient required to create
        services and send requests to device or sub-devices,

        """

        return RobotConnection(ip, port=RobotConnection.TCP_PORT, credentials=(username, password))

    @staticmethod
    def create_udp_connection(ip: str = "192.168.2.10",
                              username: str = "admin",
                              password: str = "admin"):
        """
        returns RouterClient that allows to create services and send requests
        to a device or its sub-devices @ 1khz.

        """

        return RobotConnection(ip, port=RobotConnection.UDP_PORT, credentials=(username, password))

    def __init__(self, ip_address, port=TCP_PORT, credentials=("", "")):

        self.ip_address = ip_address
        self.port = port
        self.credentials = credentials

        self.session_manager = None

        # Setup API
        self.transport = TCPTransport() if port == RobotConnection.TCP_PORT else UDPTransport()
        self.router = RouterClient(self.transport, RouterClient.basicErrorCallback)

    def connect(self):
        """
        Method responsible for connecting robot. It returns a RouterClient
        """
        self.transport.connect(self.ip_address, self.port)

        if self.credentials[0] != "":
            session_info = Session_pb2.CreateSessionInfo()
            session_info.username = self.credentials[0]
            session_info.password = self.credentials[1]
            session_info.session_inactivity_timeout = 60000  # (milliseconds)
            session_info.connection_inactivity_timeout = 2000  # (milliseconds)

            self.session_manager = SessionManager(self.router)
            print("Logging as", self.credentials[0], "on device", self.ip_address)
            self.session_manager.CreateSession(session_info)

        return self.router

    def disconnect(self):
        """"
        Method responsible for disconnecting robot, by closing SessionManager object
        """
        if self.session_manager is not None:
            router_options = RouterClientSendOptions()
            router_options.timeout_ms = 100

            self.session_manager.CloseSession(router_options)

        self.transport.disconnect()
