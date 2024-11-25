import csv

def read_shipping_prices(filename):
    prices = {}

    try:
        with open(filename, mode="r") as prices_file:
            prices_reader = csv.reader(prices_file)
            price_headers = next(prices_reader)

            for record in prices_reader:
                item = record[0].strip()
                prices[item] = {}

                for i, price_str in enumerate(record[1:], start=1):
                    country = price_headers[i].strip()
                    if price_str == "" or country == "":
                        continue
                    try:
                        price = float(price_str)
                        prices[item][country] = price
                    except ValueError:
                        print(f"Error parsing price for item {item}, country {country}")
    except Exception as e:
        print(f"Error opening shipping prices file: {e}")
        return None

    return prices


def read_orders(filename):
    orders = []

    try:
        with open(filename, mode="r") as file:
            reader = csv.reader(file)
            headers = next(reader)

            name_index = -1
            item_index = -1
            country_index = -1
            quantity_index = -1
            for i, header in enumerate(headers):
                if header == "Name":
                    name_index = i
                elif header == "Lineitem name":
                    item_index = i
                elif header == "Shipping Country":
                    country_index = i
                elif header == "Lineitem quantity":
                    quantity_index = i

            if name_index == -1 or item_index == -1 or country_index == -1 or quantity_index == -1:
                print("One or more required columns not found.")
                return None

            for record in reader:
                name = record[name_index].strip()
                item = record[item_index].strip()
                country = record[country_index].strip()
                quantity_str = record[quantity_index].strip()

                try:
                    quantity = int(quantity_str)
                except ValueError:
                    print(f"Error converting quantity to integer for item: {item}. Skipping.")
                    continue

                orders.append({"name": name, "item": item, "country": country, "quantity": quantity})

    except Exception as e:
        print(f"Error opening orders file: {e}")
        return None

    return orders
    

def read_product_prices(filepath):
    """Reads product prices and costs (COGS) from a CSV file."""
    product_data = {}
    try:
        with open(filepath, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                item = row.get("Item", "").strip()
                price = float(row.get("Price", 0))
                cost = float(row.get("Cost", 0))  # Assuming the CSV includes a "Cost" column
                if item:
                    product_data[item] = {"price": price, "cost": cost}
    except Exception as e:
        print(f"Error reading product prices: {e}")
    return product_data
