#!/bin/bash
# final_oci_fix.sh
# Ejecutar en la Torre Maestra para arreglar el acceso a la Cazadora
OCID="ocid1.instance.oc1.iad.anuwcljt7n2xbfycn2oklrfmx5evvezmnqggemlewt7vqzponxqwcccnlwba"
MAESTRA_PUB_FILE="$HOME/.ssh/id_rsa_maestra.pub"

if [ ! -f "$MAESTRA_PUB_FILE" ]; then
    echo "ERROR: No se encontró la llave publica Maestra en $MAESTRA_PUB_FILE"
    exit 1
fi

echo "Leyendo llaves actuales de la Cazadora..."
OLD_KEY=$(~/bin/oci compute instance get --instance-id $OCID --query 'data.metadata."ssh_authorized_keys"' --raw-output)
NEW_PUb=$(cat "$MAESTRA_PUB_FILE")

# Construir el JSON de metadatos combinando las llaves
# Oracle requiere que se manden todas las autorizadas en una sola cadena
COMBINED_KEYS="${OLD_KEY}\n${NEW_PUb}"

echo "Generando archivo de metadatos..."
python3 -c "
import json, sys
data = {'ssh_authorized_keys': sys.argv[1].replace('\\\\n', '\\n')}
print(json.dumps(data))
" "$COMBINED_KEYS" > metadata_fix.json

echo "Enviando actualización a Oracle Cloud..."
~/bin/oci compute instance update --instance-id $OCID --metadata file://metadata_fix.json --force

if [ $? -eq 0 ]; then
    echo "¡Actualización completada exitosamente!"
    echo "Probando conexión SSH a la Cazadora..."
    ssh -i ~/.ssh/id_rsa_maestra -o StrictHostKeyChecking=no ubuntu@129.80.32.115 "hostname && whoami"
else
    echo "ERROR: Falló la actualización de metadatos."
    exit 1
fi
