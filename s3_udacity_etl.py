import s3_udacity_config as db_config
import psycopg2
from s3_udacity_sql_queries import copy_table_queries, insert_table_queries, update_table_queries

def load_staging_tables(cur, conn):
    """ loads the staging tables from s3 using the copy command in the s3_udacity_sql_queries module """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """ insert data into fact and dimension tables the staging tables using insert queries from s3_udacity_sql_queries module """
    for query in insert_table_queries:
        #print(query)
        cur.execute(query)
        conn.commit()

def update_tables(cur, conn):
    """ update records in the time_dim table using update queries from s3_udacity_sql_queries module """
    for query in update_table_queries:
        cur.execute(query)
        conn.commit()
        
def main():

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(db_config.DWH_HOST, db_config.DWH_DB, db_config.DWH_DB_USER, db_config.DWH_DB_PASSWORD, db_config.DWH_PORT))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)
    update_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()