import csv


def save_dict_2_csv(filename: str, fieldnames: list[str], data: list[dict]):
    with open(filename, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def read_from_csv(filename: str, fieldnames: list[str], res_frame: list[str]) -> list[dict]:
    results = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f=f, fieldnames=fieldnames)
        res_all_flag = True
        header_flag = True

        if not res_frame is None or len(res_frame) > 0:
            res_all_flag = False

        for row in reader:
            if not header_flag:
                if not res_all_flag:
                    result = {}
                    for key in res_frame:
                        result[key] = row[key]
                    results.append(result)
            else:
                header_flag = False

    return results
