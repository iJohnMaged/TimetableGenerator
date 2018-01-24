from CollegeSchedule import Course, Slot, Timetable
from itertools import product

# Algorithms
algo = Course("Algorithms")
algo.add_slot(1, 0, (9, 10), "Lecture")
algo.add_slot(1, 0, (7, 8), "Section")

algo.add_slot(2, 1, (7, 8), "Lecture")
algo.add_slot(2, 4, (3, 3), "Section")

algo.add_slot(3, 1, (11, 12), "Lecture")
algo.add_slot(3, 4, (1, 1), "Section")


# DB

DB = Course("Database")
DB.add_slot(1, 2, (7, 8), "Lecture")
DB.add_slot(1, 2, (11, 11), "Section")
DB.add_slot(1, 2, (12, 12), "Lab")

DB.add_slot(2, 0, (9, 10), "Lecture")
DB.add_slot(2, 1, (11, 11), "Section")
DB.add_slot(2, 0, (7, 8), "Lab")

DB.add_slot(3, 5, (3, 4), "Lecture")
DB.add_slot(3, 5, (2, 2), "Section")
DB.add_slot(3, 5, (1, 1), "Lab")

# Analog shit
analog = Course("Analog")
analog.add_slot(1, 4, (1, 2), "Lecture")
analog.add_slot(1, 5, (9, 10), "Section")
analog.add_slot(1, 4, (5, 5), "Lab")

analog.add_slot(2, 4, (5, 6), "Lecture")
analog.add_slot(2, 2, (3, 4), "Section")
analog.add_slot(2, 4, (4, 4), "Lab")

analog.add_slot(3, 4, (3, 4), "Lecture")
analog.add_slot(3, 0, (11, 12), "Section")
analog.add_slot(3, 4, (2, 2), "Lab")

# OS
OS = Course("Operating Systems")
OS.add_slot(1, 4, (3, 4), "Lecture")
OS.add_slot(1, 5, (11, 12), "Section")
OS.add_slot(1, 4, (6, 6), "Lab")


OS.add_slot(2, 4, (7, 8), "Lecture")
OS.add_slot(2, 3, (1, 2), "Section")
OS.add_slot(2, 2, (12, 12), "Lab")

OS.add_slot(3, 4, (5, 6), "Lecture")
OS.add_slot(3, 0, (9, 10), "Section")
OS.add_slot(3, 0, (7, 8), "Lab")

# Numerical
Num = Course("Numerical")

Num.add_slot(2, 5, (7, 8), "Lecture")
Num.add_slot(2, 5, (9, 10), "Section")

Num.add_slot(3, 3, (9, 10), "Lecture")
Num.add_slot(3, 3, (7, 8), "Section")

def generate_best_timetables(courses, MAX_GROUP_NUM = 3):
    """
    Generating every possible solution to the problem, Here I am Generating
    3**N possible tuples Where 3 is the maximum number of groups and N is the number of
    courses to consider.
    Each element value in the tuple correspond to a group number - 1 (0, 1, 2), and the i-th element
    in the tuple correspond to the i-th course in the list of courses.
    i.e. for i-th element in the tuple, we try to add the tuple[i]+1 group of the i-th
    course to the timetable.
    """

    total_tt = []
    best_tt = None
    COURSES_NUM = len(courses)

    for p in product(range(MAX_GROUP_NUM), repeat=COURSES_NUM):
        tt = Timetable()
        valid = True

        for i, val in enumerate(p):
            course_slots = courses[i].get_group_slots(int(val) + 1)
            valid = tt.add_course(course_slots)
            if not valid:
                break

        if valid:
            # Store all the timetables with minimum number of work days
            if not best_tt or tt.total_days() < best_tt.total_days():
                best_tt = tt
                total_tt = [best_tt]
            elif tt.total_days() == best_tt.total_days():
                total_tt.append(tt)

    return total_tt

def main():
    courses = [OS, algo, DB, Num, analog]
    total_tt = generate_best_timetables(courses)

    for tt in total_tt:
        tt.print_timetable()
        print("Working days: ", tt.total_days())
        print("================================")

main()
