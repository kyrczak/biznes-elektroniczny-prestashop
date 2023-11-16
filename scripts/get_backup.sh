newest_backup=$(find ./backups/ -type f -name "backup*.zip" | sort -n | tail -1)

if [ -z "$newest_backup" ]; then
  echo "No backup file found."
  exit 1
fi


unzip "$newest_backup" -d ./backups/


db_dump_dir=$(find ./backups/ -type d -name "db_dump")
mariadb_dir=$(find ./backups/ -type d -name "mariadb")
prestashop_dir=$(find ./backups/ -type d -name "prestashop")


if [ -d "$db_dump_dir" ]; then
  cp -r "$db_dump_dir" ../shop/ && echo "Copied $db_dump_dir to ../shop/"
  rm -rf "$db_dump_dir"
fi

if [ -d "$mariadb_dir" ]; then
  cp -r "$mariadb_dir" ../shop/ && echo "Copied $mariadb_dir to ../shop/"
  rm -rf "$mariadb_dir"
fi

if [ -d "$prestashop_dir" ]; then
  cp -r "$prestashop_dir" ../shop/ && echo "Copied $prestashop_dir to ../shop/"
  rm -rf "$prestashop_dir"
fi

