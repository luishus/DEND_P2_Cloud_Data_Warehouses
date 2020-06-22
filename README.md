# Project 3: Data Warehouse

## Summary

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. The data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

Thre purpose is build an ETL pipeline for a database hosted on Redshift. We will load data from S3 to staging tables on Redshift and execute SQL statements that create the analytics tables from these staging tables.

## Schema design and ETL pipeline

The star schema has 1 *fact* table (songplays), and 4 *dimension* tables (users, songs, artists, time).


### Staging tables

#### staging_events

|   Column       |            Type             | 
| -------------- | --------------------------- | 
| artist         | varchar                     | 
| auth           | varchar                     | 
| firstName      | varchar                     | 
| gender         | varchar                     | 
| itemInSession  | integer                     | 
| lastName       | varchar                     | 
| length         | float                       | 
| level          | varchar                     | 
| location       | varchar                     |
| method         | varchar                     | 
| page           | varchar                     | 
| registration   | float                       | 
| sessionId      | integer                     | 
| song           | varchar                     | 
| status         | integer                     | 
| ts             | timestamp                   | 
| userAgent      | varchar                     | 
| userId         | integer                     | 


#### staging_songs

|   Column          |            Type             | 
| ----------------- | --------------------------- | 
| num_songs         | integer                     | 
| artist_id         | varchar                     | 
| artist_latitude   | float                       | 
| artist_longitude  | float                       | 
| artist_location   | varchar                     | 
| artist_name       | varchar                     | 
| song_id           | varchar                     | 
| title             | varchar                     | 
| duration          | float                       | 
| year              | integer                     |



### Fact tables

#### Songplays

Records in log data associated with song plays.

|   Column    |            Type             | 
| ----------- | --------------------------- | 
| songplay_id | integer                     | 
| start_time  | timestamp                   | 
| user_id     | integer                     | 
| level       | varchar                     | 
| song_id     | varchar                     | 
| artist_id   | varchar                     | 
| session_id  | integer                     | 
| location    | varchar                     | 
| user_agent  | varchar                     | 

Primary key: songplay_id
Distribution key: start_time
Sort key: start_time

### Dimension tables

#### Users

Users in the app.

|   Column   |       Type        | 
| ---------- | ----------------- | 
| user_id    | integer           | 
| first_name | varchar           | 
| last_name  | varchar           | 
| gender     | varchar           | 
| level      | varchar           | 

Primary key: user_id
Sort key: user_id

#### Songs

Songs in music database.

|  Column   |         Type          |
| --------- | --------------------- |
| song_id   | varchar               |
| title     | varchar               |
| artist_id | varchar               |
| year      | integer               |
| duration  | float                 |

Primary key: song_id
Sort key: song_id

#### Artists

Artists in music database.

|  Column   |         Type          |
| --------- | --------------------- |
| artist_id | varchar               |
| name      | varchar               |
| location  | varchar               |
| latitude  | float                 |
| longitude | float                 |

Primary key: artist_id
Sort key: artist_id

#### Time

Timestamps of records in songplays.

|   Column   |            Type             | 
| ---------- | --------------------------- | 
| start_time | timestamp                      | 
| hour       | integer                     | 
| day        | integer                     | 
| week       | integer                     | 
| month      | integer                     | 
| year       | integer                     | 
| weekday    | integer                     | 

Primary key: start_time
Distribution key: start_time
Sort key: start_time


Extract, transform, load processes in **etl.py** populate the **songs** and **artists** tables with data derived from the JSON song files, `data/song_data`. Processed data derived from the JSON log files, `data/log_data`, is used to populate **time** and **users** tables. A `SELECT` query collects song and artist id from the **songs** and **artists** tables and combines this with log file derived data to populate the **songplays** fact table.


## Run

Run the scripts to create database tables:

```
./create_tables.py
```

and populate data into tables:

```
./etl.py
```

Data can be verified using the provided `sample_queries.py` or through AWS Query Editor:

```
./sample_queries.py
```

## Sample queries

Identify the number of users by level (free or paid).

`SELECT level, COUNT(user_id) FROM users GROUP BY level;`

Identify the number of songplays by artist.

`SELECT a.name, COUNT(sp.songplay_id) FROM artists a JOIN songplays sp ON sp.artist_id = a.artist_id GROUP BY a.name;`

Weekday with more listeners

`SELECT COUNT(weekday) FROM time;`

Indentify the number of listeners by weekday

`SELECT t.weekday,COUNT(sp.songplay_id) FROM time t JOIN songplays sp ON sp.start_time = t.start_time GROUP BY t.weekday ORDER BY 2 DESC`