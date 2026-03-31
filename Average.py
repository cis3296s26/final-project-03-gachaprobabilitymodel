def Average(input):

    counter = 0
    total = 0

    while counter < len(input):
        total += input[counter]
        counter += 1
    
    return total/counter