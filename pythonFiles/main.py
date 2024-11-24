from file_reader import read_shipping_prices, read_orders
from order_processor import process_orders

def main():
    prices = read_shipping_prices("../csvFiles/shipping_prices.csv")
    if not prices:
        return
    
    orders = read_orders("../csvFiles/ordersexport.csv")
    if not orders:
        return
    
    process_orders(prices, orders)

if __name__ == "__main__":
    main()
