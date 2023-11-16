FROM prestashop/prestashop:1.7.8.10-apache

COPY ./prestashop.crt /etc/ssl/certs/prestashop.crt
COPY ./prestashop.key /etc/ssl/private/prestashop.key
COPY ./prestashop.crt /usr/local/share/ca-certificates/prestashop.crt
COPY ./prestashop-ssl.conf /etc/apache2/sites-enabled/prestashop-ssl.conf

RUN update-ca-certificates && a2enmod ssl && a2ensite prestashop-ssl.conf