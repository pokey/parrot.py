from subprocess import PIPE, Popen
from config.config import *
from lib.modes.base_mode import *

class PokeyMode(BaseMode):
    patterns = [
        {
            'name': 'postalveolar_click',
            'sounds': ['Postalveolar click'],
            'threshold': {
                'percentage': 99.7,
                'power': 1000
            },
            'throttle': {
                'postalveolar_click': 0.07
            }
        },
        {
            'name': 'alveolar_click',
            'sounds': ['Alveolar click'],
            'threshold': {
                'probability': 0.99999,
                'power': 1000
            },
            'throttle': {
                'alveolar_click': 0.07
            }
        }
    ]
    
    def start(self): 
        self.talon_subprocess = Popen("/Users/pokey/.talon/bin/repl", stdin=PIPE)
        self.talon_subprocess.stdin.write(
            "from talon import actions\n".encode("utf-8")
        )
        self.talon_subprocess.stdin.flush()
        super().start()

    def handle_sounds( self, dataDicts ):
        for pattern in self.patterns:
            if( self.detect(pattern["name"]) ):
                self.talon_subprocess.stdin.write(
                    f"actions.user.{pattern['name']}()\n".encode("utf-8")
                )
                self.talon_subprocess.stdin.flush()
                break