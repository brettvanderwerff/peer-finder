import math
import os
import bencoder

def decode_file(file):
    '''
    Reads and decodes binary torrent file.
    '''
    full_path = os.path.abspath(file)
    with open(full_path, 'rb') as read_obj:
        decoded_file = bencoder.decode(read_obj.read())
    return decoded_file

def extract_crit_dat(decoded_file):
    '''Extracts the needed data from the decoded torrent file, stores in dictionary torrent_dat.
    '''
    torrent_dat = {}
    torrent_dat['trackers'] = decoded_file[b'announce-list'][0]
    torrent_dat['info'] = decoded_file[b'info']
    torrent_dat['name'] = decoded_file[b'info'][b'name'].decode('utf-8')

    try:
        torrent_dat['length'] = sum([item[b'length'] for item in decoded_file[b'info'][b'files']])

    except:
        torrent_dat['length'] = decoded_file[b'info'][b'length']

    try:
        torrent_dat['write_names'] = [item[b'path'][-1].decode('utf-8') for item in decoded_file[b'info'][b'files']]

    except:
        torrent_dat['write_names'] = [decoded_file[b'info'][b'name'].decode('utf-8').replace(' ', '_')]

    try:
        torrent_dat['write_lengths'] = [item[b'length'] for item in decoded_file[b'info'][b'files']]

    except:
        torrent_dat['write_lengths'] = [decoded_file[b'info'][b'length']]

    torrent_dat['write_data'] = zip(torrent_dat['write_names'], torrent_dat['write_lengths'])
    torrent_dat['pieces'] = decoded_file[b'info'][b'pieces']
    torrent_dat['piece_length'] = decoded_file[b'info'][b'piece length']
    torrent_dat['piece_count'] = math.ceil(torrent_dat['length'] / torrent_dat['piece_length'])
    return torrent_dat

def read_file(torrent_file):
    '''
    Main method.
    '''
    decoded_file = decode_file(torrent_file)
    return extract_crit_dat(decoded_file)