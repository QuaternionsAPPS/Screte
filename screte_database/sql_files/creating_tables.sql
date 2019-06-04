create table users (id bigserial primary key,
username varchar(32) not null,
password varchar(32) not null,
first_name varchar(32) not null,
last_name varchar(32) not null,
registration_time varchar(17) not null,
ip_address varchar(15),
sh_key varchar(618) not null);

create table pictures (id bigserial primary key,
from_user_id int not null,
to_user_id int not null,
had_been_read boolean not null,
info_from_user varchar(255),
foreign key(from_user_id) references users(id),
foreign key(to_user_id) references users(id));

create table contacts (user1_id int not null,
user2_id int not null,
primary key(user1_id, user2_id),
foreign key(user1_id) references users(id),
foreign key(user2_id) references users(id));

create table sessions (id bigserial primary key,
user_id int not null,
start_time varchar(17) not null,
finish_time varchar(17) not null,
number_of_encoded_pictures int not null,
number_of_decoded_pictures int not null,
foreign key(user_id) references users(id));