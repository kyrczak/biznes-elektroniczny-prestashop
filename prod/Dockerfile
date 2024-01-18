FROM prestashop/prestashop:1.7.8.10-apache

RUN apt-get update && \
    apt-get install -y \
        memcached \
        libmemcached-dev \
        libmemcached11 \
        libmemcachedutil2 \
		systemctl

RUN rm -rf /var/www/html/*
COPY --chown=www-data:www-data ./shop/prestashop/src /var/www/html
RUN rm -rf /var/www/html/src/cache/* 

COPY ./shop/db_dump/ /db_dump

COPY ./shop/prestashop.crt /etc/ssl/certs/prestashop.crt
COPY ./shop/prestashop.key /etc/ssl/private/prestashop.key
COPY ./shop/prestashop_ssl.conf /etc/apache2/sites-available/prestashop-ssl.conf

        # Install memcached
RUN apt-get update && apt-get install -y libmemcached-dev libssl-dev zlib1g-dev \
	&& pecl install memcached \
	&& docker-php-ext-enable memcached &&\
        # Enable SSL
        update-ca-certificates &&\
        a2ensite prestashop-ssl &&\
        a2enmod ssl