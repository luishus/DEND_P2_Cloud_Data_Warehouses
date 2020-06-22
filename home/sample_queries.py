import configparser
import psycopg2
from sql_queries import select_sample_queries
from prettytable import PrettyTable


        
def select_queries(cur, conn):
    """
    Run select queries
    """
    for query in select_sample_queries:
        print('Running ' + query)
        cur.execute(query)
        conn.commit()
        results = cur.fetchall()

        print("Total rows are:  ", len(results))
        print("Printing each row")
        for row in results:
            print(row)


def main():
    '''
        - Establishes connection with the sparkify database and gets
        cursor to it.  

        - Run sample queries
        
        - Finally, closes the connection. 
    '''
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    select_queries(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()