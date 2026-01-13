# 📊 Tier System Sniper V5 (Validación de Robustez)

## 🎯 OBJETIVO
Categorizar los 80 pares de Binance Futuros para aplicar una gestión de riesgo asimétrica.

## 🧱 ESTRUCTURA DE CAPAS (TIERS)

### 🔵 TIER 1: HIGH LIQUIDITY (Top 20 Market Cap)
* Pares: BTC, ETH, SOL, BNB, XRP.
* Config: Stoploss 33.8% | Trailing Offset 25% | Stake: 15%.
* Lógica: Captura de tendencia macro.

### 🟡 TIER 2: MID CAPS (Volumen > $50M/24h)
* Pares: LINK, ADA, DOT, MATIC.
* Config: Stoploss 20% | Trailing Offset 15% | Stake: 10%.

### 🔴 TIER 3: SMALL CAPS / VOLATILE (Volumen < $50M/24h)
* Pares: Altcoins de baja capitalización.
* Config: Stoploss 10% | Trailing Offset 10% | Stake: 5%.
* Lógica: Entradas rápidas Sniper con filtro de ADX.
