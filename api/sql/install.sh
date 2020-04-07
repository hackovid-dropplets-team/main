# determine os
unameOut="$(uname -s)"
case "${unameOut}" in
    Darwin*)    pg_cmd="psql -U postgres";;
    *)          pg_cmd="sudo -u postgres psql"
esac

${pg_cmd} -c "DROP DATABASE IF EXISTS dropplets;"
${pg_cmd} -c "DROP ROLE IF EXISTS dropplets_user;"
${pg_cmd} -c "CREATE USER dropplets_user WITH PASSWORD 'dropplets_pass';"
${pg_cmd} -c "CREATE DATABASE dropplets ENCODING 'UTF8';"
${pg_cmd} -c "GRANT ALL PRIVILEGES ON DATABASE dropplets TO dropplets_user;"

cat sql/create_tables.sql | ${pg_cmd} -d dropplets -a
cat sql/sample_data.sql | ${pg_cmd} -d dropplets -a
