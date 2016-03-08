#!/bin/bash

apt-get update
apt-get upgrade -y
apt-get install -y build-essential git
apt-get install -y libfreetype6 libfreetype6-dev pkg-config
apt-get install -y python-dev python-pip

#apt-get install -y redis-server redis-tools
#pip install redis rq --upgrade

pip install six
pip install jinja2
pip install paramiko
pip install git+https://github.com/aristanetworks/arcomm.git

# install scipy stack
apt-get install -y python-numpy python-scipy python-matplotlib ipython \
    ipython-notebook python-pandas python-sympy python-nose

#cd /vagrant; python setup.py develop

# install/setup supporting services
apt-get install -y ntp dnsmasq tacacs+ nginx
apt-get install -y syslog-ng syslog-ng-core

if ! grep -q autotest /etc/hosts; then

    cat >> /etc/hosts <<EOF
192.168.56.7 shakedown
192.168.56.21 vswitch1
192.168.56.22 vswitch2
192.68.56.6 testrail
EOF

fi

cat > /etc/ntp.conf <<EOF
driftfile /var/lib/ntp/ntp.drift
statistics loopstats peerstats clockstats
filegen loopstats file loopstats type day enable
filegen peerstats file peerstats type day enable
filegen clockstats file clockstats type day enable
server 0.ubuntu.pool.ntp.org iburst
server 1.ubuntu.pool.ntp.org iburst
server 2.ubuntu.pool.ntp.org iburst
server 3.ubuntu.pool.ntp.org iburst
server ntp.ubuntu.com
restrict -4 default kod notrap nomodify nopeer noquery
restrict -6 default kod notrap nomodify nopeer noquery
restrict 127.0.0.1
restrict ::1
restrict 0.0.0.0 mask 0.0.0.0 modify notrap
EOF

cat > /etc/dnsmasq.d/local.conf <<EOF
local=/shakedown/
expand-hosts
domain=shakedown
EOF

cat > /etc/tacacs+/tac_plus.conf <<EOF
key = "shakedown"
accounting file = /var/log/tac_plus.acct

group = admins {
    default service = permit
    service = exec {
        priv-lvl = 15
    }
}

group = rousers {
    default service = permit
    service = exec {
        priv-lvl = 1
    }
}

user = admin {
    member = admins
    login = nopassword
}

user = shakedown {
    member = admins
    login = cleartext shakedown
}

user = rouser {
    member = rouser
    login = cleartext nocuser
}
EOF

cat > /etc/syslog-ng/conf.d/network.conf <<EOF
options { keep_hostname(yes); };
source s_net { tcp(); udp(); };
filter f_lessnoisy { not (
        message("LINEPROTO")
        or message("SPANTREE")
    );
};
destination d_net { file("/var/log/network"); };
# uncomment this line (and comment out the next one) to discard noisy logs messages
#log { source(s_net); filter(f_lessnoisy); destination(d_net); };
log { source(s_net); destination(d_net); };
EOF
