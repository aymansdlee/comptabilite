def process_orders(prices, orders):
    print("Filtered Orders:")
    customer_country_map = {}  # To store the country for each customer
    customer_suitcases = {}
    all_items = {}

    # Cost of goods for all items
    cost_of_goods = {
        "Carry-on": 46.954,
        "Medium": 54.5495,
        "Large": 64.4927,
        "Compressible Packing Cubes - Black": 6.9,
        "Compressible Packing Cubes - Grey": 6.9,
        "Compressible Packing Cubes - Noir": 6.9,
        "Compressible Packing Cubes - Beige": 6.9,
        "LEATHER LUGGAGE TAG - Black": 0.7,
        "LEATHER LUGGAGE TAG - Noir": 0.7,
        "RIVIERA TOILETRY CASE - Marron / 5.5𝘪𝘯": 15.0,
        "RIVIERA TOILETRY CASE - Black / 5.5𝘪𝘯": 15.0,
    }

    grandTotalPriceEuro = 0
    grandTotalPriceUsd = 0

    totalProductCostUsd = 0
    totalProductCostEuro = 0

    totalShippingCostUsd = 0
    totalShippingCostEuro = 0

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

        # Store information about customer orders
        if name not in customer_suitcases:
            customer_suitcases[name] = {"Large": 0, "Carry-on": 0, "Medium": 0}
            all_items[name] = []

        if cleaned_item == "Nomad Aluminium Suitcase - Large":
            customer_suitcases[name]["Large"] += quantity
        elif cleaned_item == "Nomad Aluminium Suitcase - Carry-on":
            customer_suitcases[name]["Carry-on"] += quantity
        elif cleaned_item == "Nomad Aluminium Suitcase - Medium":
            customer_suitcases[name]["Medium"] += quantity

        price = prices.get(cleaned_item, 0)  # Default to 0 if not in prices
        if isinstance(price, dict):
            item_price = price.get(country, 0)
        else:
            item_price = price

        all_items[name].append({
            "item": cleaned_item,
            "quantity": quantity,
            "country": country,
            "price": item_price
        })

    for name, items in all_items.items():
        print(f"\nName: {name}")

        large_count = customer_suitcases.get(name, {}).get("Large", 0)
        carry_on_count = customer_suitcases.get(name, {}).get("Carry-on", 0)
        medium_count = customer_suitcases.get(name, {}).get("Medium", 0)

        totalShippingCost = 0
        totalProductCost = 0

        # If both large and carry-on suitcases are ordered, show the combined item
        combined_count = min(large_count, carry_on_count)
        if combined_count > 0:
            combined_country = customer_country_map[name]
            combined_price = prices.get("Nomad Aluminium Suitcase - Carry-on + Large", {}).get(combined_country, 0)
            combined_total_price = combined_price * combined_count
            product_cost = (cost_of_goods["Carry-on"] + cost_of_goods["Large"]) * combined_count
            print(f"  Item: Nomad Aluminium Suitcase - Carry-on + Large, Country: {combined_country}, Quantity: {combined_count}, Shipping Price: ${combined_total_price:.2f}, Product Price: ${product_cost:.2f}")
            totalShippingCost += combined_total_price
            totalProductCost += product_cost

        # Handle remaining large suitcases
        remaining_large_count = large_count - combined_count
        if remaining_large_count > 0:
            large_country = customer_country_map[name]
            large_price = prices.get("Nomad Aluminium Suitcase - Large", {}).get(large_country, 0)
            large_total_price = large_price * remaining_large_count
            product_cost = cost_of_goods["Large"] * remaining_large_count
            print(f"  Item: Nomad Aluminium Suitcase - Large, Country: {large_country}, Quantity: {remaining_large_count}, Shipping Price: ${large_total_price:.2f}, Product Price: ${product_cost:.2f}")
            totalShippingCost += large_total_price
            totalProductCost += product_cost

        # Handle remaining carry-on suitcases
        remaining_carry_on_count = carry_on_count - combined_count
        if remaining_carry_on_count > 0:
            carry_on_country = customer_country_map[name]
            carry_on_price = prices.get("Nomad Aluminium Suitcase - Carry-on", {}).get(carry_on_country, 0)
            carry_on_total_price = carry_on_price * remaining_carry_on_count
            product_cost = cost_of_goods["Carry-on"] * remaining_carry_on_count
            print(f"  Item: Nomad Aluminium Suitcase - Carry-on, Country: {carry_on_country}, Quantity: {remaining_carry_on_count}, Shipping Price: ${carry_on_total_price:.2f}, Product Price: ${product_cost:.2f}")
            totalShippingCost += carry_on_total_price
            totalProductCost += product_cost

        # Handle medium suitcases
        if medium_count > 0:
            medium_country = customer_country_map[name]
            medium_price = prices.get("Nomad Aluminium Suitcase - Medium", {}).get(medium_country, 0)
            medium_total_price = medium_price * medium_count
            product_cost = cost_of_goods["Medium"] * medium_count
            print(f"  Item: Nomad Aluminium Suitcase - Medium, Country: {medium_country}, Quantity: {medium_count}, Shipping Price: ${medium_total_price:.2f}, Product Price: ${product_cost:.2f}")
            totalShippingCost += medium_total_price
            totalProductCost += product_cost

        # Include additional items in the total order price
        for item in items:
            if item["item"] not in ["Nomad Aluminium Suitcase - Large", "Nomad Aluminium Suitcase - Carry-on", "Nomad Aluminium Suitcase - Medium"]:
                item_total_price = item["price"] * item["quantity"]
                product_cost = cost_of_goods.get(item["item"], 0) * item["quantity"]
                print(f"  Item: {item['item']}, Country: {item['country']}, Quantity: {item['quantity']}, Shipping Price: ${item_total_price:.2f}, Product Price: ${product_cost:.2f}")
                totalShippingCost += item_total_price
                totalProductCost += product_cost

        print(f"  Total Shipping Price for order {name}: ${totalShippingCost:.2f}")
        print(f"  Total Product Price for order {name}: ${totalProductCost:.2f}")
        print(f"  Total Order Cost for {name}: ${totalShippingCost + totalProductCost:.2f}")

        totalProductCostEuro += totalProductCost * 0.957
        totalProductCostUsd += totalProductCost

        totalShippingCostEuro += totalShippingCost * 0.957
        totalShippingCostUsd += totalShippingCost

        grandTotalPriceEuro += (totalShippingCost + totalProductCost) * 0.957
        grandTotalPriceUsd += totalShippingCost + totalProductCost

    print(f"\nTotal Shipping Cost for All Orders: {totalShippingCostEuro:.2f}€ or ${totalShippingCostUsd:.2f}")
    print(f"Total Product Cost for all orders: {totalProductCostEuro:.2f}€ or ${totalProductCostUsd:.2f}")
    print(f"Total Cost for all orders product and shipping: {grandTotalPriceEuro:.2f}€ or ${grandTotalPriceUsd:.2f}")
