import os
import requests
import mysql.connector
import configparser
import load_configurations as LoadConfig
import handle_address as HandleAddress
import parse_gelocation_json as ParseGeoLocationJSON
import json

def main() :
    configs = LoadConfig.loadConfigurations()
    
    mydb = mysql.connector.connect(
        host=configs["db_url"],
        user=configs["db_username"],
        password=configs["db_password"],
        database=configs["db_dbname"],
    )
    mycursor = mydb.cursor()

    # Get District dictionary
    city_dict = {}
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id, name FROM cities;")
    myresult = mycursor.fetchall()

    for city in myresult :
        city_dict[city[0]]= city[1]

    # Get District dictionary
    district_dict = {}
    mycursor.execute("SELECT id, name FROM districts;")
    myresult = mycursor.fetchall()

    for district in myresult :
        district_dict[district[0]]= district[1]

    # Main
    f = open("error_details.txt", "a")
    mycursor.execute("""SELECT id, address, district_id, city_id FROM school_students WHERE 1 = 1 ORDER BY id ASC LIMIT {0};""".format(configs["batch_size"]))
    myresult = mycursor.fetchall()
    ggm_request = """https://maps.googleapis.com/maps/api/geocode/json?address="{0}"&key={1}"""
    for student in myresult :
        handled_address = HandleAddress.handleAddress(student[1], student[2], student[3])
        response = requests.get(ggm_request.format(handled_address, configs["google_api_key"]))
        if response.status_code == 200 :
            print(ParseGeoLocationJSON.parseGeoLocationJSON(response.json()))
        else :
            f.write("StudentID: {0}. Error: {1}".format(student[1], response.content()))

    f.close()

if __name__ == "__main__" :
    main()