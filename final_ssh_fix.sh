#!/bin/bash
# final_ssh_fix.sh
OCID_CAZADORA="ocid1.instance.oc1.iad.anuwcljt7n2xbfycn2oklrfmx5evvezmnqggemlewt7vqzponxqwcccnlwba"
MAESTRA_PUB=$(cat ~/.ssh/id_rsa_maestra.pub)
OLD_KEY="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCazNwRumQiVvrLRZnrZGtF7/O+G59BERMt9TvmhOqVKR/Xc7CgnuxwqSiTYeFEpRKyJlEitLmOEGwenT9WpZ+xEiJyKQHcNhiEDQtQyxhoGudZ0YuZnVjKWh9Xr9CcuvO4H+7oacSdiTDCjr+nGuqda3lRLcKHq0CfX4igx4CBv1y6sSRVDMSYZnB4uzBpFN0/ifqvsJBnRHucM0v1sem8ZS3X+3b5EoevZqCAiCZlEVfhSBv457L1wcfcGYX1yFk4GbNhAs4KGY5hNgXgRt1F6SCYkPOUrvb0095V37bJ4oz7c0o1l0fo172bFjwLbdPTZ1vJSiVGz7+W+NTFe7hr ssh-key-2026-01-19"

# Combinamos con salto de linea literal
COMBINED="${OLD_KEY}\n${MAESTRA_PUB}"

echo "Actualizando metadatos en Oracle..."
~/bin/oci compute instance update --instance-id $OCID_CAZADORA --metadata "{\"ssh_authorized_keys\": \"$COMBINED\"}" --force
echo "Script finalizado."
