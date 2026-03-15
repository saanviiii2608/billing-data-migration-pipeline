def validate_data(df):

    errors = []

    # Check for missing customer names
    if df['customer_name'].isnull().any():
        errors.append("Missing customer names found")

    # Check for negative usage
    if (df['usage'] < 0).any():
        errors.append("Negative usage values found")

    # Check for duplicate customers
    duplicates = df[df.duplicated('customer_id')]

    if not duplicates.empty:
        errors.append("Duplicate customer IDs detected")

    return errors