CREATE DATABASE ecommerce;
CREATE USER ironman WITH PASSWORD 'ironman';
ALTER ROLE ironman SET client_encoding TO 'utf8';
ALTER ROLE ironman SET default_transaction_isolation TO 'read committed';
ALTER ROLE ironman SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE ecommerce TO ironman;
