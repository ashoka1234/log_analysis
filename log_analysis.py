import psycopg2

# Connect to database news
db = psycopg2.connect('dbname=news user=vagrant')
cur = db.cursor()

print "What are the most populor three articles of all time?"
cur.execute("SELECT articles.title, popularviews.popularity \
             FROM (SELECT SUBSTR(log.path,10) AS slug, \
                          COUNT(log.path) AS popularity \
                   FROM log, articles \
                   WHERE SUBSTR(log.path, 1, 9) = '/article/' \
                         AND SUBSTR(log.path,10) = articles.slug \
                   GROUP BY log.path \
                   ORDER BY popularity DESC \
                   LIMIT 3) AS popularviews \
             INNER JOIN articles ON articles.slug = popularviews.slug \
             ORDER BY popularity DESC")
for article in cur.fetchall():
    print "\"{}\" - {} views".format(article[0], article[1])

print "\n"
print "Who are the most popular authors of all time?"
cur.execute("SELECT authors.name, popularauthorIds.popularity \
             FROM (SELECT authorId, COUNT(authorId) AS popularity \
                   FROM (SELECT articles.author AS authorId \
                         FROM log, articles \
                         WHERE SUBSTR(log.path, 1, 9) = '/article/' AND \
                               SUBSTR(log.path,10) = articles.slug) \
                         AS articleauthors \
                   GROUP BY authorId \
                   ORDER BY popularity DESC) AS popularauthorIds, authors \
             WHERE popularauthorIds.authorId = authors.id")
for author in cur.fetchall():
    print "\"{}\" - {} views".format(author[0], author[1])

print "\n"
print "On which days did more than 1% of requests lead to errors?"
cur.execute("SELECT COUNT(CASE WHEN SUBSTR(status,1,1) = '4' THEN 1 END) \
                        AS error4xx, \
                    COUNT(CASE WHEN SUBSTR(status,1,1) = '5' THEN 1 END) \
                        AS error5xx, \
                    COUNT(*) AS total, \
                    time::date AS date \
             FROM log \
             GROUP BY date")
for status in cur.fetchall():
    errorratio = ((status[0] + status[1]) / float(status[2]))*100
    if (errorratio > 1.0):
        print "{:%b %d, %Y} - {:2.2f}% errors".format(status[3], errorratio)

db.close()
