import csv

def main():
    # Open the shipping prices file
    prices = {}

    try:
        with open("shipping_prices.csv", mode="r") as prices_file:
            prices_reader = csv.reader(prices_file)
            price_headers = next(prices_reader)  # Read the header row

            # Parse the items and prices into a nested dictionary: item -> country -> price
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
        return

    # Open the orders file
    try:
        with open("ordersexport.csv", mode="r") as file:
            reader = csv.reader(file)
            headers = next(reader)

            # Find the indices of the required columns
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

            # Check if the required columns exist
            if name_index == -1 or item_index == -1 or country_index == -1 or quantity_index == -1:
                print("One or more required columns not found.")
                return

            # Process each order row
            print("Filtered Orders:")
            customer_country_map = {}  # To store the country for each customer
            customer_suitcases = {}
            all_items = {}

            for record in reader:
                name = record[name_index].strip()
                item = record[item_index].strip()
                country = record[country_index].strip()
                quantity_str = record[quantity_index].strip()

                # Extract country from the first item encountered for the customer
                if country != "" and name not in customer_country_map:
                    customer_country_map[name] = country
                if name in customer_country_map and country == "":
                    country = customer_country_map[name]

                # Convert quantity to an integer
                try:
                    quantity = int(quantity_str)
                except ValueError:
                    print(f"Error converting quantity to integer for item: {item}. Skipping.")
                    continue

                # Clean item name by removing color and slashes
                cleaned_item = item.replace("/ Black", "").replace("/ Silver", "").replace("/", "").strip()

                # Skip the item if it's not in the prices map
                if cleaned_item not in prices:
                    continue

                # Track the suitcases for the current customer
                if name not in customer_suitcases:
                    customer_suitcases[name] = {"Large": 0, "Carry-on": 0}
                    all_items[name] = []

                # If it's a "Large" or "Carry-on" suitcase, update the counts
                if cleaned_item == "Nomad Aluminium Suitcase - Large":
                    customer_suitcases[name]["Large"] += quantity
                elif cleaned_item == "Nomad Aluminium Suitcase - Carry-on":
                    customer_suitcases[name]["Carry-on"] += quantity

                # Store all the items for later printing (apply the first country for all)
                all_items[name].append({
                    "item": cleaned_item,
                    "quantity": quantity,
                    "country": country,  # Use the country we determined for the customer
                    "price": prices.get(cleaned_item, {}).get(country, 0)
                })

            # After processing all orders, print the result for each customer
            for name, items in all_items.items():
                # Print the customer's name
                print(f"Name: {name}")
                
                # Track the quantities of Large and Carry-on suitcases
                large_count = customer_suitcases.get(name, {}).get("Large", 0)
                carry_on_count = customer_suitcases.get(name, {}).get("Carry-on", 0)

                # Print each item except the combined one
                for item in items:
                    # Skip printing the individual Large and Carry-on if combined is going to be printed
                    if item["item"] == "Nomad Aluminium Suitcase - Large" and carry_on_count > 0:
                        continue
                    if item["item"] == "Nomad Aluminium Suitcase - Carry-on" and large_count > 0:
                        continue
                    print(f"  Item: {item['item']}, Country: {item['country']}, Quantity: {item['quantity']}, Price: {item['price']:.2f}")

                # Add a line for every time both suitcases were bought
                combined_count = min(large_count, carry_on_count)
                if combined_count > 0:
                    # Display combined item price based on the same country as the first item
                    combined_country = customer_country_map[name]  # Use the first item country
                    combined_price = prices.get("Nomad Aluminium Suitcase - Carry-on + Large", {}).get(combined_country, 0)
                    print(f"  Item: Nomad Aluminium Suitcase - Carry-on + Large, Country: {combined_country}, Quantity: {combined_count}, Price: {combined_price:.2f}")

    except Exception as e:
        print(f"Error opening orders file: {e}")
        return

if __name__ == "__main__":
    main()
