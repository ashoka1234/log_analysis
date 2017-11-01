#!/usr/bin/env python
import psycopg2

# Connect to database news
db = psycopg2.connect('dbname=news user=vagrant')
cur = db.cursor()

print "What are the most populor three articles of all time?"
cur.execute("""SELECT articles.title, COUNT(log.path) AS popularity
               FROM log, articles
               WHERE CONCAT('/article/', articles.slug) = log.path
               GROUP BY articles.title
               ORDER BY popularity DESC
               LIMIT 3""")
for article in cur.fetchall():
    print "\"{}\" - {} views".format(article[0], article[1])

print "\n"
print "Who are the most popular authors of all time?"
cur.execute("""SELECT authors.name, popularauthorIds.popularity
               FROM (SELECT authorId, COUNT(authorId) AS popularity
                     FROM (SELECT articles.author AS authorId
                           FROM log, articles
                           WHERE CONCAT('/article/', articles.slug) = log.path)
                           AS articleauthors
                     GROUP BY authorId
                     ORDER BY popularity DESC) AS popularauthorIds, authors
               WHERE popularauthorIds.authorId = authors.id""")
for author in cur.fetchall():
    print "\"{}\" - {} views".format(author[0], author[1])

print "\n"
print "On which days did more than 1% of requests lead to errors?"
cur.execute("""
       SELECT error_pct, to_char(date, 'FMMonth FMDD, YYYY') as date
       FROM (SELECT 100.0*(
                    COUNT(CASE WHEN SUBSTR(status,1,1) = '4' THEN 1 END)
                         +
                    COUNT(CASE WHEN SUBSTR(status,1,1) = '5' THEN 1 END))
                         /
                    COUNT(*) AS error_pct, time::date AS date
             FROM log
             GROUP BY date) AS daily_errors
       WHERE error_pct > 1.0""")
for status in cur.fetchall():
    print "{} - {:2.2f}% errors".format(status[1], status[0])

db.close()
