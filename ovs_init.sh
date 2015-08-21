sudo ovsdb-server --remote=punix:/usr/local/var/run/openvswitch/db.sock \
             --remote=db:Open_vSwitch,Open_vSwitch,manager_options \
             --private-key=db:Open_vSwitch,SSL,private_key \
             --certificate=db:Open_vSwitch,SSL,certificate \
             --log-file=/var/log/openvswitch/ovs-vswitchd.log \
             --bootstrap-ca-cert=db:Open_vSwitch,SSL,ca_cert \
             -vsyslog:dbg -vfile:dbg --pidfile --detach
sudo ovs-vsctl --no-wait init
sudo ovs-vswitchd --pidfile --detach \
             --log-file=/var/log/openvswitch/ovs-vswitchd.log \
             -vconsole:err -vsyslog:info -vfile:info
