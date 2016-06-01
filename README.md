read me!

tables in monica.db:


switch_map
CREATE TABLE switch_map(switch_id int, switch_name string, status int, time TIMESTAMP);

power_usage
CREATE TABLE power_usage(date TIMESTAMP, switch_id int, power int);

user_map
CREATE TABLE user_map(user_id int, switch_id int, u_name string);