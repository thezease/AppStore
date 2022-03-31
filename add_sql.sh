# Construct the URI from the .env
DB_HOST=''
DB_NAME=''
DB_USER=''
DB_PORT=''
DB_PASSWORD=''

while IFS= read -r line
do
  if [[ $line == DB_HOST* ]]
  then
    DB_HOST=$(cut -d "=" -f2- <<< $line | tr -d \')
  elif [[ $line == DB_NAME* ]]
  then
    DB_NAME=$(cut -d "=" -f2- <<< $line | tr -d \' )
  elif [[ $line == DB_USER* ]]
  then
    DB_USER=$(cut -d "=" -f2- <<< $line | tr -d \' )
  elif [[ $line == DB_PORT* ]]
  then
    DB_PORT=$(cut -d "=" -f2- <<< $line | tr -d \')
  elif [[ $line == DB_PASSWORD* ]]
  then
    DB_PASSWORD=$(cut -d "=" -f2- <<< $line | tr -d \')
  fi
done < ".env"

URI="postgres://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME"

# Run the scripts to insert data.
psql ${URI} -f sql/99_clean.sql
psql ${URI} -f sql/0_schema_final.sql
psql ${URI} -f sql/1_trigger-functions.sql
psql ${URI} -f sql/2_query-functions-procedures.sql
psql ${URI} -f sql/3_helper-functions.sql
psql ${URI} -f sql/4_demo-dataset.sql
psql ${URI} -f sql/5_users-data.sql
psql ${URI} -f sql/6_apartments-data.sql
psql ${URI} -f sql/7_rentals-data.sql
psql ${URI} -f sql/8_tempbookings-data.sql
