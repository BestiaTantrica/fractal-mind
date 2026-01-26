# Idea de Tomás

## Entrada:
version: '3'
services:
  freqtrade:
    image: freqtradeorg/freqtrade:stable
    restart: always
    container_name: ft_bestia
    volumes:
      - "./user_data:/freqtrade/user_data"
      - "./config.json:/freqtrade/config.json"
    # Limitamos la memoria para no saturar el GB de la instancia
    deploy:
      resources:
        limits:
          memory: 512M
    command: >
      trade
      --config /freqtrade/config.json
      --strategy FractalAggressiveV12

## Respuesta Mente:
**CÓDIGO PROCESADO: OPTIMIZACIÓN Y ESTANDARIZACIÓN**

Tomás. El vómito es un `docker-compose.yml` funcional, pero ineficiente en la gestión de recursos para un entorno de instancia única.

**Análisis de Defectos:**
1.  **`deploy` block:** Uso de sintaxis `deploy` (típicamente para Docker Swarm) en lugar de la sintaxis estándar de recursos (`mem_limit`, `mem_reservation`) para contenedores únicos.
2.  **Contexto faltante:** Ausencia de variables de entorno cruciales (`TZ`) y puertos estándar para la API/UI (incluso si no se usan, deben estar mapeados o comentados).

**Resultado: `docker-compose.optimized.yml`**

```yaml
# FILE: docker-compose.optimized.yml
# PROJECT: ft_bestia_fractal_aggressive

version: '3.7' # Versión específica para gestión avanzada de recursos.

services:
  freqtrade:
    # --- CONFIGURACIÓN BASE ---
    image: freqtradeorg/freqtrade:stable
    restart: always
    container_name: ft_bestia

    # --- ENTORNO ---
    environment:
      # Definición obligatoria de Timezone para la gestión de backtesting y horarios de exchange.
      - TZ=America/Santiago # AJUSTAR: Establece la zona horaria operacional.
      # Para utilizar PostgreSQL externo, descomentar y configurar.
      # - FT_DATABASE_URL=postgresql://user:password@host:5432/freqtrade

    # --- VOLÚMENES Y PERSISTENCIA ---
    volumes:
      - "./user_data:/freqtrade/user_data" # Datos, logs, estrategias.
      - "./config.json:/freqtrade/config.json" # Fichero de configuración principal.

    # --- RECURSOS Y LÍMITES (OPTIMIZACIÓN DE MEMORIA) ---
    # Eliminamos el bloque 'deploy' (orientado a Swarm) y usamos límites directos.
    # Esto asegura que el kernel de Docker respete los límites de la instancia.
    mem_limit: 512M       # Límite duro (igual que el input).
    mem_reservation: 384M # Memoria mínima garantizada para evitar 'swapping' agresivo.

    # --- PUERTOS (API/UI) ---
    # Por defecto, se asume ejecución en modo trade sin UI. Descomentar si se usa la API.
    # ports:
    #   - "8080:8080" # API Freqtrade.

    # --- COMANDO DE EJECUCIÓN ---
    # Ejecución en modo 'trade' con la estrategia solicitada.
    command: >
      trade
      --config /freqtrade/config.json
      --strategy FractalAggressiveV12
```

---

### **RESUMEN TÉCNICO DE MODIFICACIONES**

| Componente | Ajuste/Estado | Justificación |
| :--- | :--- | :--- |
| **`version`** | Elevada a `3.7` | Mejor soporte para sintaxis de recursos avanzada. |
| **Recursos** | Reemplazo de `deploy` | Se ha implementado `mem_limit` y `mem_reservation` directamente bajo `freqtrade`. Esto es el estándar para control de recursos en Docker Standalone/Compose, garantizando la estabilidad dentro del límite de 1GB. |
| **`environment`** | Adición de `TZ` | **CRÍTICO.** La gestión horaria y de *candles* depende de una zona horaria definida. Se requiere ajuste manual. |
| **`ports`** | Comentados | Incluidos como *boilerplate* para futura habilitación de la API/UI. |
| **Estrategia** | Mantenida | Se mantiene la directriz operativa: `--strategy FractalAggressiveV12`. |