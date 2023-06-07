from easysnmp import Session


# Polls the routers and returns a list of dictionaries
def poll_routers(router_ips, community):
    routers = []

    for router_ip in router_ips:
        session = Session(hostname=router_ip, community=community, version=2)

        sysname = session.get('sysName.0').value
        ip = session.get('ipAdEntAddr.1').value
        netmask = session.get('ipAdEntNetMask.1').value
        speed = session.get('ifSpeed.1').value
        discard = session.get('ifInDiscards.1').value
        loopback = session.get('ifType.1').value == 'softwareLoopback'
        down = session.get('ifOperStatus.1').value == 'down'

        router = {
            'sysname': sysname,
            'ip': ip,
            'netmask': netmask,
            'speed': speed,
            'discard': discard,
            'loopback': loopback,
            'down': down
        }

        routers.append(router)

    return routers
