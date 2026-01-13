# 📊 Tier System Sniper V5 (Lógica de Volumen y Tiempo)

## 🧱 FILTROS DE EJECUCIÓN (MIRA AJUSTADA)
- **Time-Out Exit (Tier 3):** Si el trade no es positivo en 20 min, cerrar por mercado.
- **No Reverse (Flip):** Prohibido revertir posición en capas volátiles para evitar el doble slippage.
- **Trigger de Volumen:** Entrar solo si $V_{actual} > 2.5 \times V_{promedio\_4h}$.

## 🧱 CATEGORIZACIÓN DE PARES
### 🔵 TIER 1 (Alta Cap): BTC, ETH, SOL, BNB.
- Estrategia: Trend Following. Stoploss 33.8%.

### 🟡 TIER 2 (Media Cap): LINK, ADA, DOT, MATIC, XRP.
- Estrategia: Mean Reversion. Stoploss 20%.

### 🔴 TIER 3 (Baja Cap): Resto de los 80 pares.
- Estrategia: Momentum Scalping. Stake mínimo.
