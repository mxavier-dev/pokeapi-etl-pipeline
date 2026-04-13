-- squema.sql

CREATE TABLE pokemon (
id INT AUTO_INCREMENT PRIMARY KEY,
name varchar(50) UNIQUE,
weight INT,
height INT
);

CREATE TABLE types (
id INT AUTO_INCREMENT PRIMARY KEY,
name varchar(50) UNIQUE
);

CREATE TABLE abilities (
id INT AUTO_INCREMENT PRIMARY KEY,
name varchar(50) UNIQUE
);

CREATE TABLE pokemon_types (
pokemon_id INT, 
type_id INT,
primary key (pokemon_id, type_id)
);

CREATE TABLE pokemon_abilities (
pokemon_id INT,
ability_id INT,
PRIMARY KEY (pokemon_id, ability_id)
);

ALTER TABLE pokemon_types ADD CONSTRAINT FK_pokemon_type 
FOREIGN KEY (pokemon_id)
REFERENCES pokemon(id);

ALTER TABLE pokemon_types ADD CONSTRAINT FK_type_pokemon 
FOREIGN KEY (type_id)
REFERENCES types(id);

ALTER TABLE pokemon_abilities ADD CONSTRAINT FK_pokemon_ability 
FOREIGN KEY (pokemon_id)
REFERENCES pokemon(id);

ALTER TABLE pokemon_abilities ADD CONSTRAINT FK_ability_pokemon 
FOREIGN KEY (ability_id)
REFERENCES abilities(id);
