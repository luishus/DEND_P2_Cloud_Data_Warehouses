import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries, select_sample_queries


def load_staging_tables(cur, conn):
    '''
    Load files from S3 into Redshift tables.
    '''
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    '''
    Load data from staging tables, transform data and insert into new tables
    '''
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    '''
        - Establishes connection with the sparkify database and gets
        cursor to it.  

        - Load all log and song files from S3 into Redshift
        
        - Load data from staging tables, transform data and insert into new tables

        - Finally, closes the connection. 
    '''
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()