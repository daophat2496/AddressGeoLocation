def handleAddress(_address, _district, _city) :
    handled_address = ""
    district = ""
    city = ""
    
    if _address :
        handled_address = _address.replace("&", "").replace("#", "")
    if _district:
        district = _district
    if _city : 
        city = _city
    
    return ", ".join([handled_address, district, city])