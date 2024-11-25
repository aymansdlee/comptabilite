from file_reader import read_shipping_prices, read_orders, read_product_prices
from order_processor import process_orders


def show_total_shipping_cost(totals):
    totalShippingCostEuro, totalShippingCostUsd, *_ = totals
    print(f"\n💰 Total Shipping Cost for All Orders: {totalShippingCostEuro:.2f}€ or ${totalShippingCostUsd:.2f} 💰")


def show_total_product_cost(totals):
    _, _, totalProductCostEuro, totalProductCostUsd, *_ = totals
    print(f"\n💰 Total Product Cost for all orders: {totalProductCostEuro:.2f}€ or ${totalProductCostUsd:.2f} 💰")


def show_grand_total_cost(totals):
    *_, grandTotalPriceEuro, grandTotalPriceUsd = totals
    print(f"\n💰 Total Cost for all orders product and shipping: {grandTotalPriceEuro:.2f}€ or ${grandTotalPriceUsd:.2f} 💰")


def print_all_orders(prices, orders):
    """
    Reuses the `process_orders` function from order_processor.py to handle order processing and detailed display.
    """
    print("\nAll Orders:")
    process_orders(prices, orders)  # Directly calls the function to display orders

def print_order_by_name(prices, orders):
    """
    Asks for a customer name and prints the detailed order for that name using `process_orders`.
    """
    customer_name = input("\nEnter the customer name you want to track: ").strip()
    
    # Filter the orders for the given customer name
    customer_orders = [order for order in orders if order["name"].lower() == customer_name.lower()]
    
    if not customer_orders:
        print(f"No orders found for customer: {customer_name}")
        return

    print(f"\nOrders for {customer_name}:")
    process_orders(prices, customer_orders)  # Reuse `process_orders` to display the filtered orders



def main_menu(prices, totals, orders):
    actions = {
        "1": lambda: show_total_shipping_cost(totals),
        "2": lambda: show_total_product_cost(totals),
        "3": lambda: show_grand_total_cost(totals),
        "4": lambda: print_all_orders(prices, orders),
        "5": lambda: print_order_by_name(prices, orders),
        "6": exit
    }

    while True:
        print("\nMain Menu:")
        print("1. Show Total Shipping Cost")
        print("2. Show Total Product Cost")
        print("3. Show Total Cost (Product + Shipping)")
        print("4. Show All Orders")
        print("5. Track a Customer Order by Name")
        print("6. Exit")

        choice = input("Choose an option: ")
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid option, please try again.")



def main():
    """
    Main function to load data, process orders, and navigate the menu.
    """
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

    # Process orders and get totals
    totals = process_orders(prices, orders)

    # Call the main menu with the totals and orders
    main_menu(prices, totals, orders)


if __name__ == "__main__":
    main()
