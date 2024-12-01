#!/usr/bin/env
# -*- coding: utf-8 -*-
"""
Simply send in the options you want in Printer.__init__
and then override printThis() to do what you want.
DONE!
Ready to run it with run()
"""
import typing
import os
import sys
import subprocess

from printServer import PrintCallbackDocType
from printerException import PrinterException


# find a good shell_escape routine
try:
    import shlex
    if hasattr(shlex,'quote'):
        shell_escape=shlex.quote
    else:
        import pipes # pylint: disable=deprecated-module
        shell_escape=pipes.quote
except ImportError:
    import pipes # pylint: disable=deprecated-module
    shell_escape=pipes.quote


class Printer:
    """
    You can derive from this class to create your own printer!

    Simply send in the options you want in Printer.__init__
    and then override printThis() to do what you want.
    DONE!
    Ready to run it with run()
    """

    def __init__(self,
        name:str='My Virtual Printer'
        ):
        """
        name - the name of the printer to be installed

        acceptsFormat - the format that the printThis() method accepts
        Available formats are "pdf", or "png" (default=png)

        acceptsColors - the color format that the printThis() method accepts
        (if relevent to acceptsFormat)
        Available colors are "grey", "rgb", or "rgba" (default=rgba)
        """
        from printServer import PrintServer
        self._server:typing.Optional[PrintServer]=None
        self.name:str=name

    def printThis(self,
        doc:PrintCallbackDocType,
        )->None:
        ### doc is the data
            print("printThis called")

    def run(self,
        host:str='127.0.0.1',
        port:typing.Union[None,int,str]=None,
        )->None:
        from printServer import PrintServer
        self._server=PrintServer(
            self.name,host,port,
            self._printServerCallback)
        self._server.run()
        del self._server # delete it so it gets un-registered
        self._server=None

    def _printServerCallback(self,
        dataSource:PrintCallbackDocType
        ):
        """
        Default callback, turns around and calls
        printPostscript() with the data given to it
        """
        print("here is the text:")
        print(dataSource)
        #self.printPostscript(dataSource,False,title,author,filename)
        ### here is dataSource



if __name__=='__main__':
        p=Printer()
        p.run()
        
