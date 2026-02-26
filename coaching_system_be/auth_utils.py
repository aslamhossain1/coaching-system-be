from students.models import Guardian, Student
from teachers.models import Teacher


def get_teacher(user):
    if not user or not user.is_authenticated:
        return None
    return Teacher.objects.filter(user=user).first()


def get_student(user):
    if not user or not user.is_authenticated:
        return None
    return Student.objects.filter(user=user).first()


def get_guardian(user):
    if not user or not user.is_authenticated:
        return None
    return Guardian.objects.filter(user=user).first()


def get_user_role(user):
    if get_teacher(user):
        return "teacher"
    if get_student(user):
        return "student"
    if get_guardian(user):
        return "guardian"
    return None


def can_access_student(user, student):
    teacher = get_teacher(user)
    if teacher:
        return teacher.batch_id is not None and teacher.batch_id == student.batch_id

    current_student = get_student(user)
    if current_student:
        return current_student.id == student.id

    guardian = get_guardian(user)
    if guardian:
        return student.guardian_id == guardian.id
    return False

