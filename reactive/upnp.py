import miniupnpc
from charmhelpers.core import hookenv

open_port = hookenv.open_port
close_port = hookenv.close_port

config = hookenv.config()


def open_upnp_port(external_port):
    open_port(external_port)
    external_port = int(external_port)
    if config['enable-upnp']:
        try:
            upnp = miniupnpc.UPnP()
            upnp.discover()
            upnp.selectigd()
            message = "layer-upnp unit {}".format(hookenv.local_unit())
            if upnp.addportmapping(external_port, 'tcp', upnp.lanaddr, external_port, message, ''):
                hookenv.log('Upnp open successful: {}'.format(external_port), 'INFO')
            else:
                hookenv.log('Upnp open failed: {}'.format(external_port), 'WARNING')
        except Exception as e:
            hookenv.log('Upnp open error: {}'.format(e.args[0]), 'ERROR')
            raise


def close_upnp_port(external_port):
    close_port(external_port)
    external_port = int(external_port)
    if config['enable-upnp']:
        try:
            upnp = miniupnpc.UPnP()
            upnp.discover()
            upnp.selectigd()
            if upnp.deleteportmapping(external_port, 'tcp'):
                hookenv.log('Upnp close successful: {}'.format(external_port), 'INFO')
            else:
                hookenv.log('Upnp close failed: {}'.format(external_port), 'WARNING')
        except Exception as e:
            hookenv.log('Upnp close error: {}'.format(e.args[0]), 'ERROR')
            raise


hookenv.open_port = open_upnp_port
hookenv.close_port = close_upnp_port
