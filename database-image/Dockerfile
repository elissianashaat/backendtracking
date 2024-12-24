FROM mongo:latest

# Set permissions for the /data/db directory
RUN mkdir -p /data/db && chown -R mongodb:mongodb /data/db

USER mongodb

EXPOSE 27017
CMD ["mongod"]
