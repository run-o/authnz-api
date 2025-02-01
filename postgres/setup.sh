#!/bin/bash

psql -U postgres << EOF
CREATE DATABASE authnz;
CREATE USER authnz_owner WITH PASSWORD 'authnz_owner';
GRANT ALL PRIVILEGES ON DATABASE authnz TO authnz_owner;
EOF

psql -U postgres authnz << EOF
CREATE EXTENSION "uuid-ossp";

CREATE USER authnz_user WITH PASSWORD 'authnz_user';

-- grant permissions on all existing tables
GRANT SELECT, UPDATE, INSERT, DELETE ON ALL TABLES in SCHEMA public TO authnz_user;

-- grant permissions on sequences
GRANT SELECT, UPDATE, USAGE ON ALL SEQUENCES in SCHEMA public TO authnz_user;

-- grant funtion execution rights
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO authnz_user;

-- set default privileges for future tables, sequences and functions:
ALTER DEFAULT PRIVILEGES FOR ROLE authnz_owner IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO authnz_user;
ALTER DEFAULT PRIVILEGES FOR ROLE authnz_owner IN SCHEMA public
    GRANT SELECT, UPDATE, USAGE ON SEQUENCES TO authnz_user;
ALTER DEFAULT PRIVILEGES FOR ROLE authnz_owner IN SCHEMA public
    GRANT EXECUTE ON FUNCTIONS TO authnz_user;
EOF