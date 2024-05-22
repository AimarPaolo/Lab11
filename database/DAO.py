from database.DB_connect import DBConnect
from model.product import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllProducts():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                from go_products"""
        cursor.execute(query)
        for row in cursor:
            result.append(
                Product(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllPesi(anno, v0, v1):
        conn = DBConnect.get_connection()

        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select count(distinct gds2.`Date`) as peso
                    from go_sales.go_daily_sales gds , go_sales.go_daily_sales gds2 
                    where gds2.Date = gds.Date 
                    and year (gds.Date) = %s  
                    and gds2.Retailer_code = gds.Retailer_code 
                    and gds.Product_number = %s 
                    and gds2.Product_number = %s"""
        cursor.execute(query, (anno, v0, v1, ))
        for row in cursor:
            result.append(row["peso"])
        cursor.close()
        conn.close()
        return result[0]
