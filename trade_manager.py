"""Program for calculating a trade according trading system."""

import pickle

display = True      # define display or not system settings. In case new ones were set - display only one time (not twice)

reload_set = False  # reload system settings in case new were set, so it will be in power right away


def get_input_set(message):
    """Get user input for setting trading system."""

    if message != "Currency ticker (USD, EUR, RUB, ect): ":

        while True:

            try:

                value = int(input(message))
                return value

            except ValueError:

                print('Wrong input! Try again!')

    else:

        value = input(message)

        return value


class SystemSet:
    """Set and change parameters of the trading system."""

    def __init__(self, deposit, risk_percent, p_l, trade_percent, accuracy, currency):

        self.__deposit = deposit                # amount of money in deposit
        self.__risk_percent = risk_percent      # risk for one trade in percents
        self.__p_l = p_l                        # profit / loss ratio
        self.__trade_percent = trade_percent    # percent out of deposit for one trade
        self.__accuracy = accuracy              # amount of digits after coma
        self.__currency = currency              # type of currency (usd, eur, rub, ect)
        self.__long = True                      # default long = True

        self.__risk_usd = (self.__deposit / 100) * self.__risk_percent          # max risk for one trade (in currency)
        self.__trade_usd = float(self.__deposit / 100) * self.__trade_percent   # max amount of money for one trade

    @property
    def deposit(self):
        """Get amount of money in deposit."""
        return self.__deposit

    @property
    def risk_percent(self):
        """Get risk for one trade in percents."""
        return self.__risk_percent

    @property
    def p_l(self):
        """Get profit/loss ratio."""
        return self.__p_l

    @property
    def trade_percent(self):
        """Get trade_percent (percent out of deposit for one trade)."""
        return self.__trade_percent

    @property
    def accuracy(self):
        """Get accuracy (amount of digits after coma)."""
        return self.__accuracy

    @property
    def currency(self):
        """Get currency of your account."""
        return self.__currency

    @property
    def long(self):
        """Get long/short."""
        return self.__long

    @property
    def risk_usd(self):
        """Get risk usd (max risk for one trade (in currency))."""
        return self.__risk_usd

    @property
    def trade_usd(self):
        """Get trade usd (max amount of money for one trade)."""
        return self.__trade_usd

    @long.setter
    def long(self, value):
        self.__long = value

    def print_system_set(self, show):
        """Print information about trading system."""

        if show:

            global display

            display = False

            print('')
            print('\t  |Parameters of your trading system| '
                  '\n'
                  '--------------------------------------------------------------------------\n'
                  f'Deposit: {self.__deposit} {self.currency}. \n'
                  '--------------------------------------------------------------------------\n'
                  f'Risk for one trade: {self.__risk_percent}%.\t | In currency: {int(self.__risk_usd)} {self.currency}. \n'
                  '--------------------------------------------------------------------------\n'
                  f'Amount from deposit for one trade: {self.__trade_percent}%.\t | In currency: {int(self.__trade_usd)} {self.currency}. \n'
                  '--------------------------------------------------------------------------\n'
                  f'Profit/loss ratio: 1:{self.__p_l}. \n'
                  '--------------------------------------------------------------------------'
                  )


def set_up_system():
    """Set up new settings for a trading system."""

    deposit_set = get_input_set(message="Input amount of your deposit: ")
    risk_percent_set = get_input_set(message="Max acceptable risk in percent from deposit: ")
    p_l_set = get_input_set(message="Profit/loss ratio - 1 to: ")
    trade_percent_set = get_input_set(message="Max percent out of deposit for one trade: ")
    accuracy_set = get_input_set(message="Accuracy (amount of digits after coma): ")
    currency_set = get_input_set(message="Currency ticker (USD, EUR, RUB, ect): ")

    filename = "settings.dat"

    with open(filename, "wb") as file_set:
        pickle.dump(deposit_set, file_set)
        pickle.dump(risk_percent_set, file_set)
        pickle.dump(p_l_set, file_set)
        pickle.dump(trade_percent_set, file_set)
        pickle.dump(accuracy_set, file_set)
        pickle.dump(currency_set, file_set)

        print()
        print("New parameters successfully set!")

        global reload_set

        reload_set = True

        p = SystemSet(deposit_set, risk_percent_set, p_l_set, trade_percent_set, accuracy_set, currency_set)

        p.print_system_set(show=True)


def check_set():
    """Check if the file with system settings exists."""

    set_up_check = "settings.dat"

    try:
        with open(set_up_check, "rb"):
            pass

    except FileNotFoundError:
        print()
        print("File with settings not found. Set up a new one.")
        print()
        set_up_system()  # set new file with settings


check_set()


set_up = "settings.dat"

with open(set_up, "rb") as file:

    deposit_get = pickle.load(file)        # amount of money in deposit
    risk_percent_get = pickle.load(file)   # amount of money in deposit
    p_l_get = pickle.load(file)            # profit / loss ratio
    trade_percent_get = pickle.load(file)  # percent out of deposit for one trade
    accuracy_get = pickle.load(file)       # amount of digits after coma
    currency_get = pickle.load(file)       # type of currency (usd, eur, rub, ect)

s = SystemSet(deposit_get, risk_percent_get, p_l_get, trade_percent_get, accuracy_get, currency_get)


def get_input_trade(definer, price=0):
    """Get parameters of a trade from user."""

    if definer == 0:

        while True:

            try:
                short_long = int(input('Choose type of trade 0 - short, 1 - long: '))

                if short_long == 0 or short_long == 1:
                    return short_long

                else:
                    print("Wrong input! Try again!")

            except ValueError:
                print("Wrong input! Try again!")

    if definer == 1:

        while True:

            try:
                price = float(input(f'Input price of entering: '))
                return price

            except ValueError:
                print("Wrong input! Try again!")

    if definer == 2:

        while True:

            try:

                stop = float(input('Input stop: '))

                if s.long:

                    if stop < price:
                        return float(stop)

                    else:
                        print(f'Stop must be lower {int(price)} {s.currency}!')

                else:
                    if stop > price:
                        return float(stop)

                    else:
                        print(f'Stop must be higher {int(price)} {s.currency}!')

            except ValueError:
                print("Wrong input! Try again!")

    if definer == 3:

        while True:

            try:
                amount_usd = int(input('Input amount of money for the trade: '))

                if amount_usd > s.trade_usd:

                    print(
                        f'Violation of the trading system!!! Amount of trade must be lower or equal to {int(s.trade_usd)} {s.currency}!!!'
                    )

                else:
                    return amount_usd

            except ValueError:
                print("Wrong input! Try again!")

    if definer == 4:

        while True:

            try:

                margin = float(input('Input leverage. If the trade without it just input 1: '))

                if margin < 1:
                    print("Wrong input! Try again!")

                else:
                    return float(margin)

            except ValueError:
                print("Wrong input! Try again!")

    if definer == 5:
        ticker = str(input('Input the ticker of the trading asset: '))
        return ticker

    # if definer == 6:
    # take_profit = float(input('Input take-profit: '))
    # return take_profit


def change_or_not():
    """Choose change the system or not."""

    while True:

        print()
        print("Would you like to change the system settings?")
        print()
        choice = input("Type in 'yes/no': ")
        print()

        if choice.lower() == 'yes':
            set_up_system()

        elif choice.lower() == 'no':
            break

        else:
            print('Wrong input! Try again!')


def get_trade():
    """Get parameters of a trade from user."""
    print('Calculating...\n')

    s.long = get_input_trade(0)       # choose short or long
    price = get_input_trade(1)        # price of entering
    stop = get_input_trade(2, price)  # stop price
    amount_usd = get_input_trade(3)   # amount of money for one trade
    margin = get_input_trade(4)       # leverage
    ticker = get_input_trade(5)       # ticker of an asset
    # take_profit = get_input(7)      # anticipated take-profit

    parameters = [price, stop, margin, amount_usd, ticker]

    return parameters


def calc(price, stop, margin, amount_usd, ticker):
    """Calculate trade."""

    amount_asset = (amount_usd / price) * margin  # amount of asset for the current trade

    if s.long:

        risk_trade = price - stop  # risk in the trade for long

    else:

        risk_trade = stop - price  # risk in the trade for short

    risk_trade_usd = amount_asset * risk_trade  # risk in currency

    risk_trade_percent = (risk_trade_usd / s.deposit) * 100  # risk for the all the trading money in percents

    parameters = [risk_trade_usd, risk_trade_percent, amount_asset, ticker]

    return parameters


def print_result(risk_trade_usd, risk_trade_percent, amount_asset, ticker):
    """Print calculated result for the trade."""

    if s.long:
        type_trade = 'LONG'
        buy_sell = 'buy'

    else:
        type_trade = 'SHORT'
        buy_sell = 'sell'

    if risk_trade_usd > s.risk_usd:

        print('')
        print('\t Result:'
              '\n\n'
              f"\t THE TRADE DOES NOT COMPLY WITH YOUR TRADING SYSTEM!!!\n\n"
              '--------------------------------------------------------------------------\n'
              f"Possible loss: {int(risk_trade_usd)} {s.currency} | Allowed: {int(s.risk_usd)} {s.currency} | Exceeding: {int(risk_trade_usd) - int(s.risk_usd)} {s.currency} \n"
              '--------------------------------------------------------------------------\n'
              f'Type of trade: {type_trade}. \n'
              '--------------------------------------------------------------------------\n'
              f'Risk in {s.currency}: {int(risk_trade_usd)}.\t | Allowed: {int(s.risk_usd)} {s.currency}.\n'
              '--------------------------------------------------------------------------\n'
              f'Risk in percents: {float(round(risk_trade_percent, 1))} % out of deposit.\t | Allowed: {float(round(s.risk_percent, 1))} %.\n'
              '--------------------------------------------------------------------------\n'
              f'You are going to {buy_sell}: {round(amount_asset, s.accuracy)} {ticker}. \n'
              '--------------------------------------------------------------------------\n'
              )

    else:
        print('')
        print('\t Result:'
              '\n\n'
              '--------------------------------------------------------------------------\n'
              f'Type of trade: {type_trade}. \n'
              '--------------------------------------------------------------------------\n'
              f'Risk in {s.currency}: {int(risk_trade_usd)} {s.currency}.\t | Allowed: {int(s.risk_usd)} {s.currency}.\n'
              '--------------------------------------------------------------------------\n'
              f'Risk in percents: {float(round(risk_trade_percent, 1))} % out of deposit.\t | Allowed: {float(round(s.risk_percent, 1))} %.\n'
              '--------------------------------------------------------------------------\n'
              f'You are going to {buy_sell}: {round(amount_asset, s.accuracy)} {ticker}. \n'
              '--------------------------------------------------------------------------\n'
              )


def new_trade():
    """Choose change the system or not."""

    while True:

        print("Would you like to calculate a new trade?")
        print()
        choice = input("Type in 'yes/no': ")

        if choice.lower() == 'yes':
            get_trade()

        elif choice.lower() == 'no':
            break

        else:
            print('Wrong input! Try again!')


def reboot_set(reboot):
    """Reboot system settings if set new ones."""

    if reboot:

        global set_up
        global file
        global deposit_get
        global risk_percent_get
        global p_l_get
        global trade_percent_get
        global accuracy_get
        global currency_get
        global s

        set_up = "settings.dat"

        with open(set_up, "rb") as file:

            deposit_get = pickle.load(file)        # amount of money in deposit
            risk_percent_get = pickle.load(file)   # amount of money in deposit
            p_l_get = pickle.load(file)            # profit / loss ratio
            trade_percent_get = pickle.load(file)  # percent out of deposit for one trade
            accuracy_get = pickle.load(file)       # amount of digits after coma
            currency_get = pickle.load(file)       # type of currency (usd, eur, rub, ect)

        s = SystemSet(deposit_get, risk_percent_get, p_l_get, trade_percent_get, accuracy_get, currency_get)


def main():
    """Main function."""
    s.print_system_set(display)
    change_or_not()
    reboot_set(reload_set)
    trade = get_trade()
    calc_result = calc(*trade)
    print_result(*calc_result)
    new_trade()


main()


# add detail information about trade (result in usd, percents after trade)

# add  risk / profit (p_l)

# add interface

# would you like to calc a take profit as well?
