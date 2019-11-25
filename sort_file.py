from ast import literal_eval


def extract_salary(json_data):
    try:
        return int(json_data['salary_checker'])
    except KeyError:
        return 0


final_data = []
with open("data.json", "r") as fle:
    for f in fle.readlines():
        f = f.strip()[:-1]
        final_data += literal_eval(f)

final_data.sort(key=extract_salary, reverse=True)

with open("sorted_data.json", "w") as fle:
    fle.write("{}".format(final_data))
