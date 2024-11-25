from flask import Flask, request, jsonify, render_template
from file_reader import read_shipping_prices, read_orders, read_product_prices
from order_processor import process_orders

app = Flask(__name__)

# Load data
shipping_prices = read_shipping_prices("../csvFiles/shipping_prices.csv")
product_prices = read_product_prices("../csvFiles/productprices.csv")
orders = read_orders("../csvFiles/ordersexport.csv")
prices = {**shipping_prices, **product_prices}
totals = process_orders(prices, orders)


@app.route('/')
def home():
    """
    Home route displaying available options.
    """
    return render_template('index.html')


@app.route('/total_shipping_cost')
def total_shipping_cost():
    totalShippingCostEuro, totalShippingCostUsd, *_ = totals
    return render_template(
        'styled_cost.html',
        title="Total Shipping Cost",
        costs=[
            {"label": "Total Shipping Cost (Euros)", "value": f"{totalShippingCostEuro:.2f}€"},
            {"label": "Total Shipping Cost (USD)", "value": f"${totalShippingCostUsd:.2f}"}
        ]
    )


@app.route('/total_product_cost')
def total_product_cost():
    _, _, totalProductCostEuro, totalProductCostUsd, *_ = totals
    return render_template(
        'styled_cost.html',
        title="Total Product Cost",
        costs=[
            {"label": "Total Product Cost (Euros)", "value": f"{totalProductCostEuro:.2f}€"},
            {"label": "Total Product Cost (USD)", "value": f"${totalProductCostUsd:.2f}"}
        ]
    )


@app.route('/grand_total_cost')
def grand_total_cost():
    *_, grandTotalPriceEuro, grandTotalPriceUsd = totals
    return render_template(
        'styled_cost.html',
        title="Grand Total Cost",
        costs=[
            {"label": "Grand Total Cost (Euros)", "value": f"{grandTotalPriceEuro:.2f}€"},
            {"label": "Grand Total Cost (USD)", "value": f"${grandTotalPriceUsd:.2f}"}
        ]
    )


@app.route('/all_orders')
def all_orders():
    from io import StringIO
    import sys

    # Capture the process_orders output
    old_stdout = sys.stdout
    sys.stdout = buffer = StringIO()
    process_orders(prices, orders)
    sys.stdout = old_stdout

    # Return the captured output as a string
    output = buffer.getvalue()
    return f"<pre>{output}</pre>"


@app.route('/track_order', methods=['GET', 'POST'])
def track_order():
    """
    Track a specific order by customer name.
    """
    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        customer_orders = [order for order in orders if order["name"].lower() == customer_name.lower()]

        if not customer_orders:
            return render_template('styled_message.html', message=f"No orders found for customer: {customer_name}")

        # Process the customer's orders
        from io import StringIO
        import sys

        # Capture process_orders output
        old_stdout = sys.stdout
        sys.stdout = buffer = StringIO()
        process_orders(prices, customer_orders)
        sys.stdout = old_stdout

        # Retrieve structured result
        output = buffer.getvalue()

        # Parse the output into structured data
        sections = []
        for line in output.split("\n"):
            if "Item:" in line or "Total" in line:
                sections.append(line.strip())

        return render_template('customer_orders.html', name=customer_name, sections=sections)

    return render_template('track_order.html')


if __name__ == '__main__':
    app.run(debug=True)
