# peer_finder

Tool for getting a list of peers for bittorrent, built for Ubuntu 18.04 with Python 3.

Warning: A work in progress hobby project to learn low level network tools and multi-threading. 
Project is very incomplete and may be insecure use at your own risk.

## Installation

1. Clone repo

2. Install libtorrent and requirements

```commandline
$sudo apt-get install python3-libtorrent
$pip install -r requirements.txt

```

3. Run peer-finder by passing a magent link as a command line argument

```commandline
$python -m peer_finder "your magnet link in quotation here"
```

Credit to [LordAro](https://github.com/LordAro), [danfolkes](https://github.com/danfolkes) and their contributors for developing [Magnet2Torrent](https://github.com/LordAro/Magnet2Torrent), which this project uses a modified version of










