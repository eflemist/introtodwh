## Description
This is an ETL application which will create a data warehouse using AWS Redshift Cluster
The tables store data used to analyze data regarding songs and user activity collected from 
a music streaming app. The data is sourced from AWS S3 and loaded into staging tables.
An etl process is executed to move the data from staging tables to fact and dimension tables.
Based on current AWS recommendation, the fact and dimension tables are created with DISTKEY 
and SORTKEY set to AUTO.  This will allow Redshift to distribute and sort the data on the nodes 
appropriately.

## Software required
* AWS Redshift cluster
* Python 3.7
* Python boto3 module

## Files/descriptions
* README.md - contains project/app details
* dwh.cfg - stores the Redshift cluster config variables
* s3_udacity_config.py - python module to reads the dwh.cfg file and stores values as python variables
* s3_udacity_iam_role_create.py - python module that create aws iam role to access s3
* s3_udacity_redshiftclust_create.py - python module to create the redshift cluster
* s3_udacity_redshiftclust_details.py - python module to display cluster details
* s3_udacity_create_tables.py - python module to create staging, fact and dimension tables
* s3_udacity_etl.py - python module to load staging tables from s3, then populate the 
  fact and dimension tables from the staging tables
* s3_udacity_sql_queries.py - module that contains the queires used in etl process
* s3_udacity_redshiftclust_delete.py - module that will delete cluster and iam role

## Setup Instructions
* create an aws account/user
* update the [AWS] section of dwh.cfg file with the KEY/SECRET of aws account/user
* install Python
* intall boto3 module
* execute s3_udacity_iam_role_create.py to create the iam role
* execute s3_udacity_redshiftclust_create.py to create cluster
* execute s3_udacity_redshiftclust_details.py to get host name for cluster
* under the [CLUSTER] section of dwh.cfg, update the HOST value with host name details 
* execute s3_udacity_create_tables.py to create staging and dimension tables
* execute s3_udacity_etl.py - to load staging, fact and dimension tables
* execute s3_udacity_redshiftclust_delete.py to delete the cluster



## Database Info
The following tables are created in the Postgres database
* Staging Tables
  - staging_events - app activity logs from music streaming app
  - staging_songs - metadata about a song and the artist of that song
  
* Fact Table
  - songplay_fact - records in log data associated with song plays 

* Dimension Tables
  - user_dim - stores users in the app

  - song_dim - stores song details

  - artist_dim - stores artists info

  - time_dim - records time dimension details

## Creator

* Ed Flemister
    - [https://github.com/eflemist/introtodwh](https://github.com/eflemist/introtodwh)
 
 
