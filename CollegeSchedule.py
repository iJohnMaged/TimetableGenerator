from collections import defaultdict

workdays = ('Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wedensday', 'Thrusday')


class Course():

    """
    This class contains infomation about a college course such as course
    name and in which group it occurs in.
    Each course consists of a lecture and a section at least, some courses
    has extra slot for a lab.
    """

    def __init__(self, name):

        self.name = name
        self.occurances = defaultdict(list)

    def add_slot(self, group, day, periods, type_):
        S = Slot(self, group, day, periods, type_)
        self.occurances[group].append(S)

    def get_group_slots(self, group):
        if group in self.occurances:
            return self.occurances[group]
        # In the rare case where a course is only present in 2 groups only
        return None

    def __str__(self):

        result = ""
        for group, slots in self.occurances.items():
            result += "Group " + str(group) + ":\n"
            for slot in slots:
                result += slot.get_type() + "\n"
                result += "Day: " + \
                    str(slot.day) + " Group: " + str(slot.group) + \
                    " Periods: " + str(slot.periods) + "\n"

        return result


class Slot():

    """
    This class represents a slot in a timetable (part of a course), including the
    type of that part (i.e. lecture, section or lab) along with
    the periods in which that part takes place (We've 12 periods per day, each slot
    can be between 1 to 3 periods),
    Day in which that part occurs,
    group number,
    and course name.
    """

    def __init__(self, course, group, day, periods, type_):
        self.course = course.name
        self.group = group
        self.day = day
        self.periods = periods
        self.type = type_

    def get_type(self):
        return self.type

    def __str__(self):
        result = "Course: " + self.course + " Group " + \
            str(self.group) + " " + str(self.type) + \
            " Periods " + str(self.periods)
        return result

    def __repr__(self):
        return self.__str__()


class Timetable:
    """
    A very simple Timetable representation, Has a dictionary with a
    key being the day number and the value is a list of slots
    that are part of the Timetable.
    """

    def __init__(self):
        self.work_days = defaultdict(list)

    def add_course(self, course_slots):
        """
        Tries to add a whole course (Lecture, section and lab) into the timetable.
        Returns boolean indicating if adding was successful.
        """

        if not course_slots:
            return False

        for slot in course_slots:
            can_add = self.check_slot(slot)
            if not can_add:
                return False
            self.work_days[slot.day].append(slot)

        return True

    def check_slot(self, slot):
        """
        Checks if a slot can be added into the Timetable
        by checking if the slot periods intersect with any other slot
        in the same day.
        """
        day = slot.day

        if not day in self.work_days:
            return True

        for t_slot in self.work_days[day]:
            t_time = t_slot.periods
            time = slot.periods
            new_time = (max(t_time[0], time[0]), min(t_time[1], time[1]))

            if new_time[0] <= new_time[1]:
                return False

        return True

    def print_timetable(self):
        """
        Print the timetable in a sorted way.
        First sorted by days, and inside each day sorted by periods.
        """
        days_list = sorted(self.work_days)
        for day in days_list:
            print(workdays[day])
            self.work_days[day].sort(key=lambda x: x.periods[0])
            print(*self.work_days[day], sep="\n")


    def total_days(self):
        return len(self.work_days)
