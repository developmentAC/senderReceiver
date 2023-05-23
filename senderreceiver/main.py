#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import typer
from rich.console import Console

# ref: http://code.activestate.com/recipes/578802-send-messages-between-computers/
# binafry files:
# https://stackoverflow.com/questions/46979262/python-socket-how-to-send-a-file-to-another-computer-which-is-on-a-different-ne


# Setup
# Linux machines install ifconfig to get own ip address
# sudo apt-get install net-tools # necessary for ifconfig

# Install python virtual environment capabilities
# sudo apt install python3-pip # get pip3 # if needed to install tqdm

# Create a virtual environment
# python3 -m venv myvenv

# Activate virtual environment
# source myvenv/bin/activate

# Use pip to install necessary libraries
# python3 -m pip install tqdm
# pip3 install tqdm

# The tqdm package is for the download bar. Other ideas for bars may come from
# reference https://stackoverflow.com/questions/15644964/python-progress-bar-and-downloads

# install ifconfig capabilities
# sudo apt install net-tools

# Written by: Oliver Bonham-Carter
DATE = "22 May 2023"
VERSION = "iii"
AUTHOR = " Oliver Bonham-Carter"
AUTHORMAIL = "obonhamcarter@allegheny.edu"

# directories
OUTPUT_DIR = "0out/"  # all results are saved in this local directory

port = 5001


def bighelp():
    """Helper function"""
    h_str = "   " + DATE + " | version: " + VERSION + " |" + AUTHOR + " | " + AUTHORMAIL
    print("  " + len(h_str) * "-")
    print(h_str)
    print("  " + len(h_str) * "-")

    print("\n\tThe chat and file sending program between machines by IP.")
    platform_str = get_platformType()
    print("\n\t [+] OS type: ", platform_str)  # determine what the os is.
    # print("""\n\tLibrary installation notes:""")
    command_str = "USAGE: programName {s, r, sf, rf, sbf, rbf}"
    command_str = command_str + "\n\t [+] 'r' = receive and 's' = send"
    command_str = command_str + "\n\t [+] 'rf' = receive file and 'sf' = send file"
    command_str = (
        command_str + "\n\t [+] 'rbf' = receive bin file and 'sbf' = send bin file"
    )
    command_str = command_str + "\n\t  ex: send text: programName s remoteIP"
    command_str = command_str + "\n\t  ex:  rec text: programName r 0"
    command_str = command_str + "\n\t  ex: send bin file: programName sbf remoteIP file"
    command_str = command_str + "\n\t  ex:  rec bin file: programName rbf 0"

    if platform_str.lower() == "linux" or platform_str.lower() == "osx":
        print("\t [+] \U0001f600 ", command_str)
    else:
        print("\t [+] :-) ", command_str)
    #        print("\t+ OUTPUT directory (your output is placed here)  : ",OUTPUT_DIR)
    print("\n\t [+] Using port :", port)
    print("\t [+] My IP is :", getMyIP())


# end of bighelp()


def checkOUTPUT_DIR(dir_str):
    """Function to determine whether a data output directory exists. If the directory doesnt exist, then it is created"""
    try:
        os.makedirs(dir_str)
        # print("  PROBLEM: output_dir doesn't exist")
        print("\t [+] Creating :", dir_str)
        return 1

    except OSError:
        return 0


# end of checkOUTPUT_DIR()


def get_platformType():
    """Function to dermine the OS type."""
    platforms = {
        "darwin": "OSX",
        "win32": "Windows",
        "linux1": "Linux",
        "linux2": "Linux",
    }
    if sys.platform not in platforms:
        return sys.platform
    return platforms[sys.platform]


# end of get_platformType()


def sender(remoteIP):
    """text sending function"""
    # print("\t Remote IP is: ",remoteIP)
    myHost_str = getMyIP()  # "192.168.1.14"
    host = remoteIP  # "192.168.1.28" # the IP address of target computer
    addr = (host, port)
    UDPSock = socket(AF_INET, SOCK_DGRAM)
    print("\t [+] Sending to host: ", host)
    while True:
        #    data = raw_input("Enter message to send or type 'exit': ")
        data = input("Mesg to send or 'exit': ")
        metaData = data + "  : from " + myHost_str
        #    UDPSock.sendto(data.encode(), addr)
        UDPSock.sendto(metaData.encode(), addr)
        if data == "exit":
            break
    UDPSock.close()
    os._exit(0)


# end of sender()


def receiver():
    """text receiving function"""
    host = ""
    # port = 13000
    buf = 1024
    addr = (host, port)
    UDPSock = socket(AF_INET, SOCK_DGRAM)
    UDPSock.bind(addr)
    print("\t [+] Waiting to receive messages ...")
    while True:
        (data, addr) = UDPSock.recvfrom(buf)
        #    myStr = "Received message: ", data, addr
        myStr = str(data).replace("'", "")  # +" | "+ str(addr)
        myStr = noB(myStr)
        print("\a")
        print(" : ", myStr)
        #    if data == "exit":
        if "exit" in str(data):
            break
    UDPSock.close()
    os._exit(0)


# end of receiver()


def senderFile(remoteIP, fileName_str):
    """sending file function: sends text files as text"""
    # print("\t Remote IP is: ",remoteIP)
    myHost_str = getMyIP()  # "192.168.1.14"
    host = remoteIP  # "192.168.1.28" # the IP address of target computer
    # port = 13000
    addr = (host, port)
    UDPSock = socket(AF_INET, SOCK_DGRAM)
    print("\t [+] Sending File to host: ", host)
    datas = "fComing:" + fileName_str
    #    UDPSock.sendto(datas.encode(), addr) # send the file name first

    datas = datas + "|" + open(fileName_str, "r").read()

    UDPSock.sendto(datas.encode(), addr)

    UDPSock.close()
    print("\t + File :", fileName_str, "sent ...")
    os._exit(0)


# end of sender()


def senderBinFile(fileName_str, remoteIP, port):
    """
    Client that sends the file (uploads)
    sudo apt install python3-pip # get pip3
    Note: pip3 install tqdm
    """
    import socket

    # new and improved binary sending.
    host = remoteIP
    filename = fileName_str
    # def send_file(filename, host, port):

    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 1024 * 4  # 4KB

    # get the file size
    filesize = os.path.getsize(filename)
    # create the client socket
    s = socket.socket()
    print(f"\t [+] Attempting to connect to: {host}:{port}")
    try:
        s.connect((host, port))
        print("\t [+] Connected.")
    except ConnectionRefusedError:
        platform_str = get_platformType()
        print("\t [-] Connection refused.")
        if platform_str.lower() == "linux" or platform_str.lower() == "osx":
            print(
                "\n\t \U0001f5ff \U0001F608 Is the remote machine ready to receive? \U0001f5ff \U0001F608"
            )
        else:
            print("\t :-/ Is the remote machine ready to receive? :-/", command_str)
        exit()

    # send the filename and filesize
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())

    # start sending the file
    progress = tqdm.tqdm(
        range(filesize),
        f"\t Sending {filename}",
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    )
    with open(filename, "rb") as f:
        for _ in progress:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transmission for busy networks
            s.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))

    # close the socket
    s.close()


# end of senderBinFile()


def receiverBinFile():
    """
    Server receiver of the file
    """
    import socket

    SERVER_HOST = getMyIP()
    SERVER_PORT = port
    # filename = fileName_str

    # device's IP address

    # SERVER_HOST = "192.168.1.28"
    # SERVER_PORT = 5001
    # receive 4096 bytes each time
    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPARATOR>"
    # create the server socket
    # TCP socket
    s = socket.socket()
    # bind the socket to our local address
    s.bind((SERVER_HOST, SERVER_PORT))
    # enabling our server to accept connections
    # 5 here is the number of unaccepted connections that
    # the system will allow before refusing new connections
    s.listen(5)
    print(f"\t [*] Listening as {SERVER_HOST}:{SERVER_PORT}")
    # accept connection if there is any
    client_socket, address = s.accept()
    # if below code is executed, that means the sender is connected
    print(f"\t [+] {address} is connected.")

    # receive the file infos
    # receive using client socket, not server socket
    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    # remove absolute path if there is
    filename = os.path.basename(filename)
    # convert to integer
    filesize = int(filesize)
    # start receiving the file from the socket
    # and writing to the file stream
    progress = tqdm.tqdm(
        range(filesize),
        f"\t Receiving {filename}",
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    )
    with open(filename, "wb") as f:
        for _ in progress:
            # read 1024 bytes from the socket (receive)
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                # nothing is received
                # file transmitting is done
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))

    # close the client socket
    client_socket.close()
    # close the server socket
    s.close()


# end of receiverBinFile()


def receiverFile():
    # receiving file function
    host = ""
    buf = 1024
    addr = (host, port)
    UDPSock = socket(AF_INET, SOCK_DGRAM)
    UDPSock.bind(addr)
    print("\t + Waiting to receive files ...")
    while True:
        (data, addr) = UDPSock.recvfrom(buf)
        myStr = str(data).replace("'", "")  # +" | "+ str(addr)
        myStr = noB(myStr)
        # print("\a")
        # print(" : ",myStr)
        #    if data == "exit":
        if "exit" in str(data):
            break
        elif "fComing:" in str(data):
            #            fileName_str = myStr
            fileName_str = myStr[myStr.find(":") + 1 : myStr.find("|")]
            print("\n\t\a + Receiving a file.", fileName_str)
            fileData_str = myStr[myStr.find("|") + 1 :]
            print("\n\t Contents:", fileData_str)
            saveFile(fileName_str, fileData_str)
        # save the file

        else:
            print("\a")
            print(" : ", myStr)

    #            pass
    UDPSock.close()
    os._exit(0)


# end of receiver()


def saveFile(fileName_str, in_str):
    """saves the incoming text file"""
    checkOUTPUT_DIR(OUTPUT_DIR)
    fname = OUTPUT_DIR + fileName_str
    print("saveFile() :", fname)
    f = open(OUTPUT_DIR + fileName_str, "w")
    f.write(in_str)
    f.close()
    print("\n\t + File saved:", OUTPUT_DIR + fileName_str)


# end of saveFile()


def noB(in_str):
    """remove the b' text in encoded variables another option to use str() with, str(data, "utf-8")"""
    # ref: https://docs.python.org/3.4/library/socketserver.html#examples

    # print("noB says:", in_str)
    in_str = str(in_str)
    in_str = in_str[1:]
    return in_str


# end of noB()


def getMyIP():
    """Function to get ip of this local machine."""
    import socket

    hostname = socket.gethostname()
    myIP_str = socket.gethostbyname(hostname)
    # print(" Did we get the right IP? ", myIP_str)
    if "0.1.1" in myIP_str:  # need to do some system parsing to gegt ip
        #        print("\t+ Find your IP from the text below...")
        #        os.system("ifconfig")

        os.system("ifconfig > TextForIP_tmp.txt")
        myIPText_str = open("TextForIP_tmp.txt", "r").read()
        #        print("___________")
        #        print(myIPText_str)
        #        print("___________")
        os.system("rm TextForIP_tmp.txt")
        myIP_str = parser(myIPText_str, "192")
    return myIP_str


# end of getMyIP()


def parser(f, tag_str):
    '''Function to parse the the ipconfig data for inet (IP) details: looking for "192"'''
    # print(" parser()")
    #    f[f.find("192"):f.find("192") + 12
    return f[f.find(tag_str) : f.find(tag_str) + 12]


# end of parser()


# create a Typer object to support the command-line interface
cli = typer.Typer()


@cli.command()


#  def main(first: str = "", middle: str = "", last: str = ""): file: Path = typer.Option(None),
# def main(
#     link=typer.Option(None),
#     bighelp: bool = False,
#     biggerhelp: bool = False,
# ) -> None:


def main(
    task: str = "", remoteIP: str = "", fileName_str: str = "", bighelp: bool = False
):
    """Driver function"""
    print("\t Welcome to the chat program:")
    print("\t My IP is: ", getMyIP())
    print("\t Remote IP is: ", remoteIP)

    if task.lower() == "s":
        # print("\t sender()")
        sender(remoteIP)

    elif task.lower() == "r":
        # print("\t receiver()")
        receiver()

    elif task.lower() == "sf":
        # print("\t senderFile()")
        senderFile(remoteIP, fileName_str)

    elif task.lower() == "rf":
        # print("\t receiverFile()")
        receiverFile()

    elif task.lower() == "rbf":
        # print("\t receiverBinFile()")
        receiverBinFile()

    elif task.lower() == "sbf":
        # print("\t senderBinFile(fileName_str, remoteIP, port)")
        senderBinFile(fileName_str, remoteIP, port)

    ####

    else:
        # print("\t\n Unknown option ...",)
        platform_str = get_platformType()
        if platform_str.lower() == "linux" or platform_str.lower() == "osx":
            print("\n\t \U0001f5ff \U0001F608 Unknown option ... \U0001f5ff \U0001F608")
        else:
            print("\t+ :-/ ", command_str)
        exit()


# end of main()


###################################

import os, sys, socket, tqdm
from socket import *


# if __name__ == '__main__':

#         if len(sys.argv) == 2: # one parameter at command line
#             print("Please enter IP address as a parameter.")
#             sys.exit()
#         # note: the number of command line parameters is n + 1
#             main(sys.argv[1])#,sys.argv[3], sys.argv[4]),sys.argv[5])
#         elif len(sys.argv) == 3: # one parameter at command line
#             #print("three options")
#         # note: the number of command line parameters is n + 1
#             main(sys.argv[1],sys.argv[2])#,sys.argv[3], sys.argv[4]),sys.argv[5])
#         elif len(sys.argv) == 4: # one parameter at command line
#             #print("four options")
#         # note: the number of command line parameters is n + 1
#             main(sys.argv[1],sys.argv[2],sys.argv[3])#, sys.argv[4]),sys.argv[5])

#         else:
#             help()
#             sys.exit()
