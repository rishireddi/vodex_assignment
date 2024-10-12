def clock_in_record_helper(item) -> dict:
    return {
        "id": str(item["_id"]), 
        "email": item["email"],
        "location": item["location"],
        "insert_date": item["insert_date"]
    }