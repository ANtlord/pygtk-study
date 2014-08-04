#!/usr/bin/python
import socket,select
class ChatRoomServer:
    """
    Server variables
    """
    __server_connections = []
    __recv = 4096
    __port = 5234
    __socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    """
    Server routines
    """
    def __init__(self):
        print "Initializing ..."

        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__socket.bind(("0.0.0.0",self.__port))
        self.__socket.listen(10)
        print "Init complete! Chat server started on port "+str(self.__port)
        self.__server_connections.append(self.__socket)

    def broadcast_data (self, sock, message):
        for socket in self.__server_connections:
            if socket != self.__socket and socket != sock :
                try:
                    socket.send(message)
                except:
                    socket.close()
                    if(socket in self.__server_connections):
                        self.__server_connections.remove(socket) 

    def workloop(self):
        while 1:
            read_sockets,write_sockets,error_sockets = select.select(self.__server_connections,[],[])
            for sock in read_sockets:
                if sock == self.__socket:
                    sockfd, addr = self.__socket.accept()
                    self.__server_connections.append(sockfd)
                    print "Client (%s, %s) connected" % addr
                    self.broadcast_data(sockfd, "[%s:%s] entered room\n" % addr)
                else:
                    try:
                        data = sock.recv(self.__recv)
                        if data:
                            self.broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data) 
                    except:

                        self.broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                        print "Client (%s, %s) is offline" % addr
                        sock.close()
                        if(sock in self.__server_connections):
                            self.__server_connections.remove(sock)
                            continue
                 
         
     
if __name__ == "__main__":
    crs = ChatRoomServer()
    crs.workloop()
