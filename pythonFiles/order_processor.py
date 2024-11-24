def process_orders(prices, orders):
    print("Filtered Orders:")
    customer_country_map = {}  # To store the country for each customer
    customer_suitcases = {}
    all_items = {}

    for order in orders:
        name = order["name"]
        item = order["item"]
        country = order["country"]
        quantity = order["quantity"]

        if country != "" and name not in customer_country_map:
            customer_country_map[name] = country
        if name in customer_country_map and country == "":
            country = customer_country_map[name]

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
