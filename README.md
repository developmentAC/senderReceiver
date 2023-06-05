# SenderReceiver

A Python socket-based instant messenger.

# Date

22 May 2023

This program uses [Poetry](https://python-poetry.org/docs/).

## Usage:

* Setup `poetry` from the `senderReceiver/` directory or where you are able to find the File `pyproject.toml`
   + `poetry install` 

Note: if there is an error when running the above command, try removing the File `poetry.lock`. Then rerun `poetry install`. 

* Get basic help
   + `poetry run senderreceiver --help`

* Get advanced help
   + `poetry run senderreceiver --bighelp`

* Receive Mode: Start a client to receive incoming messages and text files.
   + `poetry run senderreceiver --task r`

Note: the IP of the receiving machine will be displayed on the screen after this command has been executed. Working like a phone number, this IP number must be communicated to the sending machine in order for a message to be sent to the receiving machine. The IP number will be used with the parameter `--remoteip` on the sending machine.

* Send a chat message to another machine in receive mode
   + `poetry run senderreceiver --task s --remoteip 127.0.0.1` 

* Send a text file to another machine running in receive mode
   + `poetry run senderreceiver --task sf --remoteip 127.0.0.1 --filename myFile.md`

* Place a machine in receive mode for _binary_ files
   + `poetry run senderreceiver --task rbf`

* Send a binary file to another machine in binary receive mode.
   + `poetry run senderreceiver --task sbf --remoteip 127.0.0.1 --filename myFile.bin`

More documentation to come!!
