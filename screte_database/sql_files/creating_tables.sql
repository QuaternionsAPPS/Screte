use sql7291282; 

create table users (id int not null auto_increment,
username varchar(32) not null,
password varchar(32) not null,
first_name varchar(32) not null,
last_name varchar(32) not null,
registration_time varchar(17) not null,
sh_key varchar(618) not null,
primary key(id));

create table pictures (id int not null auto_increment,
from_user_id int not null,
to_user_id int not null,
url_address varchar(255) not null,
had_been_read bit not null,
info_from_user varchar(255),
primary key(id),
foreign key(from_user_id) references users(id),
foreign key(to_user_id) references users(id));

create table contacts (1_user_id int not null,
2_user_id int not null,
primary key(1_user_id, 2_user_id),
foreign key(1_user_id) references users(id),
foreign key(2_user_id) references users(id));

create table sessions (id int not null auto_increment,
user_id int not null,
start_time varchar(17) not null,
finish_time varchar(17) not null,
number_of_encoded_pictures int not null,
number_of_decoded_pictures int not null,
primary key(id),
foreign key(user_id) references users(id));