from file_reader import read_shipping_prices, read_orders
from order_processor import process_orders
from file_reader import read_product_prices

def main():
    shipping_prices = read_shipping_prices("../csvFiles/shipping_prices.csv")
    if not shipping_prices:
        return
    
    # Fetch product prices
    product_prices = read_product_prices("../csvFiles/productprices.csv")
    if not product_prices:
        print("No product prices found. Proceeding with shipping prices only.")
    
    # Merge product prices into shipping prices
    prices = {**shipping_prices, **product_prices}
    
    orders = read_orders("../csvFiles/ordersexport.csv")
    if not orders:
        return
    
    process_orders(prices, orders)

if __name__ == "__main__":
    main()
