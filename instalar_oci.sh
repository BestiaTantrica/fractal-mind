#!/bin/bash
# Script para instalar OCI CLI de forma silenciosa en Ubuntu
if ! command -v oci &> /dev/null; then
    bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)" -- --accept-all-defaults
fi
~/bin/oci --version
