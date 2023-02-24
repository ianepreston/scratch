eg_input = "pbokrpjejkuhxlqnwasfgtycdv"
no_dups = "asdfgh"
doubles = "aasdfh"
triples = "aaasdghk"
both = "aaasskljh"

all_inputs = [eg_input, no_dups, doubles, triples, both]

def char_counter(input_string):
    doubles = 0
    triples = 0
    for char in input_string:
        if input_string.count(char) == 2:
            doubles = 1
        elif input_string.count(char) == 3:
            triples = 1
    return doubles, triples

sum_doubles = 0
sum_triples = 0
with open("input.txt", "r") as christmas_file:
    for line in christmas_file.readlines():
        dubs, trips = char_counter(line)
        sum_doubles += dubs
        sum_triples += trips

solution = sum_doubles * sum_triples
print(solution)