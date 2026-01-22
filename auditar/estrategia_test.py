# Estrategia de prueba para el log
def check_buy(dataframe):
    if dataframe['close'] > dataframe['ema']:
        return "buy"
    return "wait"
