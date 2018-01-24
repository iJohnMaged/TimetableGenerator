from CollegeSchedule import Course, Slot, Timetable
from itertools import product


# Example Data

# Algorithms
algo = Course("Algorithms")
algo.add_slot(1, 0, (1, 2), "Lecture")
algo.add_slot(1, 0, (3, 4), "Section")
algo.add_slot(1, 1, (3, 4), "Lab")

algo.add_slot(2, 0, (1, 2), "Lecture")
algo.add_slot(2, 2, (1, 2), "Section")
algo.add_slot(2, 3, (1, 2), "Lab")

# OS
os = Course("Operating Systems")
os.add_slot(1, 0, (5, 6), "Lecture")
os.add_slot(1, 0, (7, 8), "Section")
os.add_slot(1, 1, (5, 6), "Lab")

os.add_slot(2, 0, (1, 2), "Lecture")
os.add_slot(2, 4, (7, 8), "Section")
os.add_slot(2, 5, (5, 6), "Lab")

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
    courses = [os, algo]
    total_tt = generate_best_timetables(courses)

    for tt in total_tt:
        tt.print_timetable()
        print("Working days: ", tt.total_days())
        print("================================")

main()
