import csv

def main():
    prices = {}

    try:
        with open("shipping_prices.csv", mode="r") as prices_file:
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
        return

    try:
        with open("ordersexport.csv", mode="r") as file:
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
                return

            print("Filtered Orders:")
            customer_country_map = {}  # To store the country for each customer
            customer_suitcases = {}
            all_items = {}

            for record in reader:
                name = record[name_index].strip()
                item = record[item_index].strip()
                country = record[country_index].strip()
                quantity_str = record[quantity_index].strip()

                if country != "" and name not in customer_country_map:
                    customer_country_map[name] = country
                if name in customer_country_map and country == "":
                    country = customer_country_map[name]

                try:
                    quantity = int(quantity_str)
                except ValueError:
                    print(f"Error converting quantity to integer for item: {item}. Skipping.")
                    continue

                cleaned_item = item.replace("/ Black", "").replace("/ Silver", "").replace("/", "").strip()

                # Skip the item if it's not in the prices map
                if cleaned_item not in prices:
                    continue

                if name not in customer_suitcases:
                    customer_suitcases[name] = {"Large": 0, "Carry-on": 0}
                    all_items[name] = []

                if cleaned_item == "Nomad Aluminium Suitcase - Large":
                    customer_suitcases[name]["Large"] += quantity
                elif cleaned_item == "Nomad Aluminium Suitcase - Carry-on":
                    customer_suitcases[name]["Carry-on"] += quantity

                # Store all the items for later printing (apply the first country for all)
                all_items[name].append({
                    "item": cleaned_item,
                    "quantity": quantity,
                    "country": country, 
                    "price": prices.get(cleaned_item, {}).get(country, 0)
                })

            for name, items in all_items.items():
                print(f"Name: {name}")
                
                large_count = customer_suitcases.get(name, {}).get("Large", 0)
                carry_on_count = customer_suitcases.get(name, {}).get("Carry-on", 0)

                for item in items:

                    if item["item"] == "Nomad Aluminium Suitcase - Large" and carry_on_count > 0:
                        continue
                    if item["item"] == "Nomad Aluminium Suitcase - Carry-on" and large_count > 0:
                        continue
                    print(f"  Item: {item['item']}, Country: {item['country']}, Quantity: {item['quantity']}, Price: {item['price']:.2f}")

                combined_count = min(large_count, carry_on_count)
                if combined_count > 0:

                    combined_country = customer_country_map[name]  # Use the first item country
                    combined_price = prices.get("Nomad Aluminium Suitcase - Carry-on + Large", {}).get(combined_country, 0)
                    print(f"  Item: Nomad Aluminium Suitcase - Carry-on + Large, Country: {combined_country}, Quantity: {combined_count}, Price: {combined_price:.2f}")

    except Exception as e:
        print(f"Error opening orders file: {e}")
        return

if __name__ == "__main__":
    main()
