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

ip bazy `presta-mariadb`

nazwa bazy `prestashop`,

user `root`,

haslo `admin`

jak się zainstaluje zmienamy nazwę folderu admin na dowolną inną np admin1 i usuwamy folder `install`. Oba są w `prestashop/src/`.

## Uruchomienie sklepu

1. Wchodzimy do folderu `shop`

2. Generujemy certyfikat ssl:
```c++
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout prestashop.key -out prestashop.crt -subj "/C=PL/ST=Pomeranian Voivodeship/L=Gdansk/O=Donice Hermiony/OU=Donice Hermiony/CN=localhost"
```

3. Uruchamiamy kontenery za pomocą:
```c++
docker-compose up -d
```

4. W przeglądarce sieciowej wchodzimy na adres https://localhost

5. Przy pierwszym uruchomieniu będziemy musieli zaakceptować certyfikat

6. Aby zatrzymać działanie kontenerów:
```c++
docker-compose down
```