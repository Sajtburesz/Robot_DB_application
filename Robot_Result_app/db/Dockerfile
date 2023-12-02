FROM postgres:latest
COPY ./db-entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/*
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]