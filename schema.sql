create table users(
    email text,
    password text,
    token text,
    firstname text,
    familyname text,
    gender text,
    city text,
    country text,
    primary key(email)
);
create table messages(
    id integer,
    user_id text,
    writer_id text,
    content text,
    FOREIGN KEY (user_id) REFERENCES users(email),
    FOREIGN KEY (writer_id) REFERENCES users(email),
    primary key(id)
);
