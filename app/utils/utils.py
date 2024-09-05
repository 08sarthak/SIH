def prettify_response(data):
    response = {
        "Catalog UUID": data["catalog_uuid"],
        "Description": data["desc"],
        "Created Date": data["created_date"],
        "Title": data["title"],
        "Source": data["source"],
        "Total Entries": data["total"],
        "Last Updated Date": data["updated_date"],
        "Market Prices Data": []
    }
    
    for entry in data["field"]:
        if "Arrival_Date" in entry:
            market_data = {
                "Arrival Date": entry["Arrival_Date"],
                "Commodity": entry["Commodity"],
                "District": entry["District"],
                "Market": entry["Market"],
                "Max Price": entry["Max_Price"],
                "Min Price": entry["Min_Price"],
                "Modal Price": entry["Modal_Price"],
                "State": entry["State"],
                "Variety": entry["Variety"]
            }
            response["Market Prices Data"].append(market_data)
    
    return response