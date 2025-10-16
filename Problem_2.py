'''
8 String to Integer (atoi)
https://leetcode.com/problems/string-to-integer-atoi/description/

Implement the myAtoi(string s) function, which converts a string to a 32-bit signed integer.

The algorithm for myAtoi(string s) is as follows:
Whitespace: Ignore any leading whitespace (" ").
Signedness: Determine the sign by checking if the next character is '-' or '+', assuming positivity if neither present.
Conversion: Read the integer by skipping leading zeros until a non-digit character is encountered or the end of the string is reached. If no digits were read, then the result is 0.
Rounding: If the integer is out of the 32-bit signed integer range [-2^31, 2^31 - 1], then round the integer to remain in the range. Specifically, integers less than -2^31 should be rounded to -2^31, and integers greater than 2^31 - 1 should be rounded to 2^31 - 1.

Return the integer as the final result.

Example 1:
Input: s = "42"
Output: 42
Explanation:
The underlined characters are what is read in and the caret is the current reader position.
Step 1: "42" (no characters read because there is no leading whitespace)
         ^
Step 2: "42" (no characters read because there is neither a '-' nor '+')
         ^
Step 3: "42" ("42" is read in)
           ^

Example 2:
Input: s = " -042"
Output: -42
Explanation:
Step 1: "   -042" (leading whitespace is read and ignored)
            ^
Step 2: "   -042" ('-' is read, so the result should be negative)
             ^
Step 3: "   -042" ("042" is read in, leading zeros ignored in the result)
               ^

Example 3:
Input: s = "1337c0d3"
Output: 1337
Explanation:
Step 1: "1337c0d3" (no characters read because there is no leading whitespace)
         ^
Step 2: "1337c0d3" (no characters read because there is neither a '-' nor '+')
         ^
Step 3: "1337c0d3" ("1337" is read in; reading stops because the next character is a non-digit)
             ^

Example 4:
Input: s = "0-1"
Output: 0
Explanation:
Step 1: "0-1" (no characters read because there is no leading whitespace)
         ^
Step 2: "0-1" (no characters read because there is neither a '-' nor '+')
         ^
Step 3: "0-1" ("0" is read in; reading stops because the next character is a non-digit)
          ^
Example 5:
Input: s = "words and 987"
Output: 0
Explanation:
Reading stops at the first non-digit character 'w'.

Constraints:
0 <= s.length <= 200
s consists of English letters (lower-case and upper-case), digits (0-9), ' ', '+', '-', and '.'.

Solution:
1. String (array) traversal:
We first trim the string and check if it starts with a valid sign or digit. Then we go through each character, stop at any non-digit, and build the number.
If the number goes beyond 32-bit range, we clamp it to Integer.MAX_VALUE or MIN_VALUE.
https://youtu.be/9prSQxNiaCM?t=2968
Time: O(N), Space: O(1)
'''
def myAtoi(s: str) -> int:
    s = s.lstrip()
    if s[0] != '+' and s[0] != '-' and not s[0].isdigit():
        return 0

    sign = 1 # +ve
    if s[0] == '-':
        sign = -1 # -ve
        s = s[1:]
    elif s[0] == '+':
        sign = 1 # +ve
        s = s[1:]

    N = len(s)
    INT_MAX = 2**31 - 1 # 2147483647
    INT_MIN = -2**31  # -2147483648
    limit = INT_MAX//10 # limit = 214748364, identical for INT_MAX and INT_MIN
    num = 0
    for i in range(N):
        c = s[i]
        # if char is not a digit, return num constructed so far
        if not c.isdigit():
            break
        digit = ord(c) - ord('0')

        # overflow handling
        if num > limit:
           return INT_MAX if sign==1 else INT_MIN
        elif num == limit:
            rem = digit % 10
            if sign == 1:
                if rem > 7: return INT_MAX
            else:
                if rem > 8: return INT_MIN

        # if we reach here, then num < limit
        num = num*10 + digit
    return sign*num

def run_myAtoi():
    tests = [("words and 987", 0),
             ("  -0012a42", -12),
             ("+1", 1),
             ("42", 42),
             (" -042", -42),
             ("1337c0d3", 1337),
             ("0-1", 0),
             ("2147483647", 2147483647), # in = INT_MAX, out = INT_MAX
             ("2147483648", 2147483647), # in = INT_MAX + 1, out = INT_MAX
             ("-2147483648", -2147483648), # in = INT_MIN, out = INT_MIN
             ("-2147483649", -2147483648), # in = INT_MIN - 1, out = INT_MIN
             ("3147483642", 2147483647), # in = >INT_MAX, out = INT_MAX
             ("-3147483642", -2147483648), # in = <INT_MAX, out = INT_MIN
             ]
    for test in tests:
        s, ans = test[0], test[1]
        print(f"\nstring = {s}")
        num = myAtoi(s)
        print(f"atoi = {num}")
        success = (ans == num)
        print(f"Pass: {success}")
        if not success:
            print("Failed")
            return

run_myAtoi()
