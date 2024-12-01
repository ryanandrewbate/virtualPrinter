#!/usr/bin/env
# -*- coding: utf-8 -*-
"""
We could use RedMon to redirect a port to a program, but the idea of
this file is to bypass that.

Instead, we simply set up a loopback ip and act like a network printer.
"""
import typing
import os
import time
import socket
import atexit
import select

#from virtualPrinter.windowsPrinters import WindowsPrinters

PrintCallbackDocType=typing.Any

PrintCallbackFunctionType=typing.Callable[[
    PrintCallbackDocType, # doc
    typing.Optional[str], # title
    typing.Optional[str], # author
    typing.Optional[str] # filename
    ],None
]

class PrintServer:
    """
    We could use RedMon to redirect a port to a program, but the idea of
    this file is to bypass that.

    Instead, we simply set up a loopback ip and act like a network printer.
    """

    def __init__(self,
        printerName:str='My Virtual Printer',
        ip:str='127.0.0.1',port:typing.Union[None,int,str]=None,
        printCallbackFn:typing.Optional[PrintCallbackFunctionType]=None):
        """
        You can do an ip other than 127.0.0.1 (localhost), but really
        a better way is to install the printer and use windows sharing.

        If you choose another port, you need to right click on your printer
        and go into properties->Ports->Configure Port
        and then change the port number.

        autoInstallPrinter is used to install the printer in the OS
        (currently only supports Windows)

        printCallbackFn is a function to be called with received print data
            if it is None, then will save it out to a file.
        """
        self.ip:str=ip
#        if port is None:
 #           port=0 # meaning, "any unused port"
        self.port:int=9101#int(port)
        self.buffersize:int=20  # Normally 1024, but we want fast response
        self.printerName:str=printerName
        self.running:bool=False
        self.keepGoing:bool=False
        #self.osPrinterManager:typing.Optional[WindowsPrinters]=None
        self.printerPortName:typing.Optional[str]=None
        self.printCallbackFn:typing.Optional[
            PrintCallbackFunctionType]=printCallbackFn

    def __del__(self):
        """
        Do some clean up when object is deleted
        """
        print("_del_ called")

   
    def run(self)->None:
        """
        server mainloop
        """
        if self.running:
            return
        self.running=True
        self.keepGoing=True
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.ip,self.port))
        ip,port=sock.getsockname()
        print(f'Opening {ip}:{port}')
        #sock.setblocking(0)
        sock.listen(1)
        #newWay=True
        buf:typing.List[str]
        while self.keepGoing:
            print('\nListening for incoming print job...')
            while self.keepGoing: # let select() yield some time to this thread
                #                   so we can detect ctrl+c and keep change
                inputready,outputready,exceptready= \
                    select.select([sock],[],[],1.0)
                _=outputready
                _=exceptready
                if sock in inputready:
                    break
            if not self.keepGoing:
                continue
            print('Incoming job... spooling...')
            conn,addr=sock.accept()
            _=addr # not used for now
            #        could be interesting for remote prints tho
            if self.printCallbackFn is not None:
                buf=[]
                while True:
                    raw=conn.recv(self.buffersize)
                    if not raw:
                        break
                    data=raw.decode('utf-8',errors='ignore')
                    buf.append(data)
                combinedBuf=''.join(buf)
                self.printCallbackFn(''.join(buf))
            else:
                print("No printCallbackFn")
            conn.close()
            time.sleep(0.1)


if __name__=='__main__':
    import sys
    port=9101
    ip='127.0.0.1'
    runit=True
    ps=PrintServer(ip=ip,port=port)
    ps.run()
