import sys
from bitool import Magnet2Torrent, get_ips

#Downloads a torrent file from the magnet link and saves it as 'temp.torrent'
Magnet2Torrent.main(sys.argv[1])

#Parses `temp.torrent`, connects to trackers, and returns a list of peers with the torrent
ips = get_ips.run('temp.torrent')

print("Peers with the torrent: ", ips)
