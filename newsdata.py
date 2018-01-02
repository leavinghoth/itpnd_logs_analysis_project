#! /usr/bin/env python

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
    except BaseException:
        print("No results")

# Function to Print Our Results
'''def print_results(query_results):
    # Prints results
    for i in query_results:
        print('"' + i[0] + '"' + ' -- ' + i[1])
    print '\n'

'''


# Question 1. What are the most popular three articles of all time?
def print_popular_articles():
    print " The Most Viewed Articles "
    print '--'
    query1 = """
            select title, concat(concat(page_views,' '), 'views')as views
            from most_viewed_articles limit 3;
            """
    popular_articles = connect(query1)
    print_results(popular_articles)

# Question 2. Who are the most popular article authors of all time?
def print_popular_authors():
    print " The Most Popular Authors Are: "
    print '--'
    query2 = """
            select name, concat(concat(page_views,' '), 'views')as views
            from most_popular_author join authors on most_popular_author.author = authors.id
            limit 4;
            """
    popular_authors = connect(query2)

    print_results(popular_authors)

# Question 3. On which days did more than 1% of requests lead to errors?    
'''def print_high_error_days():
    """Return the days where errors exceeded 1%"""
    query3 = """SELECT errors.day,
            ROUND(
            ((errors.errors/total.total) * 100)::DECIMAL, 2)::TEXT
            as percentage
            FROM errors, total
            WHERE total.day = errors.day
            AND (((errors.errors/total.total) * 100) > 1.0)
            ORDER BY errors.day;"""
    high_error_days = connect(query3)
    # Display header and results for Problem 3
    print('**** Days Where Errors Exceeded 1%' + ' of Total Views ****')
    for i in high_error_results:
        print(i[0].strftime('%B %d, %Y') + " -- " + i[1] + "%" + " errors")
        print(' ') 


    print_results(high_error_days)
'''
'''
# Question 3. On which days did more than 1% of requests lead to errors?
def print_error_request():
    print " Days in which more than 1% of requests lead to errors "
    print '--'
    query3 = """
            select date, concat(concat(daily_error_percentage,'%'), ' errors')
            as percentage
            from daily_error_percentage_table limit 1;
            """
    error_request = connect(query3)
    for i in error_request:
        print(i[0].strftime('%B %d, %Y') + ' -- ' + i[1])
    print '\n'
'''
# Run all 3 functions when executed
if __name__ == "__main__":
    print_popular_articles()
    print_popular_authors()
    #print_high_error_days()