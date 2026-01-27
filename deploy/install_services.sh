#!/bin/bash
# Script para instalar y activar los servicios de los bots en AWS EC2 (Amazon Linux 2023 / AL2)

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Iniciando instalación de servicios Fractal Mind...${NC}"

# Verificar si los archivos de servicio existen en el directorio actual
if [ ! -f "bot-fractal.service" ] || [ ! -f "bot-air.service" ]; then
    echo -e "${RED}Error: No se encuentran los archivos .service en el directorio actual.${NC}"
    echo "Asegurate de estar en la carpeta 'deploy/' del repositorio."
    exit 1
fi

# Copiar archivos a systemd
echo "Copiando archivos de servicio a /etc/systemd/system/..."
sudo cp bot-fractal.service /etc/systemd/system/
sudo cp bot-air.service /etc/systemd/system/

# Recargar daemon
echo "Recargando systemd daemon..."
sudo systemctl daemon-reload

# Habilitar servicios (arrancan al inicio)
echo "Habilitando servicios para inicio automático..."
sudo systemctl enable bot-fractal
sudo systemctl enable bot-air

# Reiniciar servicios para aplicar cambios
echo "Reiniciando servicios..."
sudo systemctl restart bot-fractal
sudo systemctl restart bot-air

# Verificar estado
echo -e "${GREEN}Estado de bot-fractal:${NC}"
sudo systemctl status bot-fractal --no-pager | head -n 10

echo -e "${GREEN}Estado de bot-air:${NC}"
sudo systemctl status bot-air --no-pager | head -n 10

echo -e "${GREEN}Instalación completada. Los bots deberían estar corriendo y protegidos ante reinicios.${NC}"
