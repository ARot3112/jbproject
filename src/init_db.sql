CREATE TABLE roles(id SERIAL PRIMARY KEY,name VARCHAR(10) UNIQUE NOT NULL);
CREATE TABLE users (id SERIAL PRIMARY KEY,first_name VARCHAR(20),last_name VARCHAR(20),email VARCHAR(30) UNIQUE NOT NULL,password VARCHAR(20) NOT NULL,role_id INT REFERENCES roles(id) );
CREATE TABLE countries (id SERIAL PRIMARY KEY,country_name VARCHAR(25) UNIQUE NOT NULL);
CREATE TABLE vacations (id SERIAL PRIMARY KEY,country_id INT REFERENCES countries(id),vacation_description VARCHAR(60),arrival DATE,departure DATE,price INT,file_name VARCHAR(50));
CREATE TABLE likes (user_id INT REFERENCES users(id) ON DELETE CASCADE ,vacation_id INT REFERENCES vacations(id)  ON DELETE CASCADE );

INSERT INTO roles (name) VALUES
('user'),
('admin');

INSERT INTO users (first_name,last_name,email,password,role_id) VALUES
('Afek','Rot','afekrotstain11@gmail.com','12345678',2),
('James','Wade','wade15@gmail.com','87654321',1);

INSERT INTO countries (country_name) VALUES 
('Spain'),
('ISR'),
('Brazil'),
('Hungary'),
('France'),
('Argentina'),
('Ivory Coast'),
('USA'),
('Japan'),
('China'),
('Croatia');

INSERT INTO vacations (country_id,vacation_description,arrival,departure,price,file_name) VALUES
(1,'Amazing trip to Spain','2025-06-12','2025-06-20',2500,'spain_trip.jpg'),
(2,'Great adventure to ISR','2026-11-20','2026-11-25',4000,'isr_trip.jpg'),
(3,'An unforgettable journey to Brazil, including a football game','2027-10-05','2025-10-15',3000,'brazil_trip.jpg'),
(4,'Exploring the rich history and culture of Hungary','2029-07-12','2025-07-19',3500,'hungary_trip.jpg'),
(5,'A romantic escape in France, visiting iconic landmarks.','2025-09-14','2025-09-20',4200,'france_trip.jpg'),
(6,'An adventure in Argentina, with breathtaking landscapes.','2025-03-12','2025-03-20',4400,'argentina_trip.jpg'),
(7,'A vibrant trip to Ivory Coast, filled with beautiful beaches.','2026-04-13','2025-04-21',4600,'ivory_coast_trip.jpg'),
(8,'A memorable trip to the USA','2027-08-12','2025-09-12',6900,'usa_trip.jpg'),
(9,'An immersive experience in Japan, with traditional temples.','2025-02-14','2025-02-28',5700,'japan_trip.jpg'),
(10,'Exploring the ancient wonders and modern marvels of China.','2025-10-12','2025-10-29',6000,'china_trip.jpg'),
(3,'A second chance to explore Brazil’s exotic destinations.','2026-11-18','2025-11-27',5900,'brazil_2_trip.jpg'),
(11,'Discover the stunning landscapes in Croatia','2028-05-17','2025-05-24',3100,'croatia_trip.jpg');

ALTER TABLE vacations
ALTER COLUMN vacation_description TYPE TEXT;

ALTER TABLE likes ADD CONSTRAINT unique_like 
UNIQUE (user_id, vacation_id);

                         ------ ^ jb_database ^ ------





