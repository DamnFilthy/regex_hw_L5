import re
import csv


def correction_of_name(line: list):
    full_name = f'{line[0].strip()} {line[1].strip()} {line[2].strip()}'.split()

    # add spare lines
    if len(full_name) < 3:
        full_name.extend(['', '', ''])
    line[0], line[1] = map(str, full_name[:2])
    line[2] = ' '.join(full_name[2:]).strip()

    # remove unnecessary
    return line[:7]


def correction_of_phone(line: list):
    pattern = re.compile(r'([+][7]|8)?\s*-*\s*\(*\s*(\d{1,5})\s*\)*\s*-*\s*(\d{1,3})\s*-*\s*(\d{1,3})\s*-*\s*(\d{1,3})'
                         r'\s*\(?\s*[д.|доб.]*\s*(\d*)\s*\)?\s*')
    result = re.match(pattern, line[5])
    if result:
        phone = ''.join(result.groups()[1:5])
        phone = '{}({}){}-{}-{}{}'.format('+7', phone[:3], phone[3:6], phone[6:8], phone[8:],
                                          f' доб.{result.group(6)}' if result.group(6) else '')
        line[5] = phone
    return line


def smart_append(some_list: list, line: list) -> list:
    # remove duplicates and combine information
    connect = False
    for item in some_list:
        lastname = item[0] == line[0]
        firstname = item[1] == line[1]
        surname = item[2] == line[2] or not item[2] or not line[2]
        organization = item[3] == line[3] or not item[3] or not line[3]
        position = item[4] == line[4] or not item[4] or not line[4]
        phone = item[5] == line[5] or not item[5] or not line[5]
        email = item[6] == line[6] or not item[6] or not line[6]
        need_connect = lastname and firstname and surname and organization and position \
                       and phone and email
        if need_connect:
            item[2] = line[2] if line[2] else item[2]
            item[3] = line[3] if line[3] else item[3]
            item[4] = line[4] if line[4] else item[4]
            item[5] = line[5] if line[5] else item[5]
            item[6] = line[6] if line[6] else item[6]
            connect = True
    if not connect:
        some_list.append(line)
    return some_list


def revise(some_list: list):
    fixed_list = []
    for line in some_list:
        exactly = correction_of_name(line)
        exactly = correction_of_phone(exactly)
        fixed_list = smart_append(fixed_list, exactly)
    return fixed_list


if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding='utf8') as file:
        lines = csv.reader(file, delimiter=",")
        contacts_list = list(lines)

    revised_file = revise(contacts_list)

    with open("result.csv", "w", encoding='utf8', newline='') as file:
        datawriter = csv.writer(file, delimiter=',')
        datawriter.writerows(revised_file)
