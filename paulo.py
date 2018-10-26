#-------------------------------------------------------------------------------
# Name:        paulo
# Purpose:
#
# Author:      Paul
#
# Created:     25/10/2018
#-------------------------------------------------------------------------------

import socket
import time
from threading import Thread

class ClientThread(Thread):

    def __init__(self,ip,port,clientsocket):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] Nouveau thread démarré pour "+ip+":"+str(port),self.ident)
        # self.ident : pas de tid tant que le thread n'est pas démarré !
    def run(self):
        global threads
        while True:
            data = self.clientsocket.recv(1024)
            if data == b" ":
                self.clientsocket.send(data+bytes(str(self.port),'utf-8'))
                break
            print("données recues:", data, self.ident)
            for t in threads:
                if (t != self) : #t != threading.activeThread()
                    t.clientsocket.send(data)  # echo
        self.clientsocket.close()
        print("Fin service client "+ip+":"+str(self.port),self.ident)

TCP_IP = '0.0.0.0'
TCP_PORT = 5000
BUFFER_SIZE = 1024  # Normalement 1024, mais on veut une réponse rapide


tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(4)
    print("J'attends les clients...")
    (conn, (ip,port)) = tcpsock.accept()
    newthread = ClientThread(ip,port,conn)
    newthread.start()
    threads.append(newthread) # On les stocke au cas ou...
