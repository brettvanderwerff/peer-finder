from bitool import find_tracker_connect, torrent_file_reader
import socket
import struct
import random
import hashlib
import bencoder
import binascii


def parse_trackers(torrent_dat):
    '''
    Parses trackers from the decoded torrent file, extracts the url and port number for each tracker.
    '''
    tracker_list = []
    tracker_list.append(('tracker.coppersurfer.tk', 6969))  # Use known to work tracker first

    for tracker in torrent_dat['trackers']:
        tracker = tracker.decode('utf-8').split('://')[-1]
        tracker_split = tracker.split(":")
        tracker_url = tracker_split[0]
        slash_position = tracker_split[1].find('/')
        tracker_port = int(tracker.split(":")[1][:slash_position])
        tracker_list.append((tracker_url, tracker_port))

    return tracker_list

def build_request():
    '''
    Builds a request to connnect to tracker.
    '''
    protocol_id = 0x41727101980
    action = 0
    transaction_id = random.randrange(1, 1000)
    request = struct.pack(">qii", protocol_id, action, transaction_id)
    return request

def gen_hash(torrent_dat):
    '''
    Generated SHA1 hash based on the 'info' section of the magnet link data.
    '''
    info = torrent_dat['info']
    encoded_info = bencoder.encode(info)
    return hashlib.sha1(encoded_info)

def gen_peer_id():
    '''
    Generates peer ID according to conventions at: http://www.bittorrent.org/beps/bep_0020.html
    '''
    peer_id = ['-AZ2060-']
    for i in range(12):
        peer_id.append(str(random.randrange(1, 9)))
    return bytearray(''.join(peer_id), 'utf-8')

def build_announce_req(connection_id, hash, peer_id, torrent_dat):
    '''
    Builds an announce request to get a peer list from the tracker.
    '''
    binary_hash = binascii.a2b_hex(hash.hexdigest())
    action = 1
    transaction_id = random.randrange(1, 1000)
    downloaded = 0
    uploaded = 0
    event = 0
    ip = 0
    left = torrent_dat['length']
    key = random.randrange(1, 1000)
    num_want = -1
    port = 6681
    request = struct.pack(">qii20s20sqqqiiiih",
                         connection_id,
                         action,
                         transaction_id,
                         binary_hash,
                         peer_id,
                         downloaded,
                         left,
                         uploaded,
                         event,
                         ip,
                         key,
                         num_want,
                         port)
    return request


def communicate_DGRAM(target, message):
    '''
    Primary function for sending and receiving information with tracker via DGRAM.
    '''
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    sock.settimeout(15)
    sock.connect(target)
    sock.send(message)
    response = sock.recv(4096)
    sock.close()
    return response

def get_connection_id(response):
    '''Gets the connection ID from the tracker response.
    '''
    unpacked_response = struct.unpack(">iiq", response)
    connection_id = unpacked_response[2]
    return connection_id


def connect_tracker(tracker, request, hash, peer_id, torrent_dat):
    '''
    Connects to each tracker in the tracker_list, if tracker connects will return a response that contains a list
    of IP addresses for potential peers.
    '''
    response = communicate_DGRAM(tracker, request)
    connection_id = get_connection_id(response)
    announce_req = build_announce_req(connection_id, hash, peer_id, torrent_dat) #ToDo fix nested argument
    print('Receiving list of peers..')
    response = communicate_DGRAM(tracker, announce_req)
    return response


def parse_ips(response):
    '''
    Parses response from tracker and unpacks the encoded IP addresses and Ports.
    '''
    ips_ports = []
    for offset in range(20, len(response), 6):
        raw_ip = struct.unpack_from(">BBBB", response, offset)
        ip = '.'.join([str(i) for i in raw_ip])
        port = struct.unpack_from(">H", response, offset + 4)[0]
        ips_ports.append((ip, port))
    print("Peer list received")
    return ips_ports


def run(torrent_file):
    '''
    Main function connects to trackers to get ip addresses. Loops until successful.
    '''
    torrent_dat = torrent_file_reader.read_file(torrent_file)
    tracker_list = parse_trackers(torrent_dat)

    while True:
        try:
            tracker = find_tracker_connect.run(tracker_list)
            request = build_request()
            hash = gen_hash(torrent_dat)
            peer_id = gen_peer_id()
            response = connect_tracker(tracker, request, hash, peer_id, torrent_dat)
            return parse_ips(response)
        except socket.error:
            continue







