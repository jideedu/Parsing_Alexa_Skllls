from vpnocchio import VPN, init_logging
from threading import Thread

init_logging()

# set your dir with ovpn files, default is:
VPN.conf_dir = './ovpn_tcp'
# set minimum seconds must elapse between reconnects
VPN.min_time_before_reconnect = 10

credentials = [('guillermo.suarez.tangil@gmail.com', 'tcFI+9cyjOE2','')]

def do_something(*args):
    vpn = VPN(*args)
    for one in range(2):
        # it has requests inside
        response = vpn.get('http://ip.barjomet.com')
        vpn.log.info('Hooray, here is desired data: %s',  response.text)
        vpn.new_ip()
    vpn.disconnect() 

for username, password, match_config_name in credentials:
    Thread(target=do_something,
           args=(username,
                 password,
                 match_config_name)).start()