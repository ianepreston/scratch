string_1 = "123456"
string_2 = "113456"
string_3 = "098766"

def compare_strings(str1, str2):
    if len(str1) != len(str2):
        return False
    diffs = 0
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            diffs += 1
        if diffs >= 2:
            return False
    if diffs == 0:
        return False
    else:
        return str1, str2

def find_matches():
    with open("input.txt", "r") as christmas_file:
        christmas_lines_list = [line for line in christmas_file.readlines()]
    for i in range(len(christmas_lines_list)):
        for j in range(i+1, len(christmas_lines_list)):
            if compare_strings(christmas_lines_list[i], christmas_lines_list[j]):
                return(christmas_lines_list[i], christmas_lines_list[j])

def shared_characters(str1, str2):
    shared = []
    for i in range(len(str1)):
        if str1[i] == str2[i]:
            shared.append(str1[i])
    return shared

def main():
    match1, match2 = find_matches()
    return "".join(shared_characters(match1, match2))

print(main())
