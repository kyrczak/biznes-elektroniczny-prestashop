newest_backup=$(find ./backups/ -type f -name "backup*.tar.gz" | sort -n | tail -1)

if [ -z "$newest_backup" ]; then
  echo "No backup file found."
  exit 1
fi

# untar the backup with access rights
tar -xzf "$newest_backup" -C ./backups/


db_dump_dir=$(find ./backups/shop -type d -name "db_dump")
prestashop_dir=./backups/shop/prestashop


if [ -d "$db_dump_dir" ]; then
  cp -r "$db_dump_dir" ../shop/ && echo "kopiuje $db_dump_dir do ../shop/"
  rm -rf "$db_dump_dir"
fi

if [ -d "$prestashop_dir" ]; then
  cp -r "$prestashop_dir" ../shop/ && echo "kopiuje $prestashop_dir do ../shop/"
  rm -rf "$prestashop_dir"
  rm -rf ./backups/shop

  sudo rm -r ../shop/mariadb/
  echo "usuwam ../shop/mariadb/"
fi

# if mariadb doesnt exist
if [ ! -d "../shop/mariadb" ]; then
  sudo chmod -R 777 ../shop/db_dump
  sudo chmod -R 777 ../shop/prestashop
  echo "Backup przywrócony"
fi

