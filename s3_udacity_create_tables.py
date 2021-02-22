import psycopg2
from s3_udacity_sql_queries import create_table_queries, drop_table_queries
import s3_udacity_config as db_config


def drop_tables(cur, conn):
    """ removes tables from db using the drop table queries from the s3_udacity_sql_queries module """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()

def create_tables(cur, conn):
    """ create tables in db using the create table queries from the s3_udacity_sql_queries module """
    for query in create_table_queries:
        print(query)
        cur.execute(query)
        conn.commit()


def main():

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(db_config.DWH_HOST, db_config.DWH_DB, db_config.DWH_DB_USER, db_config.DWH_DB_PASSWORD, db_config.DWH_PORT))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()