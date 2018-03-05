#!/usr/bin/python3
# -*- coding: utf-8 -*-

import psycopg2
from datetime import datetime


# Connect to the database and fetch results
def connect(query):
    try:
        # Connect to the Database
        database = psycopg2.connect(database="news")
        c = database.cursor()
        c.execute(query)
        # fetch results from the cursor
        query_results = c.fetchall()
        database.close()
        return query_results
    except BaseException as e:
        print("Error %s" % e)
        return "Error"


# Function to Print Our Results
def print_results(query_results):
    # Prints results
    print('--------------------------')
    if query_results != "Error":
        for i in query_results:
            print('-"{}" -- {} views'.format(i[0], i[1]))
    else:
        print('Error')
    print('\n')


# Question 1. What are the most popular three articles of all time?
def print_popular_articles():
    query = """
    select
        (select title
        from articles
        where slug = substring(l.path from 10))
        as title,
    count(l.path) as articles_count
    from log l
    where l.path != '/'
    group by l.path order by articles_count desc
    limit 3;
    """
    result = connect(query)
    print("1. What are the most popular three articles of all time?")
    print_results(result)


# Question 2. Who are the most popular article authors of all time?
def print_popular_authors():
    query = """
    SELECT
    authors.name,
    count(authors.name) as authors_count
    FROM
    log l
    LEFT JOIN articles ON substring(l.path from 10) = articles.slug
    LEFT JOIN authors ON articles.author = authors.id
    where authors.name != 'None'
    group by authors.name
    order by authors_count desc;
    """
    result = connect(query)
    print("2. Who are the most popular article authors of all time?")
    print_results(result)


# Question 3. On which days did more than 1% of requests lead to errors?
def print_high_error_days():
    query = """
    select
    tmp.time1,
    ROUND(tmp.ok, 2)
    from
        (select date(l.time) as time1,
        (ROUND(count(*) filter (where l.status!='200 OK'), 2) /
        ROUND(count(*), 2)) * 100 as ok
        from log l
        group by time1) as tmp
    WHERE tmp.ok > 1
    ORDER BY tmp.time1 desc;
    """
    result = connect(query)
    print("3. On which days did more than 1% of requests lead to errors?")
    print('--------------------------')
    if result != "Error":
        for i in result:
            print('-{} -- {}% errors'.format(i[0].strftime("%B %d, %Y"), i[1]))
    else:
        print('Error')
    print('\n')


# Run all 3 functions when executed
if __name__ == "__main__":
    print_popular_articles()
    print_popular_authors()
    print_high_error_days()
