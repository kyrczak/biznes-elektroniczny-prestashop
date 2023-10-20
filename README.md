# Docker
Obrazy do pobrania ze strony dockera

`prestashop 1.7.8.10-apache`

`mariadb:10`

## Compose
Na linuxie trzeba pobrac pakiet docker-compose

```c++
//Linux
docker-compose up

//Windows
docker compose up  
```
## Instalacja
Po odpaleniu wchodzisz na `127.0.0.1:8080`

Przechodzisz przez instalacje

**BEZ SSL**

w bazach danych:

nazwa bazy `prestashop`,

user `root`,

haslo `admin`

jak się zainstaluje zmienamy nazwę folderu admin na dowolną inną np admin1 i usuwamy folder `install`. Oba są w `prestashop/src/`.