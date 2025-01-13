#!/bin/bash

psql -U postgres << EOF
CREATE DATABASE authnz_test;
GRANT ALL PRIVILEGES ON DATABASE authnz_test TO authnz_owner;
EOF

psql -U postgres authnz_test << EOF
CREATE EXTENSION "uuid-ossp";
GRANT SELECT, UPDATE, INSERT, DELETE ON ALL TABLES in SCHEMA public TO authnz_user;
GRANT SELECT, UPDATE, USAGE ON ALL SEQUENCES in SCHEMA public TO authnz_user;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO authnz_user;

ALTER DEFAULT PRIVILEGES FOR ROLE authnz_owner IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO authnz_user;
ALTER DEFAULT PRIVILEGES FOR ROLE authnz_owner IN SCHEMA public GRANT USAGE ON SEQUENCES TO authnz_user;
ALTER DEFAULT PRIVILEGES FOR ROLE authnz_owner IN SCHEMA public GRANT EXECUTE ON FUNCTIONS TO authnz_user;
EOF