from charms.reactive import when, when_not, set_state
import miniupnpc

from charmhelpers.core import hookenv
import miniupnpc

open_port = hookenv.open_port
close_port = hookenv.close_port

config = hookenv.config()

def open_upnp_port(external_port):
    open_port(external_port)
    if config['enable-upnp']:
        try:
            upnp = miniupnpc.UPnP()
            upnp.discover()
            upnp.selectigd()
            upnp.addportmapping(external_port,'tcp',upnp.lanaddr,external_port,'juju expose upnp','')
        except Exception as e:
            hookenv.log('Upnp open failed: {}'.format(e.args[0]),'ERROR')
                    

def close_upnp_port(external_port):
    close_port(external_port)
    if config['enable-upnp']:
        try:
            upnp = miniupnpc.UPnP()
            upnp.discover()
            upnp.selectigd()
            upnp.deleteportmapping(external_port,'tcp')
        except Exception as e:
            hookenv.log('Upnp close failed: {}'.format(e.args[0]),'ERROR')

hookenv.open_port = open_upnp_port
hookenv.close_port = close_port

