# Estrategia de prueba para el log
def check_buy(dataframe: pd.DataFrame) -> str:
    """
    Verifica si el precio de cierre es mayor que el promedio móvil exponencial (EMA).
    
    Args:
    dataframe (pd.DataFrame): DataFrame con los datos de precios.
    
    Returns:
    str: "buy" si el precio de cierre es mayor que el EMA, "wait" en caso contrario.
    """
    if dataframe['close'].iloc[-1] > dataframe['ema'].iloc[-1]:
        return "buy"
    return "wait"