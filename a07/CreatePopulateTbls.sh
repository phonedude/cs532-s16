#! /bin/bash

# CREATE postgresql movies table
echo
echo "Creating table movie_tb ...."
psql cs532_db -c "CREATE TABLE IF NOT EXISTS movie_tb ( movie_id INT,
                                                        title VARCHAR,
                                                        release_date date,
                                                        video_date date DEFAULT NULL,
                                                        IMDb_url text,
                                                        genre cube DEFAULT '(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)',
                                                        PRIMARY KEY (movie_id));"

echo
echo "Creating table rating_tb ...."
psql cs532_db -c "CREATE TABLE IF NOT EXISTS rating_tb ( user_id INT,
                                                         item_id INT,
                                                         rating INT,
                                                         timestamp INT,
                                                       PRIMARY KEY (user_id, item_id));"

echo
echo "Creating table user_tb ...."
psql cs532_db -c "CREATE TABLE IF NOT EXISTS user_tb ( user_id INT,
                                                         age INT,
                                                         gender VARCHAR,
                                                         occupation VARCHAR,
                                                         zipcode VARCHAR,
                                                       PRIMARY KEY (user_id));"

# CREATE Index for rating's table
echo
echo "Creating index for table rating_tb...."
psql cs532_db -c "CREATE INDEX item_idx ON rating_tb (item_id);"


##
# INSERT or COPY data to postgresql table
echo
echo "Extracting data from ml-100k/u.item into movie_tb"
psql cs532_db -c "\COPY movie_tb (movie_id,
                                  title,
                                  release_date,
                                  IMDb_url,
                                  genre
                                  ) FROM PROGRAM 'python3 TransferMoviesData.py'"
##

##
# INSERT or COPY data to postgresql table
echo
echo "Extracting data from ml-100k/u.data into rating_tb"
psql cs532_db -c "\COPY rating_tb (user_id,
                                  item_id,
                                  rating,
                                  timestamp
                                  ) FROM PROGRAM 'python3 TransferRankingData.py'"



##
# INSERT or COPY data to postgresql table
echo
echo "Extracting data from ml-100k/u.user into user_tb"
psql cs532_db -c "\COPY user_tb ( user_id,
                                  age,
                                  gender,
                                  occupation,
                                  zipcode
                                 )FROM PROGRAM 'python3 TransferUserData.py'"
