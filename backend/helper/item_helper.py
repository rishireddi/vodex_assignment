def item_helper(item) -> dict:
    return {
        "id": str(item["_id"]), 
        "name": item["name"],
        "email": item["email"],
        "item_name": item["item_name"],
        "quantity": item["quantity"],
        "expiry_date": item["expiry_date"],
        "insert_date": item["insert_date"]
    }