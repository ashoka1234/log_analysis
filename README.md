# Log Analysis
Log Analysis is a simple reporting tool of a news database which consists of articles, authors, and log tables. The tool is written in Python and the database is a PostgreSQL installed in a virtual machine. The connection to the database is via a vagrant connection to the virtual machine.

# Install
A PostgreSQL database is required which could be installed in a virtual machine. A vagrant connection could be used to connect to the virtual machine from a windows shell.

The database is called `news`. The tables could be created and populated by running the SQL file `newsdata.sql` in the `vagrant` directory using the following command:

`psql -d news -f newsdata.sql`

The tool is in a single source file `log_analysis.py`

# Run
Simply run the following Python interpreter in a shell.

`python  log_analysis.py`

In a windows machine with PostgreSQL installed in a virtual machine, run the above command in a shell that has established a vagrant connection (e.g. vagrant ssh) to the virtual machine that hosts the database. The output of the tool is displayed on the console.
