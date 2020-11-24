BEGIN;
CREATE TABLE IF NOT EXISTS terms (
	id	INT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
	term	TEXT,
	PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS content (
	id	INT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
	title	TEXT NOT NULL,
	path	TEXT NOT NULL,
	info	TEXT,
	text	TEXT,
	type	TEXT NOT NULL,
	quantity	INTEGER,
	PRIMARY KEY(id)
);
CREATE TABLE IF NOT EXISTS term_content (
	term_id	INT NOT NULL,
	content_id	INT NOT NULL,
	FOREIGN KEY(content_id) REFERENCES content(id),
	FOREIGN KEY(term_id) REFERENCES terms(id)
);
INSERT INTO terms (term) VALUES
 ('Henry la Fontaine'),
 ('Pacifizam'),
 ('Brisanje Juge'),
 ('Astrid Kuljanić'),
 ('Stipe Bilić'),
 ('Esperanto');
INSERT INTO content (id,title,path,info,text,type,quantity) VALUES
 ('Brisanje Juge','/slideshow/brisanje_juge','Prikazujemo prezentaciju o brisanju Juge','Prikazujemo prezentaciju o brisanju Juge.','presentation',10),
 ('Henry la Fontaine','/slideshow/henry_la_fontaine','Prikazujemo prezentaciju o Henry la Fontaine-u','Prikazujemo prezentaciju o Henry la Fontaine-u.','presentation',NULL),
 ('Pacifizam','/slideshow/pacifizam','Prikazujemo prezentaciju o pacifizmu.','Prikazujemo prezentaciju o pacifizmu.','presentation',12),
 ('Astrid Kunjarić & Spartaco Črnjarić','https://youtu.be/WLSXCfjjZps','Drenovska muzika','Slušate muziku od Astrid Kuljanić i Spartaco Črnjarića.','video',NULL),
 ('Stipe Bilić, Joseph Haydn: Keyboard Sonata No. 49 in E flat','https://youtu.be/0E1nvbEEoAo','Stipe Bilić svira Josepha Haydn-a','Stipe Bilić svira djelo koje je skladao Joseph Haydn','video',NULL),
 ('Esperanto','/slideshow/pacifizam/9.JPG','Esperanto','Međunarodni jezik koji omogućava bolje razumijevanje među narodima','image',NULL);
INSERT INTO term_content (term_id,content_id) VALUES (3,1),
 (1,2),
 (2,3),
 (4,4),
 (5,5),
 (6,6);
COMMIT;