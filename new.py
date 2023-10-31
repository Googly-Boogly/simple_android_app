import math
def repeatedSubstringPattern( s: str) -> bool:

    runner = 0
    while runner < len(s) - 1:
        check = s[:runner + 1]

        if runner == 0:
            check_s = check * len(s)
        else:
            check_s = check * math.floor(len(s) / (runner + 1))
        if check_s == s:
            return True
        runner += 1
    return False

print(repeatedSubstringPattern('babbabbabbabbab'))