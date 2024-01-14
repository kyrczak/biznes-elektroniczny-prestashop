FROM prestashop/prestashop:1.7.8.10-apache


RUN rm -rf /var/www/html/*
COPY --chown=www-data:www-data ./shop/prestashop/src /var/www/html
RUN rm -rf /var/www/html/src/cache/* 

COPY ./shop/db_dump/ /db_dump

COPY ./shop/prestashop.crt /etc/ssl/certs/prestashop.crt
COPY ./shop/prestashop.key /etc/ssl/private/prestashop.key
COPY ./shop/prestashop_ssl.conf /etc/apache2/sites-available/prestashop-ssl.conf

        # Enable SSL
RUN     update-ca-certificates &&\
        a2ensite prestashop-ssl &&\
        a2enmod ssl


