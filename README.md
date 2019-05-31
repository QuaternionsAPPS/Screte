# SCRETE
Project for Linear algebra and Databases courses.


## Database architecture ##


**users**

name  | type |
 :------------: | :-----------: |
id       |    integer auto-incremental primary key     |
username      |    text field up to 32 symbols, can not be empty     |
password       |    text field up to 32 symbols, can not be empty     |
first_name     |    text field up to 32 symbols, can not be empty     |
last_name      |    text field up to 32 symbols, can not be empty   |
sh_key      |    text field up to 618 symbols, can not be empty     |
registration_time      |   text field in format `HH:MM:SS_DD-MM-YY`, can not be empty     |


**pictures**

name  | type |
 :------------: | :-----------: |
id       |    integer auto-incremental primary key     |
from_user_id       |    integer foreign key, references table users,  can not be empty|
to_user_id       |    integer foreign key, references table users,  can not be empty     |
had_been_read       |    boolean value, can not be empty, default - 0     |
info_from_user       |    text field up to 255 symbols     |

**contacts**

name  | type |
 :------------: | :-----------: |
1_user_id       |    integer foreign key, references table users,  can not be empty|
2_user_id       |    integer foreign key, references table users,  can not be empty     |
Combination of 1_user_id and 2_user_id can be used as primary key for this table.

**sessions**

name  | type |
 :------------: | :-----------: |
id       |    integer auto-incremental primary key     |
user_id      |    integer foreign key, references table users,  can not be empty |
start_time      |    text field in format  `HH:MM:SS_DD-MM-YY`, can not be empty     |
finish_time      |    text field in format  `HH:MM:SS_DD-MM-YY`, can not be empty     |
number_of_encoded_pictures       |    integer, can not be empty     |
number_of_decoded_pictures       |    iinteger, can not be empty     |