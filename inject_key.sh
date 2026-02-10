#!/bin/bash
# Script PEGASO V3 - Append de llaves
OCID="ocid1.instance.oc1.iad.anuwcljt7n2xbfycn2oklrfmx5evvezmnqggemlewt7vqzponxqwcccnlwba"
MAESTRA_KEY_FILE="/home/ubuntu/.ssh/id_rsa_maestra.pub"

# Llave original detectada en el panel
ORIGINAL_KEY="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCazNwRumQiVvrLRZnrZGtF7/O+G59BERMt9TvmhOqVKR/Xc7CgnuxwqSiTYeFEpRKyJlEitLmOEGwenT9WpZ+xEiJyKQHcNhiEDQtQyxhoGudZ0YuZnVjKWh9Xr9CcuvO4H+7oacSdiTDCjr+nGuqda3lRLcKHq0CfX4igx4CBv1y6sSRVDMSYZnB4uzBpFN0/ifqvsJBnRHucM0v1sem8ZS3X+3b5EoevZqCAiCZlEVfhSBv457L1wcfcGYX1yFk4GbNhAs4KGY5hNgXgRt1F6SCYkPOUrvb0095V37bJ4oz7c0o1l0fo172bFjwLbdPTZ1vJSiVGz7+W+NTFe7hr ssh-key-2026-01-19"

if [ ! -f "$MAESTRA_KEY_FILE" ]; then
    echo "ERROR: No se encontro la llave publica Maestra"
    exit 1
fi

MAESTRA_KEY=$(cat "$MAESTRA_KEY_FILE" | tr -d '\n')

# Combinar con un salto de linea entre ellas
COMBINED_KEYS="${ORIGINAL_KEY}\n${MAESTRA_KEY}"

# Crear JSON
echo "{\"ssh_authorized_keys\": \"$COMBINED_KEYS\"}" > metadata.json

# Actualizar en Oracle
~/bin/oci compute instance update --instance-id $OCID --metadata file://metadata.json --force
