def median(input):
    input = sorted(input)
    n = len(input)
    mid = n // 2

    if n % 2 == 0:
        return (input[mid - 1] + input[mid]) / 2
    else:
        return input[mid]