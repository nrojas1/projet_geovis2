-- number of entries in db
Select COUNT(*)
FROM musicians;

-- number of distinct musicians
SELECT COUNT(*) FROM (SELECT
DISTINCT name, lastname, email
FROM musicians) AS foo;

-- how many of each instrument in db
SELECT COUNT(instruments.name), instruments.name
FROM musicians
JOIN instruments ON musicians.instrument_id = instruments.id
GROUP BY instruments.name
ORDER BY instruments.name;

-- how many of each skill in db... yea naaah
SELECT COUNT(sk1.name), sk1.name, sk2.name, sk3.name, sk4.name
FROM musicians
JOIN skills AS sk1 ON musicians.skill_id1 = sk1.id
JOIN skills AS sk2 ON musicians.skill_id2 = sk2.id
JOIN skills AS sk3 ON musicians.skill_id3 = sk3.id
JOIN skills AS sk4 ON musicians.skill_id4 = sk4.id
GROUP BY sk1.name, sk2.name, sk3.name, sk4.name;
