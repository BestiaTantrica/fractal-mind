import oci
import time
import random
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# === CONFIGURACIÓN ===
CONFIG = {
    'user': os.getenv('OCI_USER_OCID'),
    'key_file': os.getenv('OCI_KEY_FILE'),
    'tenancy': os.getenv('OCI_TENANCY_OCID'),
    'region': os.getenv('OCI_REGION'),
    'fingerprint': os.getenv('OCI_FINGERPRINT')
}

STATUS_FILE = os.getenv('STATUS_FILE', 'cazador_status.json')
LOG_FILE = os.getenv('LOG_FILE', 'cazador.log')
SSH_PUB_KEY_FILE = os.getenv('SSH_PUB_KEY_FILE', 'ssh_for_arm.pub')

def log(mensaje):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    linea = f'[{timestamp}] {mensaje}\n'
    print(linea.strip())
    with open(LOG_FILE, 'a') as f:
        f.write(linea)

def actualizar_estado(intentos, ad_actual, estado, detalle=''):
    data = {
        'timestamp': datetime.now().isoformat(),
        'intentos': intentos,
        'zona_actual': ad_actual,
        'estado': estado,
        'detalle': detalle
    }
    with open(STATUS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def hunt():
    try:
        log('🔥 CAZADOR INICIADO - Conectando a Oracle Cloud...')
        compute = oci.core.ComputeClient(CONFIG)
        network = oci.core.VirtualNetworkClient(CONFIG)
        identity = oci.identity.IdentityClient(CONFIG)
        
        # Obtener ADs
        ads = identity.list_availability_domains(CONFIG['tenancy']).data
        log(f'📍 Detectados {len(ads)} dominios de disponibilidad')
        
        # Obtener infraestructura
        vcns = network.list_vcns(CONFIG['tenancy']).data
        if not vcns:
            log('❌ ERROR: No hay VCN configurada')
            return
            
        subnets = network.list_subnets(CONFIG['tenancy'], vcn_id=vcns[0].id).data
        if not subnets:
            log('❌ ERROR: No hay Subnet configurada')
            return
            
        subnet_id = subnets[0].id
        log(f'✅ Infraestructura lista: VCN={vcns[0].display_name}, Subnet={subnets[0].display_name}')
        
        # Imagen Ubuntu 22.04 aarch64 válida para Ashburn
        image_id = 'ocid1.image.oc1.iad.aaaaaaaa3axglz7hak6fmtcrpfckybc4j7zkausb4xpbqwbfypzfsto2pdmq'
        
        intentos = 0
        log('🏹 INICIANDO CAZA DE INSTANCIA ARM (4 OCPUs, 24GB RAM)')
        
        while True:
            intentos += 1
            ad_actual = random.choice(ads).name
            log(f'🎯 Intento #{intentos} - Probando {ad_actual}...')
            
            launch_details = oci.core.models.LaunchInstanceDetails(
                compartment_id=CONFIG['tenancy'],
                availability_domain=ad_actual,
                shape='VM.Standard.A1.Flex',
                shape_config=oci.core.models.LaunchInstanceShapeConfigDetails(
                    ocpus=4,
                    memory_in_gbs=24
                ),
                display_name=f'CAZADORA_ARM_{intentos}',
                image_id=image_id,
                create_vnic_details=oci.core.models.CreateVnicDetails(subnet_id=subnet_id),
                metadata={
                    'ssh_authorized_keys': open(SSH_PUB_KEY_FILE).read()
                }
            )
            
            try:
                actualizar_estado(intentos, ad_actual, 'CAZANDO', f'Probando {ad_actual}...')
                instance = compute.launch_instance(launch_details)
                
                # ¡ÉXITO!
                instance_id = instance.data.id
                log(f'✅✅✅ ¡ÉXITO! Instancia ARM creada: {instance_id}')
                actualizar_estado(intentos, ad_actual, 'ÉXITO', f'Instancia ARM creada: {instance_id}')
                break
                
            except oci.exceptions.ServiceError as e:
                if e.status == 429:
                    log('🚨 BLOQUEO DETECTADO (429 Too Many Requests) - Durmiendo 15 minutos...')
                    actualizar_estado(intentos, ad_actual, 'PÁNICO', 'Too Many Requests - Durmiendo 15 min')
                    time.sleep(900)
                elif 'capacity' in str(e).lower() or 'limit' in str(e).lower():
                    jitter = random.randint(20, 60)
                    log(f'⏳ {ad_actual} sin capacidad - Reintentando en {jitter}s')
                    actualizar_estado(intentos, ad_actual, 'CAZANDO', f'Sin capacidad, reintento en {jitter}s')
                    time.sleep(jitter)
                else:
                    log(f'❌ Error Inesperado: {e.message}')
                    actualizar_estado(intentos, ad_actual, 'ERROR', str(e.message))
                    time.sleep(30)
    
    except Exception as ex:
        log(f'💥 CRASH CRÍTICO: {str(ex)}')
        actualizar_estado(0, 'N/A', 'CRASH', str(ex))

if __name__ == "__main__":
    hunt()
