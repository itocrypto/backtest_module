# backtest_module

This simple class does the bookkeeping for backtesting a trading strategy. Accounts for slippage and transaction fees. 

transaction_fee is a percentage of the price at which the order is executed. 


Primitive usage example: 
```

bt = BacktestBookkeeper(init_balance=10000, transaction_fee=0, slippage=1)
## Gettin REKT on slippage
bt.update_price(10)
bt.market_order(quantity=1000)
bt.get_position_details()
bt.market_order(quantity=-500)
bt.get_position_details()
bt.get_balance()
bt.market_order(quantity=-500)
bt.get_position_dils()
bt.get_balance()

## profitting on a long
bt.update_price(10)
bt.market_order(quantity=1000)
bt.update_price(15)
bt.market_order(quantity=-1000)
bt.get_position_dils()
bt.get_balance()
```

Less primitive usage example:

```
# list_of_candles  # first element is oldest candle
# process_candle() # some function that determines how much to buy/sell on each new candle

while len(list_of_candles)>0:
    new_candle = list_of_candles.pop(0)
    quantity = process_candle(new_candle)
    price = new_candle['close']
    bt.update_price(price=price)
    if quantity!=0:
      bt.market_order(quantity=quantity)  
    print(f"position details: {bt.get_position_details()}"")
    print(f"balance: {bt.get_balance()}")    

print(f"position details: {bt.get_position_details()}"")
print(f"balance: {bt.get_balance()}")    
```
