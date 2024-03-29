from typing import List
from app.services.course_service import CourseService
from app.db.connection import LocalSession
from app.models.course import Course
from app.models.student import Student
from app.models.assignment import Assignment
from app.models.student_course import StudentCourse
from app.models.submission import Submission
from sqlalchemy import func, desc
from fastapi.exceptions import HTTPException



class CourseServiceMixin:
  """
  Additional methods for database queries
  """
  def get_student_by_id(self, student_id) -> Student:
    with LocalSession() as session:
      db_student = session.get(Student, ident=student_id)
    return db_student
    

  def get_assignment_by_id(self, assignment_id: int) -> Assignment:
    with LocalSession() as session:
      db_assignment = session.get(Assignment, assignment_id)
    return db_assignment



class CourseServiceImpl(CourseService, CourseServiceMixin):
  """
  Please implement the CourseService interface according to the requirements.
  """
  def get_course_by_id(self, course_id) -> Course:
    with LocalSession() as session:
      db_course = session.get(Course, course_id)
    return db_course
  

  def get_courses(self) -> list[Course]:
    with LocalSession() as session:
      # fetch all courses from database
      db_courses = session.query(Course).all()
    return db_courses
  

  def create_course(self, course_name) -> Course:
    with LocalSession() as session:
      # validate course name length
      if not 0< len(course_name) <= 100:
        raise HTTPException(status_code=406, detail={
          'description': 'cannot create course.',
          'message': 'course name should have less than 100 characters.'
        })
      
      # check for duplicate course name
      if session.query(Course).filter_by(course_name=course_name).first():
        raise HTTPException(status_code=409, detail={
          'description': 'cannot insert duplicate.',
          'message': f'A course with {course_name} name is available and cannot insert duplicate'
        })

      #insert course to database
      db_course = Course(course_name=course_name.lower())
      session.add(db_course)
      session.commit()
      session.refresh(db_course)
    return db_course  
  
  
  def delete_course(self, course_id) -> Course:
    with LocalSession() as session:
      # check for course existance by course_id
      if not self.get_course_by_id(course_id=course_id):
        raise HTTPException(status_code=404, detail={
          'description': 'cannot delete course.',
          'message': f'course couldn\'t be found with ID {course_id}.' 
        })

      # fetch course with course_id and return
      db_course = session.get(Course, course_id)
      session.delete(db_course)
      session.commit()
    return db_course
  
  
  def create_assignment(self, course_id, assignment_name) -> Assignment:
    with LocalSession() as session:
      # assignment name length validation
      if not 0 < len(assignment_name) <= 100: 
        raise HTTPException(status_code=406, detail={
          'description': 'cannot create assignment.',
          'message': 'assignment name should have between 0 and 100 characters.'
        })

      # Check for duplicate assignment
      if session.query(Assignment)\
      .filter_by(assignment_name=assignment_name, course_id=course_id)\
      .first():
        raise HTTPException(status_code=409, detail={
          'description': 'cannot create assignment.',
          'message': f'An assignment was found with name {assignment_name} and course ID {course_id}'
        })
        
      # Insert assignment into database
      db_assignemnt = Assignment(course_id=course_id, assignment_name=assignment_name)      
      session.add(db_assignemnt)
      session.commit()
      session.refresh(db_assignemnt)
      return db_assignemnt


  def enroll_student(self, course_id, student_id) -> StudentCourse:
    with LocalSession() as session:
      db_student_course = StudentCourse(student_id=student_id, course_id=course_id)
      # check for duplicate student and course enrollment
      if session.query(StudentCourse)\
        .filter_by(student_id=student_id, course_id=course_id)\
        .first():
        raise HTTPException(status_code=409, detail={
          'description': 'cannot enroll student.',
          'message': f'student with ID {student_id} is already enrolled in course with ID {course_id}.'
        })
      session.add(db_student_course)
      session.commit()
      session.refresh(db_student_course)
    return db_student_course


  def dropout_student(self, course_id, student_id) -> StudentCourse:
    with LocalSession() as session:
      # fetch enrolled student with student_id and course_id
      db_student_course = session.query(StudentCourse).where(
        StudentCourse.course_id==course_id,
        StudentCourse.student_id==student_id
      ).order_by(StudentCourse.student_course_id.desc()).first()

      # check if the enrolled student exists
      if not db_student_course:
        raise HTTPException(status_code=404, detail={
          'description': 'cannot dropout student.',
          'message': f'student with ID {student_id} is not enrolled in course with ID {course_id}!'
        })

      # dropout student
      session.delete(db_student_course)
      session.commit()

    return db_student_course


  def submit_assignment(self, course_id, student_id, assignment_id, grade: int):
    with LocalSession() as session:
      # check if grade is between 0 and 100
      if not 0 <= grade <= 100:
        raise HTTPException(status_code=422, detail={
          'description': 'cannot create submission',
          'message': f'grade out of range. grade should be between 0 and 100.'
        })

      # check for duplicate values in database
      if session.query(Submission)\
      .filter_by(course_id=course_id, assignment_id=assignment_id, student_id=student_id)\
      .first():
        raise HTTPException(status_code=409, detail={
          'description': 'cannot create submission.',
          'message': f'dupliacate values not allowed! record is available for course with ID {course_id}, assignment with ID {assignment_id}, and student with ID {student_id}.'
        })

      # add submission record
      db_submission = Submission(
        course_id=course_id,
        student_id=student_id,
        assignment_id=assignment_id,
        grade=grade
      )
      session.add(db_submission)
      session.commit()
      session.refresh(db_submission)
    return db_submission

  
  def get_assignment_grade_avg(self, course_id, assignment_id) -> int:
    with LocalSession() as session:
      result = session.query(func.round(func.avg(Submission.grade)))\
        .filter(Submission.course_id==course_id, Submission.assignment_id==assignment_id)\
        .scalar()
      # check if any grade exists
      if not result:
        raise HTTPException(status_code=404, detail={
          'description': 'request cannot be made',
          'message': f'could not find any grade for course with ID {course_id} and assignment with ID {assignment_id}'
        })
      return int(result)
        
  

  def get_student_grade_avg(self, course_id, student_id) -> int:
    with LocalSession() as session:
      result = session.query(func.round(func.avg(Submission.grade))).filter(Submission.course_id==course_id, Submission.student_id==student_id).scalar()
      # check if any grade exists
      if not result:
        raise HTTPException(status_code=404, detail={
          'description': 'request cannot be made',
          'message': f'could not find any grade for course with ID {course_id} and student with ID {student_id}'
        })
      return int(result)
  

  def get_top_five_students(self, course_id) -> List[int]:
    with LocalSession() as session:
        top_5 = session.query(
          Submission.student_id,
          func.avg(Submission.grade).label('average_grade')
          ).filter_by(course_id=course_id)\
          .group_by(Submission.student_id)\
          .order_by(desc('average_grade'))\
          .limit(5)\
          .all()
    
    # check if any student grade available
    if not top_5:
      raise HTTPException(status_code=404, detail={
        'description': 'request cannot be made',
        'message': f'no student grade were found for the course with ID {course_id}'
      })

    return [student_id for student_id, _ in top_5]
  
