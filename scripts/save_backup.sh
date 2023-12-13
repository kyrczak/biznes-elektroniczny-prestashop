#!/bin/bash

docker exec presta-mariadb mysqldump --user=root --password=admin prestashop > ../shop/db_dump/db.sql

timestamp=$(date +%s)


db_dump_dir=$(find ../shop/ -type d -name "db_dump")
prestashop_dir=$(find ../shop/ -type d -name "prestashop" -not -path "../shop/mariadb/prestashop")

chmod -R 777 $db_dump_dir
chmod -R 777 $prestashop_dir

#if no 'backups' directory here then create one
if [ ! -d "./backups" ]; then
  mkdir ./backups
fi

#let user put backup name
echo "Nazwa backupu: "
read backup_name


#tar the folders with access rights 
tar -czf ./backups/$backup_name-$timestamp.tar.gz $db_dump_dir $prestashop_dir
