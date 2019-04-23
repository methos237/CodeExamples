create table students
	(id				numeric(3), 
	 name			varchar(20) not null, 
	 dept			varchar(20), 
	 primary key (id)
	);
	
create table courses
	(cNo			numeric(3), 
	 title			varchar(50), 
	 credits		numeric(1,0) check (credits > 0),
	 primary key (cNo)
	);
	
create table transcripts
	(id				numeric(3),
	 cNo			numeric(3),
	 grade			char(1),
	 foreign key (id) references students(id)
		on delete set null on update cascade,
	 foreign key (cNo) references courses(cNo)
		on update cascade
	);
	

INSERT INTO `students` (`id`, `name`, `dept`) 
VALUES ('111', 'Amy', 'CS'),
	('222', 'Bob', 'Math'), 
	('333', 'Cindy', 'CS'), 
	('444', 'David', 'CS');


INSERT INTO `courses` (`cNo`, `title`, `credits`) 
VALUES ('529', 'AI', '4'), 
	('555', 'Alg', '5'), 
	('562', 'OS', '3');


INSERT INTO `transcripts` (`id`, `cNo`, `grade`) 
VALUES ('111', '529', 'B'), 
	('111', '555', 'A'), 
	('222', '555', 'A'), 
	('333', '529', 'B'), 
	('333', '555', 'C'), 
	('333', '562', 'A'), 
	('444', '562', 'C');
	
	
Q1.
SELECT id, name FROM students WHERE department = 'CS';

Q2.
SELECT distinct
  courses.cNo,
  courses.title
FROM
  courses
  INNER JOIN transcripts ON transcripts.cNo = courses.cNo,
  students
WHERE
  (students.name = 'Cindy' AND
  transcripts.grade = 'A') OR
  (transcripts.grade = 'B');
  
Q3.
SELECT
  students.name,
  Sum(DISTINCT courses.credits) AS total_credits,
  transcripts.id
FROM
  courses
  INNER JOIN transcripts ON transcripts.cNo = courses.cNo
  INNER JOIN students ON transcripts.id = students.id
WHERE
  students.dept = 'CS'
GROUP BY
  students.name,
  transcripts.id;