update_request = """ UPDATE school_students 
                        SET address_latitude = '{0}', 
                            address_longitude = '{1}', 
                            address_place_id = '{2}' 
                        WHERE id = {3};"""

select_query_base = """ SELECT id, address, district_id, city_id 
                    FROM school_students 
                    WHERE 1 = 1"""

select_query_condition = """ AND (address_latitude IS NULL OR address_longitude IS NULL) AND (address IS NOT NULL OR district_id IS NOT NULL OR city_id IS NOT NULL)"""

select_query_error_id_condition = """ AND id NOT IN ({})"""

select_query_order_limit = """ ORDER BY id ASC LIMIT {};"""