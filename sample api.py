  curl -X 'POST' \
     'localhost/api/v1/database' \
     -H 'accept: application/json' \
     -H 'Content-Type: application/json' \
     -d '{
       "db_alias": "postgres",
       "use_ssh": false,
       "connection_uri": "postgresql+psycopg2://hakkoda:P@ssw0rd@hakkoda.postgres.database.azure.com:5432/postgres"

     }'

curl -X 'POST' \
  'http://localhost/api/v1/scanner' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "db_alias": "postgres_new"
}'