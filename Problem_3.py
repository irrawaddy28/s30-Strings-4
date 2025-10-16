'''
937 Reorder Data in Log Files
https://leetcode.com/problems/reorder-data-in-log-files/description/

You are given an array of logs. Each log is a space-delimited string of words, where the first word is the identifier.

There are two types of logs:
Letter-logs: All words (except the identifier) consist of lowercase English letters.
Digit-logs: All words (except the identifier) consist of digits.

Reorder these logs so that:
The letter-logs come before all digit-logs.
The letter-logs are sorted lexicographically by their contents. If their contents are the same, then sort them lexicographically by their identifiers.
The digit-logs maintain their relative ordering.

Return the final order of the logs.

Example 1:
Input: logs = ["dig1 8 1 5 1","let1 art can","dig2 3 6","let2 own kit dig","let3 art zero"]
Output: ["let1 art can","let3 art zero","let2 own kit dig","dig1 8 1 5 1","dig2 3 6"]
Explanation:
The letter-log contents are all different, so their ordering is "art can", "art zero", "own kit dig".
The digit-logs have a relative order of "dig1 8 1 5 1", "dig2 3 6".

Example 2:
Input: logs = ["a1 9 2 3 1","g1 act car","zo4 4 7","ab1 off key dog","a8 act zoo"]
Output: ["g1 act car","a8 act zoo","ab1 off key dog","a1 9 2 3 1","zo4 4 7"]

Constraints:
1 <= logs.length <= 100
3 <= logs[i].length <= 100
All the tokens of logs[i] are separated by a single space.
logs[i] is guaranteed to have an identifier and at least one word after the identifier.

Solution:
1. Sorting
The problem is really a test on using custom comparator in sorting function.
https://youtu.be/Xr5bTeXTJC8?t=4327
Time: O(N log N), Space: O(1), N = no. of logs
'''
from typing import List
import functools

def custom_compare(log1, log2):
    # custom comparator return values:
    # -1: log 1 < log 2
    #  0: log 1 = log 2
    #  1: log 1 > log 2

    s1 = log1.split(" ", 1) # maxsplit = 1 -> returns list with 2 elements
    s2 = log2.split(" ", 1)
    is_digit1 = s1[1][0].isdigit()
    is_digit2 = s2[1][0].isdigit()

    if not is_digit1 and not is_digit2:
        # both log1 and log2 are letter logs
        id1, content1 = s1[0], s1[1]
        id2, content2 = s2[0], s2[1]
        if content1 != content2:
            if content1 > content2:
                return 1
            else:
                return -1
        else:
             if id1 > id2:
                 return 1
             else:
                 return -1

    elif not is_digit1 and is_digit2:
        # log1 letter log and log2 digit log
        return -1
    elif is_digit1 and not is_digit2:
        # log1 digit log and log2 letter log
        return 1
    else:
        return 0


def reorderLogFiles(logs: List[str]) -> List[str]:
    ''' Time: O(N log N), Space: O(1) '''
    if not logs:
        return []
    out_logs = sorted(logs, key=functools.cmp_to_key(custom_compare))
    return out_logs

def run_reorderLogFiles():
    tests = [(["dig1 8 1 5 1","let1 art can","dig2 3 6","let2 own kit dig",
               "let3 art zero"],  ["let1 art can","let3 art zero","let2 own kit dig","dig1 8 1 5 1","dig2 3 6"]),
             (["a1 9 2 3 1","g1 act car","zo4 4 7","ab1 off key dog","a8 act zoo"], ["g1 act car","a8 act zoo","ab1 off key dog","a1 9 2 3 1","zo4 4 7"]),
    ]
    for test in tests:
        logs, ans = test[0], test[1]
        print(f"\nlogs = {logs}")
        result = reorderLogFiles(logs)
        print(f"result = {result}")
        success = (ans == result)
        print(f"Pass: {success}")
        if not success:
            print("Failed")
            return

run_reorderLogFiles()
