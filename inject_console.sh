#!/bin/bash
# Script PEGASO - Inyeccion via Consola Serie
OCID_INSTANCIA="ocid1.instance.oc1.iad.anuwcljt7n2xbfycn2oklrfmx5evvezmnqggemlewt7vqzponxqwcccnlwba"
ID_CONEXION="ocid1.instanceconsoleconnection.oc1.iad.anuwcljt7n2xbfycyhw4sf3hrnpje7h5ayfkxuqnes6jotrp5x5tg5obodfa"
REGION="us-ashburn-1"
MAESTRA_PUB_KEY=$(cat ~/.ssh/id_rsa_maestra.pub)

# Comando de conexion de consola serie
PROXY_CMD="ssh -i ~/.ssh/id_rsa_maestra -W %h:%p -p 443 ${ID_CONEXION}@instance-console.${REGION}.oci.oraclecloud.com"

echo "Intentando inyectar llave en la Cazadora (Consola Serie)..."

# Usamos SSH a traves de la conexión de consola serie
# La consola serie de OCI escucha en el puerto 443 via el ProxyCommand
ssh -i ~/.ssh/id_rsa_maestra -o StrictHostKeyChecking=no -o ProxyCommand="$PROXY_CMD" $OCID_INSTANCIA "mkdir -p ~/.ssh && echo '$MAESTRA_PUB_KEY' >> ~/.ssh/authorized_keys"

if [ $? -eq 0 ]; then
    echo "¡LLAVE INYECTADA CON EXITO!"
else
    echo "ERROR al inyectar la llave."
fi
