#! /bin/bash
# CREATE DATABASE postgresql

echo
echo "Creating database cs532..."
psql -c "CREATE DATABASE cs532_db;"

echo 
echo "Creating Extension unaccent ..."
psql cs532_db -c "CREATE EXTENSION IF NOT EXISTS unaccent;"

echo
echo "Creating Extension cube ..."
psql cs532_db -c "CREATE EXTENSION IF NOT EXISTS cube;"