# task_repeat.py
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

MAX_REPEAT_LIMIT = 10


def repeat_task(repeat_params, start):
    dates = []
    task_count = 0

    if repeat_params:
        start_date = datetime.strptime(str(start), "%Y-%m-%d")

        def repeat_units(repeat_params, start_date, task_count):
            temp_date = start_date
            # daily tasks
            if repeat_params["everyUnit"] == "days":
                dates.append(temp_date)
                start_date += timedelta(days=repeat_params["everyNumber"])
                task_count += 1
                return start_date, task_count
            # weekly tasks
            elif repeat_params["everyUnit"] == "weeks":
                for day in repeat_params["selectedDays"]:
                    current_date = temp_date
                    if (
                        repeat_params["repeatEnd"] == "after"
                        and task_count >= repeat_params["occurrences"]
                    ) or (
                        repeat_params["repeatEnd"] == "never"
                        and task_count >= MAX_REPEAT_LIMIT
                    ):
                        break
                    days_to_add = ((day - 1) - temp_date.weekday() + 7) % 7
                    current_date += timedelta(days=days_to_add)
                    if current_date >= start_date:
                        dates.append(current_date)
                        task_count += 1

                start_date += timedelta(days=7 * repeat_params["everyNumber"])
                return start_date, task_count
            # monthly tasks
            elif repeat_params["everyUnit"] == "months":
                dates.append(temp_date)
                start_date += relativedelta(months=repeat_params["everyNumber"])
                task_count += 1
                return start_date, task_count
            # yearly tasks
            elif repeat_params["everyUnit"] == "years":
                dates.append(temp_date)
                start_date += relativedelta(years=repeat_params["everyNumber"])
                task_count += 1
                return start_date, task_count

        # loops for repeating tasks
        if repeat_params["repeatEnd"] == "after":
            for _ in range(repeat_params["occurrences"]):
                start_date, task_count = repeat_units(
                    repeat_params, start_date, task_count
                )

        elif repeat_params["repeatEnd"] == "on":
            end_date = datetime.strptime(repeat_params["endDate"], "%Y-%m-%d")
            while start_date <= end_date:
                start_date, task_count = repeat_units(
                    repeat_params, start_date, task_count
                )

        elif repeat_params["repeatEnd"] == "never":
            for _ in range(MAX_REPEAT_LIMIT):
                start_date, task_count = repeat_units(
                    repeat_params, start_date, task_count
                )
    return dates
