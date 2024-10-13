import socket
import select

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345
MESSAGE_SIZE = 1024

class Reactor:
    """
    class for reactor objects
    """
    def __init__(self):
        """
        keys are sockets, values are dicts. inner dicts keys are modes (read,write,except) and values are functions
        {SocketA : {'r' : func_r, 'w' : func_w, 'x': func_x }, SocketB : .... }
        """
        self.main_dict = {}
        self.is_running = False

    def subscribe(self, sock, mode, func):
        """
        subscribe to the reactor
        :param sock: the socket to subscribe
        :param mode: the mode of the socket read write or except
        :param func: function to execute according to the mode
        :return: None
        """
        if mode not in ['read', 'write', 'except']:
            raise ValueError("mode has to be read write or except")
        if sock not in self.main_dict:
            self.main_dict[sock] = {}
        self.main_dict[sock][mode] = func

    def unsubscribe(self, sock, mode):
        """
        unsubscribe from the reactor
        :param sock: the socket to unsubscribe
        :param mode: the mode of the socket to unsubscribe
        :return: None
        """
        if sock in self.main_dict and mode in self.main_dict[sock]:
            del self.main_dict[sock][mode]
            if not self.main_dict[sock]:
                del self.main_dict[sock]

    def run(self):
        """
        run the reactor until there are no more sockets subscribed
        :return: None
        """
        self.is_running = True
        while self.is_running:
            #print("--- Select round ---")
            r_list, w_list, x_list = [], [], []
            for sock, modes in self.main_dict.items():
                if 'read' in modes:
                    r_list.append(sock)
                if 'write' in modes:
                    w_list.append(sock)
                if 'except' in modes:
                    x_list.append(sock)
            if not r_list and not w_list and not x_list:
                print("zero sockets to monitor, stopping reactor.")
                self.stop()
                break
            r_ready, w_ready, x_ready = select.select(r_list, w_list, x_list)
            for sock in r_ready:
                self.main_dict[sock]['read']()
            for sock in w_ready:
                self.main_dict[sock]['write']()
            for sock in x_ready:
                self.main_dict[sock]['except']()


    def stop(self):
        self.is_running = False


class Server:
    """
    class that will be the server for our test
    """
    def __init__(self, reactor):
        """
        reactor for the server to use to handle 2 clients. subscribe to read first
        :param reactor:
        """
        self.reactor = reactor
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setblocking(False)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind((SERVER_IP, SERVER_PORT))
        self.server_sock.listen()
        self.client_count = 0
        self.reactor.subscribe(self.server_sock, 'read', self.accept_client)
        self.reactor.subscribe(self.server_sock, 'except', self.handle_exception)

    def accept_client(self):
        """
        function to accept client connection and subscribe their sockets to wait to read from them
        """
        client_sock, addr = self.server_sock.accept()
        client_sock.setblocking(False)
        self.client_count += 1
        self.reactor.subscribe(client_sock, 'read', lambda: self.read_from_client(client_sock, addr))
        self.reactor.subscribe(client_sock, 'except', lambda: self.handle_exception(client_sock))
        print(f"accepted connection from {addr}")

    def read_from_client(self, client_sock, addr):
        """
        function to get a message from a client. it creates a response and subscribe to write to it
        if there is no data, handle client disconnecting
        """
        data = client_sock.recv(MESSAGE_SIZE)
        if data:
            message = data.decode()
            print(f"Server got {message}")
            response = "pong".encode()
            self.reactor.subscribe(client_sock, 'write', lambda: self.write_to_client(client_sock, addr, response))
        else:
            self.reactor.unsubscribe(client_sock, 'read')
            self.reactor.unsubscribe(client_sock, 'except')
            client_sock.close()
            self.client_count -= 1
            print(f"client {addr} disconnected")
            if self.client_count == 0:
                self.shutdown()

    def write_to_client(self, client_sock, addr, response):
        """
        write to client
        """
        client_sock.sendall(response)
        print(f"Server sent {response.decode()} to {addr}")
        self.reactor.unsubscribe(client_sock, 'write')

    def handle_exception(self, client_sock=None):
        """
        handle exception if needed by closing it
        """
        print(f"exception on socket {client_sock}")
        self.reactor.unsubscribe(client_sock, 'read')
        self.reactor.unsubscribe(client_sock, 'write')
        self.reactor.unsubscribe(client_sock, 'except')
        client_sock.close()
        self.client_count -= 1
        print(f"client {client_sock} disconnected")
        if self.client_count == 0:
            self.shutdown()

    def shutdown(self):
        """
        close server socket
        """
        self.reactor.unsubscribe(self.server_sock, 'read')
        self.reactor.unsubscribe(self.server_sock, 'except')
        self.server_sock.close()
        print("server shutting down.")


class Client:
    """
    class for client
    """
    def __init__(self, reactor, name, num_pings):
        """
        init reactor, num of pings and socket. subscribe to write first
        """
        self.reactor = reactor
        self.name = name
        self.num_pings = num_pings
        self.pings_sent = 0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(False)
        self.sock.connect_ex((SERVER_IP, SERVER_PORT))
        self.reactor.subscribe(self.sock, 'write', self.send_ping)
        self.reactor.subscribe(self.sock, 'except', self.handle_exception)

    def send_ping(self):
        """
        function to send ping with index. when done, get ready to read
        """
        message = f"ping {self.pings_sent + 1} from {self.name}".encode()
        self.sock.sendall(message)
        print(f"{self.name} sent: {message.decode()}")
        self.pings_sent += 1
        self.reactor.unsubscribe(self.sock, 'write')
        self.reactor.subscribe(self.sock, 'read', self.receive_pong)

    def receive_pong(self):
        """
        function to get data from server. if needed, sub to write when done. if finished, end connection
        """
        data = self.sock.recv(MESSAGE_SIZE)
        if data:
            print(f"{self.name} got: {data.decode()}")
            self.reactor.unsubscribe(self.sock, 'read')
            if self.pings_sent < self.num_pings:
                self.reactor.subscribe(self.sock, 'write', self.send_ping)
            else:
                self.close_connection()
        else:
            self.close_connection()

    def handle_exception(self):
        """
        handle exceptions by closing socket
        """
        print(f"exception on socket {self.name} ")
        self.close_connection()

    def close_connection(self):
        self.reactor.unsubscribe(self.sock, 'read')
        self.reactor.unsubscribe(self.sock, 'write')
        self.reactor.unsubscribe(self.sock, 'except')
        self.sock.close()
        print(f"{self.name} closed connection")


if __name__ == '__main__':
    reactor = Reactor()
    server = Server(reactor)
    Client(reactor, 'Client 1', 6)
    Client(reactor, 'Client 2', 3)
    print("starting reactor")
    reactor.run()

