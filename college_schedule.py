from collections import defaultdict, namedtuple
from enum import IntEnum
from terminaltables import SingleTable


def break_msg(msg):
    if ' ' in msg:
        return msg.split(' ')

    length = len(msg)
    return msg[:length//2], msg[length//2:]


class Workdays(IntEnum):
    SATURDAY = 0
    SUNDAY = 1
    MONDAY = 2
    TUESDAY = 3
    WEDNESDAY = 4
    THURSDAY = 5


class ScheduleConflictError(Exception):
    pass


Period = namedtuple('Period', ["start", "end"])

PERIOD_TO_TIME = {
    1: '8:30',
    2: '10:00',
    3: '10:10',
    4: '11:40',
    5: '11:50',
    6: '1:20',
    7: '1:40',
    8: '3:10',
    9: '3:20',
    10: '4:50',
    11: '5:00',
    12: '6:30'
}


class Slot(namedtuple('Slot', ['group', 'day', 'period', 's_type', 'instructor'])):
    __slots__ = ()

    def overlaps(self, other):
        p = Period(max(self.period.start, other.period.start),
                   min(self.period.end, other.period.end))
        return p.start <= p.end

    def __str__(self):
        return f'{self.s_type} Group: {self.group} Starts: {PERIOD_TO_TIME[self.period.start]}' \
               f' Ends: {PERIOD_TO_TIME[self.period.end]} {"Instructor: " + self.instructor if self.instructor else ""}'

    def __lt__(self, other):
        return self.period < other.period


Slot.__new__.__defaults__ = (None,)


class Course(namedtuple('Course', 'name occurrences')):
    __slots__ = ()

    @classmethod
    def create(cls, name, slots):
        occurrences = defaultdict(list)
        for slot in slots:
            occurrences[slot.group].append(slot)
        return cls(name, occurrences)

    def get_course_slots(self, group_number):
        return self.occurrences[group_number]


class Timetable:
    """
    A very simple Timetable representation, Has a dictionary with a
    key being the day number and the value is a list of slots
    that are part of the Timetable.
    """
    __slots__ = ['work_days']

    def __init__(self):
        self.work_days = defaultdict(list)

    def add_course(self, course, group_number):
        """
        Tries to add a whole course (Lecture, section and lab) into the timetable.
        Returns boolean indicating if adding was successful.
        """
        course_slots = course.get_course_slots(group_number)

        if not course_slots:
            raise ScheduleConflictError

        for slot in course_slots:
            if not self._available_slot(slot):
                raise ScheduleConflictError

        self._add_valid_course(course.name, course_slots)

    def _add_valid_course(self, cname, slots):
        for slot in slots:
            self.work_days[slot.day].append((cname, slot))

    def _available_slot(self, slot):
        """
        Checks if a slot can be added into the Timetable by checking if the slot
        periods intersect with any other slot in the same day.
        """
        return not any(slot.overlaps(other_slot[1]) for other_slot in self.work_days[slot.day])

    def print_timetable(self):
        """
        Print the timetable to the console in a sorted way. First sorted by
        days, and then by periods.
        """
        for day in sorted(self.work_days):
            print(day.name)
            print()
            for cname, slot in sorted(self.work_days[day], key=lambda x: x[1]):
                print(cname, slot)
            print()

    @property
    def total_work_days(self):
        return len(self.work_days)

    def print_table(self):
        """
        Uses the `terminaltables` module to pretty-print the timetable. Doesn't
        work Properly on smaller screens, use `print_timetable` function instead.
        """
        rows = []
        headers = [""] + [str(i) for i in range(1, 13)]
        # Used a copy here because work_days is a defaultdict
        work_days_copy = self.work_days.copy()

        for day in Workdays:
            row = [day.name] + [""] * 12
            for cname, slot in work_days_copy[day]:
                msg = f'G{slot.group} {cname} {slot.s_type}'
                msg = '\n'.join(msg.split(' '))
                row[slot.period.start] = f'{msg}'
                if slot.period.start != slot.period.end:
                    row[slot.period.end] = f'Period\n{slot.period.start}\nContinued'
                if slot.instructor:
                    row[slot.period.start] += f'\n{slot.instructor}'

            rows.append(row)
        table_data = [headers] + rows
        table_instance = SingleTable(table_data, "Timetable")
        table_instance.inner_row_border = True
        print(table_instance.table)
