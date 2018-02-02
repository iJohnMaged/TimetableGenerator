from college_schedule import Course, Slot, Timetable, Workdays, ScheduleConflictError, Period
from itertools import product


def generate_best_timetables(courses, max_group_num=3):
    """
    Generating every possible solution to the problem, Here I am Generating
    3**N possible tuples Where 3 is the maximum number of groups and N is the
    number of courses to consider. Each element value in the tuple correspond
    to a group number-1 (0, 1, 2), and the i-th element in the tuple correspond
    to the i-th course in the list of courses. i.e. for i-th element in the
    tuple, we try to add the tuple[i]+1 group of the i-th course to the
    timetable.
    """

    best_timetables = []
    courses_num = len(courses)
    current_timetable = Timetable()

    for course_set in product(range(max_group_num), repeat=courses_num):
        try:
            current_timetable = Timetable()

            for course, pre_group in zip(courses, course_set):
                current_timetable.add_course(course, pre_group+1)

            if current_timetable.total_work_days < best_timetables[0].total_work_days:
                best_timetables = [current_timetable]
            elif current_timetable.total_work_days == best_timetables[0].total_work_days:
                best_timetables.append(current_timetable)

        except ScheduleConflictError:
            pass

        except IndexError:
            best_timetables = [current_timetable]

    return best_timetables


def main():

    # Example Data

    finance = Course.create('Finance', [
        Slot(1, Workdays.THURSDAY, Period(9, 10), 'Lecture'),
        Slot(2, Workdays.THURSDAY, Period(11, 12), 'Lecture'),
    ])

    accounting = Course.create('Accounting', [
        Slot(1, Workdays.TUESDAY, Period(11, 12), 'Lecture', 'Haybat'),
        Slot(2, Workdays.THURSDAY, Period(11, 12), 'Lecture', 'Haybat'),
        Slot(3, Workdays.THURSDAY, Period(9, 10), 'Lecture', 'Haybat'),
    ])

    artificial_intelligence = Course.create('Artificial Intelligence', [
        Slot(1, Workdays.SUNDAY, Period(7, 8), 'Lecture', 'Amr ElMasry'),
        Slot(1, Workdays.SUNDAY, Period(11, 12), 'Tutorial'),
    ])

    embedded_systems = Course.create('Embedded Systems', [
        Slot(1, Workdays.SATURDAY, Period(1, 2), 'Lecture', 'Hossam Eldin'),
        Slot(1, Workdays.SATURDAY, Period(5, 5), 'Lab'),
        Slot(2, Workdays.SATURDAY, Period(3, 4), 'Lecture', 'Hossam Eldin'),
        Slot(2, Workdays.SATURDAY, Period(7, 7), 'Lab'),
        Slot(3, Workdays.MONDAY, Period(1, 2), 'Lecture', 'Hossam Eldin'),
        Slot(3, Workdays.MONDAY, Period(7, 7), 'Lab'),

    ])

    computer_networks = Course.create('Computer Networks', [
        Slot(1, Workdays.SATURDAY, Period(6, 6), 'Tutorial'),
        Slot(1, Workdays.MONDAY, Period(5, 6), 'Lecture', 'Ahmed Elsayed'),
        Slot(1, Workdays.WEDNESDAY, Period(3, 3), 'Lab'),
        Slot(2, Workdays.SATURDAY, Period(8, 8), 'Tutorial'),
        Slot(2, Workdays.TUESDAY, Period(3, 4), 'Lecture', 'Ahmed Elsayed'),
        Slot(2, Workdays.THURSDAY, Period(10, 10), 'Lab'),
        Slot(3, Workdays.SUNDAY, Period(3, 4), 'Tutorial'),
        Slot(3, Workdays.THURSDAY, Period(5, 6), 'Lecture', 'Ahmed Elsayed'),
        Slot(3, Workdays.WEDNESDAY, Period(6, 6), 'Lab'),

    ])

    digital_communications = Course.create('Digital Comm', [
        Slot(1, Workdays.MONDAY, Period(4, 3), 'Tutorial'),
        Slot(1, Workdays.WEDNESDAY, Period(1, 2), 'Lecture', 'Said Elkhamy'),
        Slot(1, Workdays.WEDNESDAY, Period(4, 4), 'Lab'),
        Slot(2, Workdays.TUESDAY, Period(1, 2), 'Tutorial'),
        Slot(2, Workdays.THURSDAY, Period(7, 8), 'Lecture', 'Rezk'),
        Slot(2, Workdays.THURSDAY, Period(9, 9), 'Lab'),
        Slot(3, Workdays.WEDNESDAY, Period(1, 2), 'Tutorial'),
        Slot(3, Workdays.WEDNESDAY, Period(3, 4), 'Lecture', 'Said Elkhamy'),
        Slot(3, Workdays.WEDNESDAY, Period(5, 5), 'Lab'),
    ])

    switching_theory = Course.create('Switching Theory', [
        Slot(1, Workdays.TUESDAY, Period(5, 5), 'Tutorial'),
        Slot(1, Workdays.TUESDAY, Period(7, 8), 'Lecture', 'Ahmed Younes'),
    ])

    courses = [computer_networks, switching_theory, embedded_systems, accounting,
               digital_communications, artificial_intelligence, ]

    total_timetables = generate_best_timetables(courses)

    for timetable in total_timetables:
        # For small screens, uncomment the below code.
        # timetable.print_timetable()
        timetable.print_table()
        print("Working days: ", timetable.total_work_days)
        print("\n================================\n")


main()
