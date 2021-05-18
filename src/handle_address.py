def handleAddress(_address, _district, _city) :
    if not _address :
        return _district + _city
    else :
        return _address.replace("&", "")