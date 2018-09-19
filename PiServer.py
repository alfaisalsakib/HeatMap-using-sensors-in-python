import socket
import time

def Server():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    s.bind(('192.168.0.3',5000)) #the server address and port

    s.listen(1)
    conn,addr=s.accept()
    
    graph_data = open('example.txt','r+').read()
    lines = graph_data.split('\n')

    for line in lines:
        val = input()
        if len(line) > 1:
            x, y, v = val.split(',')
           
            conn.send(x.encode()+str(',').encode()+y.encode()+str(',').encode()+v.encode()+str('\n').encode())
            print("server Send : " + x + y + v)
            
        time.sleep(.4)
        
    conn.close()
    
Server()
