import socket
import threading

part = {} #{address: id} # enables to regain the chunks when a peer rejoins the connection
peer_data = {}

def get_id(addr)->int:
    if addr not in part:
        part[addr] = max(list(peer_data.keys()) + [0]) + 1
    return part[addr]

def handle_peer(conn, addr):
    with conn:
        host,port = addr

        peer_id = get_id(host)
        peer_data[peer_id] = {'address': (host, int(port)), 'id': peer_id}
        response = str(peer_data)
        conn.sendall(response.encode('utf-8'))

def tracker_server(host='127.0.0.1', port=65431):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Tracker listening on {host}:{port}")
        
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_peer, args=(conn, addr)).start()

if __name__ == "__main__":
    tracker_server()
