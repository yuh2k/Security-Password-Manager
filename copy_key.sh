cat ~/.ssh/id_rsa.pub | ssh bach@127.0.0.1 "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
