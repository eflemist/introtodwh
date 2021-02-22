import s3_udacity_config as db_config
import boto3

iam_resource = boto3.client('iam',
                             region_name='us-west-2',                            
                             aws_access_key_id=db_config.KEY,
                             aws_secret_access_key=db_config.SECRET
                            )

roleArn = iam_resource.get_role(RoleName=db_config.DWH_IAM_ROLE_NAME)['Role']['Arn']

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_fact_table_drop = "DROP TABLE IF EXISTS songplay_fact"
user_dim_table_drop = "DROP TABLE IF EXISTS user_dim"
song_dim_table_drop = "DROP TABLE IF EXISTS song_dim"
artist_dim_table_drop = "DROP TABLE IF EXISTS artist_dim"
time_dim_table_drop = "DROP TABLE IF EXISTS time_dim"

# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE IF NOT EXISTS staging_events
                                 (artist varchar,
                                  auth varchar,
                                  firstName varchar,
                                  gender varchar,
                                  itemInSession varchar,
                                  lastName varchar,
                                  length varchar,
                                  level varchar,
                                  location varchar,
                                  method varchar,
                                  page varchar,
                                  registration varchar,
                                  sessionId varchar,
                                  song varchar,
                                  status varchar,
                                  ts varchar,
                                  userAgent varchar,
                                  userId varchar);
                               """)

staging_songs_table_create = ("""CREATE TABLE IF NOT EXISTS staging_songs
                                 (song_id varchar,
                                  num_songs varchar,
                                  title varchar(4000),
                                  artist_name varchar(4000),
                                  artist_latitude varchar,
                                  year varchar,
                                  duration varchar,
                                  artist_id varchar,
                                  artist_longitude varchar,
                                  artist_location varchar(4000))
                              """)

user_dim_table_create = ("""CREATE TABLE IF NOT EXISTS user_dim
                            (user_id int,
                             first_name varchar,
                             last_name varchar,
                             gender varchar,
                             level varchar,
                             primary key(user_id))
                             DISTSTYLE AUTO
                             SORTKEY AUTO;
                          """)


song_dim_table_create = ("""CREATE TABLE IF NOT EXISTS song_dim
                            (song_id varchar,
                             artist_id varchar,
                             title varchar(4000),
                             year varchar,
                             duration varchar,
                             primary key(song_id))
                             DISTSTYLE AUTO
                             SORTKEY AUTO;
                          """)

artist_dim_table_create = ("""CREATE TABLE IF NOT EXISTS artist_dim
                              (artist_id varchar,
                               name varchar(4000),
                               location varchar(4000),
                               latitude varchar(4000),
                               longitude varchar(4000),
                               primary key(artist_id))
                               DISTSTYLE AUTO
                               SORTKEY AUTO;
                            """)

time_dim_table_create = ("""CREATE TABLE IF NOT EXISTS time_dim
                            (start_time datetime,
                             year varchar,
                             month varchar,
                             week varchar,
                             day varchar,
                             hour varchar,
                             primary key(start_time))
                             DISTSTYLE AUTO
                             SORTKEY AUTO;
                          """)

songplay_fact_table_create = ("""CREATE TABLE IF NOT EXISTS songplay_fact
                                 (songplay_id int IDENTITY(0,1),
                                 song_id varchar,
                                 artist_id varchar,
                                 session_id int,
                                 user_id int,
                                 level varchar,
                                 location varchar,
                                 start_time varchar,
                                 user_agent varchar,
                                 primary key(songplay_id),
                                 foreign key(song_id) references song_dim(song_id),
                                 foreign key(artist_id) references artist_dim(artist_id),
                                 foreign key(user_id) references user_dim(user_id),
                                 foreign key(start_time) references time_dim(start_time))
                                 DISTSTYLE AUTO
                                 SORTKEY AUTO;
                              """)

# STAGING TABLES

staging_events_copy = ("""copy staging_events from {} 
                          credentials 'aws_iam_role={}'
                          json {}
                          emptyasnull
                          blanksasnull
                          TIMEFORMAT 'epochmillisecs'
                          region 'us-west-2';
                       """).format(db_config.DWH_LOG_DATA, roleArn, db_config.DWH_LOGJSONPATH)

staging_songs_copy = ("""copy staging_songs from {}
                         credentials 'aws_iam_role={}'
                         json 'auto'
                         emptyasnull
                         blanksasnull                         
                         region 'us-west-2';                         
                       """).format(db_config.DWH_SONG_DATA, roleArn)


# FINAL TABLES

user_table_insert = ("""INSERT INTO user_dim
                        (select distinct userId::int, firstName, lastName, gender, level
                        from staging_events
                        where userId is not null
                          and page = 'NextSong')""")
 
song_table_insert = ("""INSERT INTO song_dim
                        (select distinct song_id, artist_id, title, year, duration
                        from staging_songs)""")

artist_table_insert = ("""INSERT INTO artist_dim (select distinct artist_id, artist_name, artist_latitude, artist_longitude, artist_location
                          from staging_songs)""")

time_table_insert = ("""INSERT INTO time_dim (start_time)
                        (select timestamp 'epoch' + CAST(ts AS BIGINT)/1000 * interval '1 second' AS start_time from staging_events)""")

time_table_update = ("""UPDATE time_dim 
                        SET year =  (EXTRACT (YEAR FROM start_time)),
                            month =  (EXTRACT (MONTH FROM start_time)),
                            week =  (EXTRACT (WEEK FROM start_time)),
                            day =  (EXTRACT (DAY FROM start_time)),
                            hour =  (EXTRACT (HOUR FROM start_time))  """)

songplay_table_insert = ("""INSERT INTO songplay_fact (song_id, artist_id, session_id,  user_id, level, location, start_time,  user_agent)
                            (SELECT ss.song_id,
                                    ss.artist_id,
                                    se.sessionid::int,
                                    se.userid::int,
                                    se.level,
                                    se.location,
                                    timestamp 'epoch' + CAST(se.ts AS BIGINT)/1000 * interval '1 second' AS start_time,
                                    se.useragent
                              FROM staging_events AS se 
                              JOIN staging_songs AS ss
                                ON (se.artist = ss.artist_name)
                               AND (se.length = ss.duration)
                             WHERE se.page = 'NextSong')""")
# QUERY LISTS

create_table_queries = [staging_events_table_create,
                        staging_songs_table_create,
                        user_dim_table_create,
                        song_dim_table_create,
                        artist_dim_table_create,
                        time_dim_table_create,
                        songplay_fact_table_create]


drop_table_queries = [staging_events_table_drop,
                      staging_songs_table_drop,
                      songplay_fact_table_drop,
                      user_dim_table_drop,
                      song_dim_table_drop,
                      artist_dim_table_drop,
                      time_dim_table_drop]


copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [user_table_insert, song_table_insert, artist_table_insert, time_table_insert, songplay_table_insert]
update_table_queries = [time_table_update]