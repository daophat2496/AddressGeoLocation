import os
import requests
import mysql.connector
import configparser
import load_configurations as LoadConfig
import handle_address as HandleAddress
import parse_gelocation_json as ParseGeoLocationJSON
import query_string as QueryString
import utils as Utils
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
    select_query_builder = QueryString.select_query_base + QueryString.select_query_condition + QueryString.select_query_order_limit
    ggm_request = """https://maps.googleapis.com/maps/api/geocode/json?address="{0}"&key={1}"""
    update_request = QueryString.update_request

    while True :
        if os.stat('error_ids.txt').st_size == 0 :
            error_ids_condition = ""
        else :
            error_list_file = open('error_ids.txt')
            error_ids_condition = QueryString.select_query_error_id_condition.format(", ".join(line.strip() for line in error_list_file))
            error_list_file.close()
        
        select_query_builder = QueryString.select_query_base + QueryString.select_query_condition+ error_ids_condition + QueryString.select_query_order_limit
        # select_query_builder = """ SELECT id, address, district_id, city_id 
        #         FROM school_students 
        #         WHERE id = 2344"""
        print(select_query_builder.format(configs["batch_size"]))
        mycursor.execute(select_query_builder.format(configs["batch_size"]))
        myresult = mycursor.fetchall()
        print(myresult)

        if not myresult :
            break

        for student in myresult :
            handled_address = HandleAddress.handleAddress(student[1], district_dict.get(student[2]), city_dict.get(student[3]))
            response = requests.get(ggm_request.format(handled_address, configs["google_api_key"]))
            if response.status_code == 200 :
                if response.json()["status"] != "OK" :
                    Utils.appendToFile("error_details.txt","{} - {}\n".format(student[0], response.json()))
                    Utils.appendToFile("error_ids.txt", "{}\n".format(student[0]))
                else :
                    status, lat, lng, plid = ParseGeoLocationJSON.parseGeoLocationJSON(response.json())
                    try :
                        mycursor.execute(update_request.format(lat, lng, plid, student[0]))
                        Utils.appendToFile("success_ids.txt", "{}\n".format(student[0]))
                        print("0k")
                    except Exception as ex:
                        Utils.appendToFile("error_details.txt","{} - {}\n".format(student[0], ex))
                        Utils.appendToFile("error_ids.txt", "{}\n".format(student[0]))
            else :
                Utils.appendToFile("error_details.txt","{} - {}\n".format(student[0], response.json()))
        
        mydb.commit()
    
    mycursor.close()

if __name__ == "__main__" :
    main()