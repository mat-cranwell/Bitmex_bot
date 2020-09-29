# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 15:18:45 2020

@author: m052366
"""


def get_data(periods = 50, bin_size = '1m'):
    number_of_minutes_needed = periods
    past_minutes_data_list = []
    past_minutes_data = client.Trade.Trade_getBucketed(binSize=bin_size, count=number_of_minutes_needed, symbol=symbol, reverse=True).result()[0]
    past_minutes_data = reversed(past_minutes_data)
    for past_minute_data in past_minutes_data:
        processed_min_data = {}
        timestamp_minute = str(past_minute_data["timestamp"]).split(':')[0] + ":" + str(past_minute_data["timestamp"]).split(':')[1] + ":00"
    
        processed_min_data["symbol"] = past_minute_data["symbol"]
        processed_min_data["Date"] = timestamp_minute
        processed_min_data["Open"] = past_minute_data["open"]
        processed_min_data["Close"] = past_minute_data["close"]
        processed_min_data["Volume"] = past_minute_data["volume"]
        processed_min_data["High"] = past_minute_data["high"]
        processed_min_data["Low"] = past_minute_data["low"]
        past_minutes_data_list.append(processed_min_data)
        
        return pd.DataFrame(processed_min_data)
    
def strategy():
    df = get_data(50, '1m')
    df['ma'] = df.Close.rolling(50).mean()
    z = np.ln(df.Close.tail(1) / df.ma.tail(1))
    
    if z <= - 0.01:
        return 1
    if z >= 0.01:
        return -1 
    else:
        return 0 
    
def check_pos():
    positions = client.Position.Position_get(filter=json.dumps({"symbol": symbol})).result()[0][0]
    # processed_position = {}
    # timestamp_minute = str(positions["timestamp"]).split(':')[0] + ":" + \
    #                    str(positions["timestamp"]).split(':')[1] + ":00"
    
    # processed_position["symbol"] = positions["symbol"]
    # processed_position["timestamp"] = timestamp_minute
    # processed_position["isOpen"] = positions["isOpen"]
    # processed_position["currentQty"] = positions["currentQty"]
    # processed_position["leverage"] = positions["leverage"]
    # processed_position["liquidationPrice"] = positions["liquidationPrice"]
    
    possy = positions["currentQty"]
    
    if possy > 0:
        return 1
    if possy < 0:
        return -1
    else:
        return 0
    
def Trader():
    symbol = 'XBTUSD'
    ordType = 'Market'
    orderQty_Buy = 10 # Positive value to long
    orderQty_Sell = -10 # Negative value to short
    prediction = strategy()
    pos = check_pos()
    print ('prediction: ', prediction())
    print ('position: ', pos)
    if pos == 0:
        if pred == 1:
            print ('Buying...')
            client.Order.Order_new(symbol=symbol, ordType=ordType, orderQty=orderQty_Buy).result() # Long
        if pred == -1:
            print ('Selling...')
            client.Order.Order_new(symbol=symbol, ordType=ordType, orderQty=orderQty_Sell).result() # Short
            
    if pos == 1:
        if pred == 1:
            print ('Holding...')
        if pred == 0:
            print ('Holding...')
        if pred ==-1:
            #close position
            print ('Closing position...')
            client.Order.Order_closePosition(symbol=symbol).result()
            #short
            print ('Selling...')
            client.Order.Order_new(symbol=symbol, ordType=ordType, orderQty=orderQty_Sell).result()
    if pos == -1:
        if pred == -1:
            print ('Holding...')
        if pred == 0:
            print ('Holding...')
        if pred == 1:
            print ('Closing position...')
            client.Order.Order_closePosition(symbol=symbol).result()
            #short
            print ('Buying...')
            client.Order.Order_new(symbol=symbol, ordType=ordType, orderQty=orderQty_Buy).result()            
    
        