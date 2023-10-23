from tabulate import tabulate
from csv import writer, reader

# List of team members
team_members = ["Hadar", "Matasas", "Ofer", "Nissan", "Or", "Michal", "Eylon", "Pavel", "Ido"]
hard_shifts_count = {key: 0 for key in team_members}
on_call_count = {key: 0 for key in team_members}
hard_shifts_hours = [("01:00", "04:00"), ("04:00", "07:00")]
shifts_space = {key: 0 for key in team_members}

# Define the days off
days_off = [
    [("Sunday", ("22:00", "01:00")), ("Tuesday", ("22:00", "01:00")), ["Ofer", "Nissan"]],
    [("Tuesday", ("22:00", "01:00")), ("Thursday", ("22:00", "01:00")), ["Or", "Michal"]],
    [("Thursday", ("22:00", "01:00")), ("Saturday", ("22:00", "01:00")), ["Matasas", "Pavel"]]
]
team_members_on_day_off = []
on_call = []

# Define the shifts (24 hours divided into 3-hour shifts)
shifts = [(f"{hour:02}:00", f"{(hour + 3) % 24:02}:00") for hour in range(1, 24, 3)]

# Create a schedule for 7 days
days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
schedule = {day: {} for day in days_of_week}


def remove_team_members_if_day_off_is_on(day, shift):
    '''
    Check if the current shift is a start of a day off. If so - add the team members to the team_members_on_day_off list and remove them from the team_members list
    '''

    for day_off in days_off:
        if (day, shift) == day_off[0]:
            for member in day_off[2]:
                if member in team_members:
                    team_members_on_day_off.append(member)
                    shifts_space.pop(member)
                    hard_shifts_count.pop(member)
                    team_members.remove(member)


def add_team_members_if_day_off_is_over(day, shift):
    '''
    Check if the current shift is an end of a day off. If so - add the team members back to the team_members list and remove them from the team_members_on_day_off list
    '''

    global team_members_on_day_off

    for day_off in days_off:
        if (day, shift) == day_off[1]:
            team_members.reverse()

            for member in day_off[2]:
                if member not in team_members:
                    team_members.append(member)
                    shifts_space[member] = 0
                    hard_shifts_count[member] = 0

            team_members.reverse()
            team_members_on_day_off = []


def set_shift_to_relevant_team_member(day, shift):
    '''
    Set the current shift to the team member with the maximum amount of shifts space, as long as they didn't have 2 hard shifts already earlier this week
    '''
    if shift in hard_shifts_hours:
        member_index = 0
        while True:
            if hard_shifts_count[team_members[member_index]] == 2:
                member_index += 1
            else:
                break

        hard_shifts_count[team_members[member_index]] += 1
        schedule[day][shift] = team_members.pop(member_index)
    else:
        schedule[day][shift] = team_members.pop(0)


def update_shift_space(day, shift):
    '''
    Update shifts space for each team member
    '''

    shifts_space[schedule[day][shift]] = -1
    for member in team_members:
        shifts_space[member] += 1


def set_on_call_for_team_member(shift):
    '''
    Set a team member to be on call according to his shift space and past on-call duties
    '''

    if shift == ("22:00", "01:00"):
        member_index = 0
        while True:
            if on_call_count[team_members[member_index]] == 1:
                member_index += 1
            else:
                break

        on_call_count[team_members[member_index]] += 1
        on_call.append(team_members[member_index])
        shifts_space[team_members[member_index]] = -4


def print_shifts_schedule():
    table = [["Shift"] + days_of_week]

    for shift in shifts:
        table.append([f"{shift[0]} - {shift[1]}"] + [schedule[day][shift] for day in days_of_week])

    table.append([f"On Call"] + [member for member in on_call])

    print(tabulate(table, headers="firstrow", tablefmt="pretty"))


def build_shifts_schedule():
    for day in days_of_week:
        for shift in shifts:

            remove_team_members_if_day_off_is_on(day, shift)
            add_team_members_if_day_off_is_over(day, shift)

            team_members.sort(key=lambda member: shifts_space[member], reverse=True)

            set_shift_to_relevant_team_member(day, shift)

            update_shift_space(day, shift)

            # Add the team member back to the team_members list
            team_members.append(schedule[day][shift])

            set_on_call_for_team_member(shift)


def initialize_shift_according_to_old_schedule_hard_coded():
    '''
    Initialize the shifts schedule according to old schedule, including on-call duties, shifts space and hard shifts count for each team member since their last day off
    '''

    global on_call, hard_shifts_count, shifts_space

    # Initialize on-call duties
    # For instance: on_call_count["Matasas"] = 1

    # Initialize shifts space
    # For instance:
    #   shifts_space["Matasas"] = 2
    #   shifts_space["Ofer"] = 3

    # Initialize hard shifts count
    # For instance:
    #   hard_shifts_count["Matasas"] = 2
    #   hard_shift_count["Ofer"] = 1

    pass
    

def write_to_csv_file():
    # write the scehdule to a csv file
    
    with open("schedule.csv", "w", newline="") as file:
        csv_writer = writer(file)
        csv_writer.writerow(["Shift"] + days_of_week)

        for shift in shifts:
            csv_writer.writerow([f"{shift[0]} - {shift[1]}"] + [schedule[day][shift] for day in days_of_week])

        csv_writer.writerow([f"On Call"] + [member for member in on_call])


def load_old_schedule_fron_csv_file_and_initialize_shift_according_to_old_schedule():
    global on_call, schedule

    with open("schedule.csv", "r", newline="") as file:
        csv_reader = reader(file)

        for row in csv_reader:
            if row[0] == "Shift":
                continue

            if row[0] == "On Call":
                on_call = row[1:]
                continue

            for day in days_of_week:
                schedule[day][tuple(row[0].split(" - "))] = row[days_of_week.index(day) + 1]

    # initialize_shift_according_to_old_schedule()
        

if __name__ == "__main__":
    load_old_schedule_fron_csv_file_and_initialize_shift_according_to_old_schedule()
    initialize_shift_according_to_old_schedule_hard_coded()
    build_shifts_schedule()
    print_shifts_schedule()
    write_to_csv_file()
