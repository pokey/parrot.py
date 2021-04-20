from lib.modes.base_talon_mode import BaseTalonMode

class PokeyMode(BaseTalonMode):
    patterns = [
        {
            'name': 'postalveolar_click',
            'sounds': ['Postalveolar click'],
            'threshold': {
                'probability': 0.99999,
                'power': 10000
            },
            'throttle': {
                'postalveolar_click': 0.15
            }
        },
        {
            'name': 'dental_click',
            'sounds': ['Dental click'],
            'threshold': {
                'probability': 0.99999,
                'power': 8000,
            },
            'throttle': {
                'dental_click': 0.07
            },
            
            # TODO: This doesn't do anything yet. Implement this by storing a
            # list of sounds that are in "limbo" waiting for their
            # ensureNotFollowedBy sound
            'ensureNotFollowedBy': {
                'suppress_clicks': 0.08
            }
        },
        {
            'name': 'suppress_clicks',
            'sounds': ['Speech'],
            'threshold': {
                'probability': 0.999,
                'power': 10000,
            },
            'throttle': {
                'dental_click': 0.1,
                'postalveolar_click': 0.1,
            },
            "sendToTalon": False
        },
    ]
