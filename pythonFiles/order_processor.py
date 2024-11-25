def process_orders(prices, orders):
    print("Filtered Orders:")
    customer_country_map = {}  # To store the country for each customer
    customer_suitcases = {}
    all_items = {}

    additional_items = [
        "LEATHER LUGGAGE TAG - Black", "LEATHER LUGGAGE TAG - Noir",
        "RIVIERA TOILETRY CASE - Marron / 5.5𝘪𝘯 𝘹 9.8𝘪𝘯 𝘹 5.9𝘪𝘯",
        "COMPRESSIBLE PACKING CUBES - Black", "COMPRESSIBLE PACKING CUBES - Grey",
        "COMPRESSIBLE PACKING CUBES - Noir", "COMPRESSIBLE PACKING CUBES - Beige"
    ]

    grandTotalPrice = 0  # To accumulate total for all orders

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

        # Skip the item if it's not in the prices map (only for regular items)
        if cleaned_item not in prices and cleaned_item not in additional_items:
            continue

        # Store information about customer orders
        if name not in customer_suitcases:
            customer_suitcases[name] = {"Large": 0, "Carry-on": 0}
            all_items[name] = []

        if cleaned_item == "Nomad Aluminium Suitcase - Large":
            customer_suitcases[name]["Large"] += quantity
        elif cleaned_item == "Nomad Aluminium Suitcase - Carry-on":
            customer_suitcases[name]["Carry-on"] += quantity

        if cleaned_item in additional_items:
            print(f"Processing additional item: {cleaned_item} (Quantity: {quantity})")

        all_items[name].append({
            "item": cleaned_item,
            "quantity": quantity,
            "country": country,
            "price": prices.get(cleaned_item, {}).get(country, 0)
        })

    # Print out the results for all items
    for name, items in all_items.items():
        print(f"\nName: {name}")

        large_count = customer_suitcases.get(name, {}).get("Large", 0)
        carry_on_count = customer_suitcases.get(name, {}).get("Carry-on", 0)

        totalOrderPrice = 0

        # If both large and carry-on suitcases are ordered, show the combined item
        combined_count = min(large_count, carry_on_count)
        if combined_count > 0:
            combined_country = customer_country_map[name]  # Use the first item country
            combined_price = prices.get("Nomad Aluminium Suitcase - Carry-on + Large", {}).get(combined_country, 0)
            combined_total_price = combined_price * combined_count
            print(f"  Item: Nomad Aluminium Suitcase - Carry-on + Large, Country: {combined_country}, Quantity: {combined_count}, Price: {combined_price:.2f}")
            totalOrderPrice += combined_total_price

        # Handle remaining large suitcases if any
        remaining_large_count = large_count - combined_count
        if remaining_large_count > 0:
            large_country = customer_country_map[name]
            large_price = prices.get("Nomad Aluminium Suitcase - Large", {}).get(large_country, 0)
            large_total_price = large_price * remaining_large_count
            print(f"  Item: Nomad Aluminium Suitcase - Large, Country: {large_country}, Quantity: {remaining_large_count}, Price: {large_price:.2f}")
            totalOrderPrice += large_total_price

        # Handle remaining carry-on suitcases if any
        remaining_carry_on_count = carry_on_count - combined_count
        if remaining_carry_on_count > 0:
            carry_on_country = customer_country_map[name]
            carry_on_price = prices.get("Nomad Aluminium Suitcase - Carry-on", {}).get(carry_on_country, 0)
            carry_on_total_price = carry_on_price * remaining_carry_on_count
            print(f"  Item: Nomad Aluminium Suitcase - Carry-on, Country: {carry_on_country}, Quantity: {remaining_carry_on_count}, Price: {carry_on_price:.2f}")
            totalOrderPrice += carry_on_total_price

        # Include additional items in the total order price
        for item in items:
            if item["item"] not in ["Nomad Aluminium Suitcase - Large", "Nomad Aluminium Suitcase - Carry-on"]:
                item_total_price = item["price"] * item["quantity"]
                print(f"  Item: {item['item']}, Country: {item['country']}, Quantity: {item['quantity']}, Price: {item['price']:.2f}")
                totalOrderPrice += item_total_price

        print(f"  Total Order Price for order {name}: {totalOrderPrice:.2f}")
        grandTotalPrice += totalOrderPrice * 0.957  # prix total en euros basé sur le taux d'ajd

    print(f"\Shipping Total Price for All Orders: {grandTotalPrice:.2f}")
