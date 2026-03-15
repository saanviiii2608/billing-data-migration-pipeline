def transform_data(df):

    records = []

    for _, row in df.iterrows():

        customer_name = row["customer_name"]

        # Handle missing names
        if customer_name != customer_name:   # checks for NaN
            customer_name = "Unknown Customer"

        record = {
            "customer_id": int(row["customer_id"]),
            "customer_name": customer_name,
            "subscription": {
                "plan": row["plan"],
                "price": float(row["price"])
            },
            "usage": int(row["usage"])
        }

        records.append(record)

    return records