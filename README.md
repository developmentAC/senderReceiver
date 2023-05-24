# SenderReceiver

A Python socket-based instant messenger.

# Date

22 May 2023

This program uses [Poetry](https://python-poetry.org/docs/).

## Usage:

* Setup `poetry` from the `senderReceiver/` directory or where you are able to find the File `pyproject.toml`
   + `poetry install`

* Get basic help
   + `poetry run senderreceiver --help`
* Get advanced help
   + `poetry run senderreceiver --bighelp`

* Receive Mode: Start a client to receive incoming messages and text files.
   + `poetry run senderreceiver --task r`

* Send a chat message to another machine in receive mode
   + `poetry run senderreceiver --task s --remoteip 127.0.0.1` 

* Send a text file to another machine running in receive mode
   + `poetry run senderreceiver --task sf --remoteip 127.0.0.1 --filename myFile.md`

* Place a machine in receive mode for _binary_ files
   + `poetry run senderreceiver --task rbf`

* Send a binary file to another machine in binary receive mode.
   + `poetry run senderreceiver --bighelp --task sbf --remoteip 127.0.0.1 --filename myFile.bin`

More documentation to come!!
