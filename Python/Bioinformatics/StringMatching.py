# Assignment 3 - CSC-571 - Dr. Pranshanti Manda - UNCG
#
# Sring matching using Z algorithm and KMP
#
# @author: James Knox Polk <jkpolk@uncg.edu>
# Last Revision: 2/28/2019


def zalg(input_string, patt):
    # concatenate the pattern to the string
    pst = patt + '$' + input_string
    pst_len = len(pst)
    # create the z-array
    z_arr = [0] * pst_len

    # set the initial interval values to 0 and set z_arr[0] to x
    l_intval, r_intval, z_arr[0] = 0, 0, "x"

    # populate the z-array in O(n) time
    for x in range(1, pst_len):
        # left interval < x < right interval
        if x < r_intval:
            k = x - l_intval
            if z_arr[k] < r_intval - x:
                z_arr[x] = z_arr[k]
                continue
            l_intval = x
        else:
            # naive solution
            l_intval = r_intval = x
        while r_intval < pst_len and (pst[r_intval - l_intval] == pst[r_intval]):
            r_intval += 1
        z_arr[x] = r_intval - l_intval
    print("Z-Array:", z_arr)

    # See if the pattern is found in the string
    match_index = []
    for x in range(pst_len):
        # any index that has a value = to the length of the pattern is the start of a full match
        if z_arr[x] == len(patt):
            match_index.append(x - len(patt) - 1)

    if len(match_index) != 0:
        print("Pattern found in string: Yes")
        # start index 0 at the beginning of the original string
        print(patt, "found at index ", match_index)
    else:
        print("Pattern found in string: No")

    return


def kmp(input_string, pattern):

    # Create the prefix table
    p_table = [0] * len(pattern)
    prev_ps = 0  # length of the previous longest prefix suffix

    # Loop over the pattern and calculate the prefix table
    # The value for index 0 is always 0, so we start at 1
    p_table[0] = 0
    i = 1
    while i < len(pattern):
        # if there is a prefix-suffix match, increment length
        if pattern[i] == pattern[prev_ps]:
            prev_ps += 1
            p_table[i] = prev_ps
            i += 1
        else:
            # In case of palindrome we don't increment the loop.
            if prev_ps != 0:
                prev_ps = p_table[prev_ps - 1]
            else:
                p_table[i] = 0
                i += 1

    # prefix table is filled out, so lets print it
    print("Prefix Table:", p_table)

    # Search for a pattern match
    match_index = []

    # Pointer for input_string and pattern
    i, p = 0, 0

    while i < len(input_string):
        # If both characters match, advance both pointers by 1
        if pattern[p] == input_string[i]:
            i += 1
            p += 1

        # If the pointer is equal to the length of the pattern, we found a match
        if p == len(pattern):
            match_index.append(i - p)
            p = p_table[p - 1]

        # If there isn't a match, use the prefix table to skip ahead
        elif i < len(input_string) and pattern[p] != input_string[i]:
            # Don't worry about rematching previous p_table characters
            if p != 0:
                p = p_table[p - 1]
            else:
                i += 1

    if len(match_index) != 0:
        print("Pattern found in string: Yes")
        print(pattern, "found at index ", match_index)
    else:
        print("Pattern found in string: No")

    return


search_string = "ACAT ACGACACAGT"
pattern = "ACACAGT"
print("Matching using Z Algorithm:")
zalg(search_string, pattern)
print("\n\n\nMatching using KMP:")
kmp(search_string, pattern)
