    new_customers = []
    # Iterating through customer df to find new customers
    for customer in df_customer.values:
        reference = customer[0]
        name = customer[1]
        # If we have a new customer we add to db and to new customer df
        if db.get_customer(reference) is None:
            logger.debug(f"Adding Customer to db - reference: %s, name: %s", reference, name)
            # print(f" row = {row}")
            db.add_customer(reference, name)
            new_customers.append()