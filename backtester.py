from math import copysign

class BacktestBookkeeper:
    def __init__(self, init_balance, transaction_fee=0, slippage=0):
        self.balance=init_balance
        self.transaction_fee = transaction_fee
        self.slippage = slippage
        
        self.current_position=0
        self.average_entry=0
        self.upnl=0
        self.current_price=0

    def update_price(self, price):
        self.current_price=price
        self.upnl = self.pnl_calc(entry_price=self.average_entry, exit_price=self.current_price, contracts=self.current_position)
        return {'current_position':self.current_position,'average_entry':self.average_entry, 'upnl':self.upnl, 'balance': self.balance}

    def market_order(self,quantity):

        # if quantity>0 then long, then slippage>0,
        # if quantity<0 then short, then slippage<0
        slippage = self.slippage*copysign(1,quantity)
        executing_price = self.current_price+slippage 

        self.upnl = self.pnl_calc(entry_price=self.average_entry, exit_price=executing_price, contracts=self.current_position)
        # print('pnl after first line of order fcn: {}'.format(self.upnl))

        new_position = self.current_position + quantity

        new_average_entry = self.compute_new_average_entry(
            old_entry_price=self.average_entry, 
            old_contracts=self.current_position, 
            new_entry_price=executing_price, 
            new_contracts=quantity)        

        if (self.current_position<=0 and quantity<0) or (self.current_position>=0 and quantity>0):
            # print('INCREASING POSITION BY {}'.format(quantity))
            # ADDING TO POSITION:
            # reduces pnl!
            self.upnl = self.pnl_calc(entry_price=new_average_entry, exit_price=self.current_price, contracts=new_position)
            # self.current_position = quantity+self.current_position
        
        if (self.current_position<0 and quantity>0) or (self.current_position>0 and quantity<0):
            # print('REDUCING POSITION BY {}'.format(quantity))
            # UPDATE upnl, and balance 
            # note: the negative sign is because we are reducing position
            pnl = -self.pnl_calc(entry_price=self.average_entry, exit_price=self.current_price, contracts=quantity)
            self.balance += pnl
            self.upnl -= pnl  
        
        self.balance=self.balance-self.transaction_fee*abs(quantity)
        
        self.current_position = new_position
        self.average_entry = new_average_entry
        self.upnl = self.pnl_calc(entry_price=self.average_entry, exit_price=self.current_price, contracts=self.current_position)
        # print('pnl after order: {}'.format(self.upnl))

        return {'status':'FILLED', 'fill_price':self.current_price}

    def get_position_details(self):
        return {'current_position':self.current_position,'average_entry':self.average_entry, 'upnl':self.upnl}

    def get_balance(self):
        return self.balance        

    @staticmethod     
    def compute_new_average_entry(old_entry_price, old_contracts, new_entry_price, new_contracts):
        if new_contracts+old_contracts == 0:
            average_entry = 0
        # if you are short/long and the new_contracts is long/short, then you are 
        # reducing position, and your average entry price does not change
        elif (old_contracts<0 and new_contracts>0) or (old_contracts>0 and new_contracts<0) :
            average_entry = old_entry_price
        else: 
            average_entry = ((abs(old_contracts) * old_entry_price) +
                              (new_entry_price * abs(new_contracts))) / (abs(old_contracts)+abs(new_contracts)) 
        return average_entry
        
    # profit/loss calculator
    @staticmethod
    def pnl_calc(entry_price, exit_price, contracts):
        return (exit_price-entry_price)*contracts


# bt = BacktestBookkeeper(init_balance=10000, transaction_fee=0, slippage=1)
# bt.update_price(10)
# bt.market_order(quantity=1000)
# bt.get_position_details()
# bt.market_order(quantity=-500)
# bt.get_position_details()
# bt.get_balance()
# bt.market_order(quantity=-500)
# bt.get_position_details()
# bt.get_balance()
