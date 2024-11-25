from file_reader import read_shipping_prices, read_orders, read_product_prices
from order_processor import process_orders

def main():
    # Load shipping prices
    shipping_prices = read_shipping_prices("../csvFiles/shipping_prices.csv")
    if not shipping_prices:
        print("Failed to load shipping prices.")
        return

    # Load product prices
    product_prices = read_product_prices("../csvFiles/productprices.csv")
    if not product_prices:
        print("Failed to load product prices.")
        return

    # Merge the price dictionaries
    prices = {**shipping_prices, **product_prices}

    # Load orders
    orders = read_orders("../csvFiles/ordersexport.csv")
    if not orders:
        print("Failed to load orders.")
        return

    # Process orders
    process_orders(prices, orders)

if __name__ == "__main__":
    main()
