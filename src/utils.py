def appendToFile(_filename, _content) :
    f = open(_filename, "a")
    f.write(_content)
    f.close()