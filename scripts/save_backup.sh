#!/bin/bash

docker exec presta-mariadb mysqldump --user=root --password=admin prestashop > ../shop/db_dump/db.sql

timestamp=$(date +%s)


db_dump_dir=$(find ../shop/ -type d -name "db_dump")
mariadb_dir=$(find ../shop/ -type d -name "mariadb")
prestashop_dir=$(find ../shop/ -type d -name "prestashop")


zip -r ./backups/backup$timestamp.zip $db_dump_dir $mariadb_dir $prestashop_dir
