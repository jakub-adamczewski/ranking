# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import csv


def get_data_as_table(file_name):
    file = open(file_name)
    type(file)
    csvreader = csv.reader(file)
    rows = []
    for row in csvreader:
        rows.append(row)
    return rows


def get_absolute_value(min, max, value):
    return (float(value) - float(min)) / (float(max) - float(min))


def get_points(min, max, value, is_maximising):
    if is_maximising:
        return get_absolute_value(min, max, value)
    return 1 - get_absolute_value(min, max, value)


def get_column(data, col_index):
    column = []
    for row in data:
        column.append(row[col_index])
    return column


def print_ranking(ranking):
    sorted_ranking = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
    print("Punktacja:")
    for e in sorted_ranking:
        print(e)

    places_iterator = 0
    last_points = -1
    for e in sorted_ranking:
        current_points = e[1]
        if current_points != last_points:
            places_iterator += 1
            last_points = current_points
        print("Miejsce: ", places_iterator, ": ", e[0])


def create_ranking(weghts_dict, max_or_min_dict, file_name):
    weights_sum = sum(weghts_dict.values())
    if weights_sum != 1:
        raise RuntimeError('weights sum should be equal to 1, but are equal to: ', weights_sum)
    rows = get_data_as_table(file_name)
    mins_dict = {}
    maxes_dict = {}
    for row in rows[1:]:
        row_numbers = [float(i) for i in row[1:]]
        maxes_dict[row[0]] = max(row_numbers)
        mins_dict[row[0]] = min(row_numbers)
        print("Added min/max: ", row[0], min(row_numbers), max(row_numbers))

    ranking = {}
    for car_name in rows[0][1:]:
        ranking[car_name] = 0
    for properties_row in rows[1:]:
        property_name = properties_row[0]
        property_data = [float(i) for i in properties_row[1:]]
        for i, single_car_property in enumerate(property_data):
            is_maximising = max_or_min_dict[property_name]
            p = get_points(mins_dict[property_name], maxes_dict[property_name], single_car_property, is_maximising)
            weight = weghts_dict[property_name]
            points = p * weight
            car_name = rows[0][i + 1]
            ranking[car_name] += points
    print_ranking(ranking)


if __name__ == '__main__':
    create_ranking(
        weghts_dict={
            'cena [tys zl]': 0.6,
            'moc [km]': 0.2,
            'moment obrotowy [Nm]': 0.0,
            'przyspieszenie do 100 [s]': 0,
            'pojemnosc aku [kWh]': 0,
            'zuzycie energii [kWh/100km]': 0,
            'naped na kola': 0.2
        },
        max_or_min_dict={
            'cena [tys zl]': False,
            'moc [km]': True,
            'moment obrotowy [Nm]': True,
            'przyspieszenie do 100 [s]': True,
            'pojemnosc aku [kWh]': True,
            'zuzycie energii [kWh/100km]': False,
            'naped na kola': True
        },
        file_name='data/dane_auta_elektryczne.csv'
    )
