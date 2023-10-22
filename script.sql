CREATE DATABASE undolog_db;

CREATE TABLE t (
    id integer NOT NULL,
    A integer NOT NULL,
    B integer NOT NULL,
    CONSTRAINT pk_t PRIMARY KEY (id)
);

INSERT INTO t (id, A, B) VALUES (1,2,3);