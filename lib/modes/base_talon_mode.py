from datetime import datetime
from os.path import expanduser
from subprocess import PIPE, Popen
from config.config import *
from lib.modes.base_mode import *
from abc import ABCMeta

class BaseTalonMode(BaseMode, metaclass=ABCMeta):
            
    def start(self): 
        talon_repl_path = expanduser("~/.talon/bin/repl")
        self.talon_subprocess = Popen([talon_repl_path, "-wr"], stdin=PIPE)
        super().start()

    def handle_sounds( self, dataDicts ):
        for pattern in self.patterns:
            if( self.detect(pattern["name"]) ):
                if ("sendToTalon" in pattern and pattern["sendToTalon"] == False):
                    continue
                print(f"{datetime.utcnow().isoformat()}: Sending {pattern['name']} to talon.")
                self.talon_subprocess.stdin.write(
                    f"actions.user.{pattern['name']}()\n".encode("utf-8")
                )
                self.talon_subprocess.stdin.flush()