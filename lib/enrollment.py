from datetime import datetime

class Student:
    def __init__(self, name):
        self.name = name
        self._enrollments = []
        self._grades = {}  # Dictionary to store enrollment and grade pairs

    def enroll(self, course):
        if isinstance(course, Course):
            enrollment = Enrollment(self, course)
            self._enrollments.append(enrollment)
            course.add_enrollment(enrollment)
        else:
            raise TypeError("course must be an instance of Course")

    def add_grade(self, enrollment, grade):
        if enrollment in self._enrollments:
            self._grades[enrollment] = grade
        else:
            raise ValueError("Enrollment does not exist for this student")

    def get_enrollments(self):
        return self._enrollments.copy()

    def course_count(self):
        return len(self._enrollments)

    def aggregate_average_grade(self):
        if not self._grades:
            return 0  # Return 0 if there are no grades
        total_grades = sum(self._grades.values())
        num_courses = len(self._grades)
        return total_grades / num_courses


class Course:
    def __init__(self, title):
        self.title = title
        self._enrollments = []

    def add_enrollment(self, enrollment):
        if isinstance(enrollment, Enrollment):
            self._enrollments.append(enrollment)
        else:
            raise TypeError("enrollment must be an instance of Enrollment")

    def get_enrollments(self):
        return self._enrollments.copy()

    def student_count(self):
        return len(self._enrollments)


class Enrollment:
    all = []

    def __init__(self, student, course):
        if isinstance(student, Student) and isinstance(course, Course):
            self.student = student
            self.course = course
            self._enrollment_date = datetime.now()
            type(self).all.append(self)
        else:
            raise TypeError("Invalid types for student and/or course")

    def get_enrollment_date(self):
        return self._enrollment_date

    @classmethod
    def aggregate_enrollments_per_day(cls):
        enrollment_count = {}
        for enrollment in cls.all:
            date = enrollment.get_enrollment_date().date()
            enrollment_count[date] = enrollment_count.get(date, 0) + 1
        return enrollment_count

# Example Usage
if __name__ == "__main__":
    # Create Students
    alice = Student("Alice")
    bob = Student("Bob")

    # Create Courses
    math = Course("Math")
    science = Course("Science")

    # Enroll Students
    alice.enroll(math)
    alice.enroll(science)
    bob.enroll(math)

    # Add Grades
    for enrollment in alice.get_enrollments():
        alice.add_grade(enrollment, 90)

    # Calculate Aggregates
    print(f"Alice's course count: {alice.course_count()}")
    print(f"Alice's average grade: {alice.aggregate_average_grade()}")
    print(f"Math student count: {math.student_count()}")
    print(f"Enrollments per day: {Enrollment.aggregate_enrollments_per_day()}")
