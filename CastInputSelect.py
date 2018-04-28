import pychromecast
import eiscp

print "Finding Chromecasts..."
all_casts = pychromecast.get_chromecasts()

livingroom = next((x for x in all_casts if x.device.friendly_name == 'Living Room'), None)
if livingroom == None:
    print "Living Room Chromecast not found."
    exit(1)

livingroom.wait()
print "Connected to '{}' ({})".format(livingroom.name, livingroom.host)


print "Finding Onkyo receivers..."
all_receivers = eiscp.eISCP.discover()
if len(all_receivers) == 0:
    print "Receiver not found."
    exit(1)

receiver = all_receivers[0]
print "Connected to '{}' ({})".format(receiver.model_name, receiver.host)


def connected():
    # Power on receiver and select AUX channel
    print "Chromecast connected, sending wake up to {}".format(receiver.host)
    receiver.command('system-power=on')
    receiver.command('input-selector=aux1')

def disconnected():
    # Don't do anything on disconnection
    pass


def is_casting(media_status):
    return media_status.player_state != pychromecast.controllers.media.MEDIA_PLAYER_STATE_UNKNOWN
def is_connected(cast_status):
    return cast_status.session_id != None

class Listener:
    def __init__(self, cast):
        self.curr_is_connected = is_connected(cast.status)
        cast.register_status_listener(self)

    def new_cast_status(self, status):
        new_is_connected = is_connected(status)
        if not self.curr_is_connected and new_is_connected:
            connected()
        elif self.curr_is_connected and not new_is_connected:
            disconnected()
        
        self.curr_is_connected = new_is_connected

listener = Listener(livingroom)

print "Waiting for connections..."
livingroom.socket_client.join()
