def txt_to_lst(completion):
    lst = []
    for line in completion.strip().splitlines():
        words = line.split()
        lst.append(tuple(words))
    return lst

