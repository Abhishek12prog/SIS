START TRANSACTION;

CREATE TEMPORARY TABLE duplicate_students_to_remove AS
SELECT s.student_id AS remove_student_id,
       d.keep_student_id,
       s.username
FROM students s
JOIN (
    SELECT UPPER(TRIM(username)) AS enrollment_key, MIN(student_id) AS keep_student_id
    FROM students
    WHERE username IS NOT NULL AND TRIM(username) != ''
    GROUP BY UPPER(TRIM(username))
    HAVING COUNT(*) > 1
) d
    ON UPPER(TRIM(s.username)) = d.enrollment_key
WHERE s.student_id <> d.keep_student_id;

UPDATE academics a
JOIN duplicate_students_to_remove d ON a.student_id = d.remove_student_id
SET a.student_id = d.keep_student_id;

UPDATE exam_subjects e
JOIN duplicate_students_to_remove d ON e.student_id = d.remove_student_id
SET e.student_id = d.keep_student_id;

UPDATE feedback f
JOIN duplicate_students_to_remove d ON f.student_id = d.remove_student_id
SET f.student_id = d.keep_student_id;

UPDATE fees f
JOIN duplicate_students_to_remove d ON f.student_id = d.remove_student_id
SET f.student_id = d.keep_student_id;

UPDATE helpdesk h
JOIN duplicate_students_to_remove d ON h.student_id = d.remove_student_id
SET h.student_id = d.keep_student_id;

UPDATE faculty_chat_messages m
JOIN duplicate_students_to_remove d ON m.student_id = d.remove_student_id
SET m.student_id = d.keep_student_id;

UPDATE faculty_meeting_requests r
JOIN duplicate_students_to_remove d ON r.student_id = d.remove_student_id
SET r.student_id = d.keep_student_id;

UPDATE exam_seating_allocations a
JOIN duplicate_students_to_remove d ON a.student_id = d.remove_student_id
SET a.student_id = d.keep_student_id;

DELETE s
FROM students s
JOIN duplicate_students_to_remove d ON s.student_id = d.remove_student_id;

ALTER TABLE students
MODIFY username VARCHAR(50) NOT NULL,
ADD CONSTRAINT uq_students_username UNIQUE (username);

COMMIT;
