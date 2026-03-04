
from . import  tool
def count_occurrences_in_db(database,table_name, column_name):
        connection = tool.get_db_connection(database)
        cursor = connection.cursor()


        query = f"""
            SELECT {column_name}, COUNT(*) as occurrence 
            FROM {table_name} 
            GROUP BY {column_name} 
            ORDER BY occurrence DESC
        """
        cursor.execute(query)


        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results

if __name__ == "__main__":
 data = count_occurrences_in_db('health_record','record','disease')
 print(data)