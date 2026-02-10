#!/bin/bash
# Script nativo de Maestra para arreglar acceso a Cazadora
OCID_CAZADORA="ocid1.instance.oc1.iad.anuwcljt7n2xbfycn2oklrfmx5evvezmnqggemlewt7vqzponxqwcccnlwba"
MAESTRA_PUB_KEY=$(cat ~/.ssh/id_rsa_maestra.pub)

echo "Buscando llaves actuales..."
CURRENT_KEYS=$(~/bin/oci compute instance get --instance-id $OCID_CAZADORA --query 'data.metadata."ssh_authorized_keys"' --raw-output)

if [[ "$CURRENT_KEYS" == *"$MAESTRA_PUB_KEY"* ]]; then
    echo "¡Listo! La llave ya esta en los metadatos."
else
    echo "Agregando llave de Maestra a Cazadora..."
    NEW_KEYS="${CURRENT_KEYS}\n${MAESTRA_PUB_KEY}"
    ~/bin/oci compute instance update --instance-id $OCID_CAZADORA --metadata "{\"ssh_authorized_keys\": \"${NEW_KEYS}\"}" --force
    echo "Actualizacion enviada a Oracle."
fi
