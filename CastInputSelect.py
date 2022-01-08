import sys
import pychromecast
import eiscp
import argparse
import logging


def find_chromecast(known_hosts):
    print("Finding Chromecasts...")
    casts, browser = pychromecast.get_listed_chromecasts(friendly_names=["Living Room"], known_hosts=known_hosts)
    #print(casts)
    browser.stop_discovery()

    if len(casts) == 0:
        print("Living Room Chromecast not found.")
        exit(1)
    livingroom = casts[0]

    livingroom.wait()
    lr_info = livingroom.cast_info
    print("Connected to {} '{}' ({})".format(lr_info.model_name, lr_info.friendly_name, lr_info.host))

    return livingroom


receiver = None
def find_receiver():
    print("Finding Onkyo receivers...")
    all_receivers = eiscp.eISCP.discover()
    if len(all_receivers) == 0:
        print("Receiver not found.")
        return

    global receiver
    receiver = all_receivers[0]
    print("Connected to '{}' ({})".format(receiver.model_name, receiver.host))


# Power on receiver and select AUX channel
def select_channel():
    if receiver == None:
        find_receiver()

    print("Sending channel select to {}".format(receiver.host))
    receiver.command('system-power=on')
    receiver.command('input-selector=aux1')


def connected():
    global receiver

    print("Chromecast connected")
    try:
        select_channel()
        return
    except:
        pass

    # Maybe we lost the connection? Try reconnecting.
    print("Channel select failed, attempting reconnect")
    try:
        receiver.disconnect()
        select_channel()
        return
    except:
        pass

    # Maybe the DHCP lease expired, so now we're on a different IP?
    print("Reconnect failed, attempting re-discovery")
    try:
        receiver = None
        select_channel()
    except:
        pass


def disconnected():
    # Don't do anything on disconnection
    print("ChromeCast disconnected")


def is_casting(media_status):
    return media_status.player_state != pychromecast.controllers.media.MEDIA_PLAYER_STATE_UNKNOWN
def is_connected(cast_status):
    return cast_status.session_id != None

class Listener:
    def __init__(self, cast):
        self.curr_is_connected = is_connected(cast.status)
        cast.register_status_listener(self)

    def new_cast_status(self, status):
        try:
            new_is_connected = is_connected(status)
            print("new_cast_status:")
            print("  " + str(status))
            print("  self.curr_is_connected = {}".format(self.curr_is_connected))
            print("  new_is_connected = {}".format(new_is_connected))
            if not self.curr_is_connected and new_is_connected:
                connected()
            elif self.curr_is_connected and not new_is_connected:
                disconnected()
            
            self.curr_is_connected = new_is_connected
        except:
            print("Unexpected error:", sys.exc_info()[0])


def parse_args():
    parser = argparse.ArgumentParser(
        description="Python script to switch receiver input when the Chromecast is connected to."
    )
    parser.add_argument(
        "--known-host",
        help="Add known chromecast IP. Can be used multiple times. Useful for debugging on Windows.",
        action="append",
    )
    parser.add_argument("--show-chromecast-debug", help="Enable pychromecast debug log", action="store_true")
    parser.add_argument("--show-zeroconf-debug", help="Enable zeroconf debug log", action="store_true")
    args = parser.parse_args()

    if args.show_chromecast_debug:
        logging.basicConfig(level=logging.DEBUG)
    if args.show_zeroconf_debug:
        print("Zeroconf version: " + zeroconf.__version__)
        logging.getLogger("zeroconf").setLevel(logging.DEBUG)

    return args


def main():
    args = parse_args()
    livingroom = find_chromecast(args.known_host)

    # Find receiver at startup to avoid delay on first connect
    find_receiver()

    listener = Listener(livingroom)

    print("Waiting for connections...")
    livingroom.socket_client.join()

main()