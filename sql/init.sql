CREATE TABLE profile (
    id SERIAL PRIMARY KEY,
    job VARCHAR(150),
    company VARCHAR(150),
    ssn VARCHAR(250),
    residence VARCHAR(150),
    current_location jsonb,
    blood_group VARCHAR(150)    
);

CREATE ROLE user1 WITH LOGIN SUPERUSER CREATEDB CREATEROLE INHERIT NOREPLICATION CONNECTION LIMIT -1 PASSWORD '1234'