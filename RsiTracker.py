import websocket, json, pprint, talib, numpy



SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1h"
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = "ETHUSD"
TRADE_QUANTITY = 0.05
closes = []

in_postion = False
def on_open(ws):
    print("open")


def on_close(ws):
    print("close")

def on_message(ws, message):
    global closes
    print("received")
    print(message)
    json_message = json.loads(message)
    pprint.pprint(json_message)

    candle = json_message["k"]
    is_candle_closed = candle["x"]
    close = candle["c"]
    if is_candle_closed:

        print("candle closed a {}".format(close))
        closes.append(float(close))
        print("closes")
        print(closes)

        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print("all rsi so far")
            print(rsi)
            last_rsi = rsi[-1]
            print("current rsi is {}".format(last_rsi))

            if last_rsi > RSI_OVERBOUGHT:
                if in_postion:
                    print("SELL")
                else:    
                    print("Overbought, but you do not own anything.")
            if last_rsi < RSI_OVERSOLD:
                if in_postion:
                    ("it is oversold, but you already own it, nothing to do")
                else:
                    print("BUY")
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)

ws.run_forever()


