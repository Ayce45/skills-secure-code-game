'''
Welcome to Secure Code Game Season-1/Level-1!

Follow the instructions below to get started:

1. tests.py is passing but code.py is vulnerable
2. Review the code. Can you spot the bug?
3. Fix the code but ensure that tests.py passes
4. Run hack.py and if passing then CONGRATS!
5. If stuck then read the hint
6. Compare your solution with solution.py
'''

from collections import namedtuple
from decimal import Decimal

Order = namedtuple('Order', 'id, items')
Item = namedtuple('Item', 'type, description, amount, quantity')

MAX_ITEM_AMOUNT = 100_000 # maximum price of item in the shop
MAX_QUANTITY = 100 # maximum quantity of an item in the shop
MIN_QUANTITY = 1 # minimum quantity of an item in the shop
MAX_TOTAL = 1e6 # maximum total amount accepted for an order


def is_valid_payment(amount):
    return -MAX_ITEM_AMOUNT <= amount <= MAX_ITEM_AMOUNT

def is_valid_product(quantity, amount):
    return (type(quantity) is int and MIN_QUANTITY <= quantity <= MAX_QUANTITY and 
            0 < amount <= MAX_ITEM_AMOUNT)

def process_item(item):
    if item.type == 'payment' and is_valid_payment(item.amount):
        return 'payment', Decimal(str(item.amount))
    elif item.type == 'product' and is_valid_product(item.quantity, item.amount):
        return 'product', Decimal(str(item.amount)) * item.quantity
    else:
        raise ValueError("Invalid item type: %s" % item.type)

def calculate_totals(order):
    payments = Decimal('0')
    expenses = Decimal('0')
    
    for item in order.items:
        item_type, amount = process_item(item)
        if item_type == 'payment':
            payments += amount
        elif item_type == 'product':
            expenses += amount
    
    return payments, expenses

def validorder(order):
    try:
        payments, expenses = calculate_totals(order)
    except ValueError as e:
        return str(e)
    
    if payments > MAX_TOTAL or expenses > MAX_TOTAL:
        return "Total amount payable for an order exceeded"

    if payments != expenses:
        return "Order ID: %s - Payment imbalance: $%0.2f" % (order.id, payments - expenses)
    else:
        return "Order ID: %s - Full payment received!" % order.id