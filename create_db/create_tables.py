#!/usr/bin/python3
# coding: utf8

import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = "../mycards.db"

    sql_create_cards_prices_table = """ CREATE TABLE IF NOT EXISTS cards_prices (
                                        set_id text,
                                        number integer,
                                        date text,
                                        price integer,
                                        quantity integer
                                    ); """

    sql_create_cards_table = """ CREATE TABLE IF NOT EXISTS cards (
                                        set_id text,
                                        number integer,
                                        promo text,
                                        lang text,
                                        quantity integer,
					album_id integer
                                    ); """
    sql_create_albums_table = """ CREATE TABLE IF NOT EXISTS albums (
                                        id integer,
                                        name text
                                    ); """
    sql_create_colors_table = """ CREATE TABLE IF NOT EXISTS colors (
                                        id integer,
                                        name_en text,
					name_ru text
                                    ); """
    sql_create_total_data_table = """ CREATE TABLE IF NOT EXISTS total_data (
                                        date text,
                                        price integer,
                                        quantity integer
                                    ); """

    sql_create_cards_names = """ CREATE TABLE IF NOT EXISTS cards_names (
                                        set_id text,
                                        number integer,
                                        lang text,
                                        name text
                                    ); """
    sql_create_cards_data = """ CREATE TABLE IF NOT EXISTS cards_data (
                                        set_id text,
                                        number integer,
                                        lang text,
                                        name text,
					color integer
                                    ); """


    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_cards_prices_table)
        create_table(conn, sql_create_total_data_table)
        create_table(conn, sql_create_cards_names)
        create_table(conn, sql_create_albums_table)
        create_table(conn, sql_create_colors_table)
        create_table(conn, sql_create_cards_table)
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
