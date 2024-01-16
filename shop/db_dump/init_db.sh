MYSQL_HOST="db"
MYSQL_PORT=3306
MYSQL_USER="root"
MYSQL_PASSWORD="student"
MYSQL_DATABASE="BE_188618"
SQL_DUMP_FILE="/db_dump/db.sql"

echo "Creating Database if not exists..."
mysql -h"$MYSQL_HOST" -P"$MYSQL_PORT" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS ${MYSQL_DATABASE};"

echo "Adding SQL dump to the database..."
mysql -h"$MYSQL_HOST" -P"$MYSQL_PORT" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" < "$SQL_DUMP_FILE"
echo "Finished adding db dump to the database..."

exec apache2-foreground
