'''
Find object in a grid
Given a char grid (o represents an empty cell and x represents a target object) and an API getResponse which would give you a response w.r.t. to your previous position. Write a program to find the object. You can move to any position.

enum Response { HOTTER, // Moving closer to target COLDER, // Moving farther from target SAME, // Same distance from the target as your previous guess EXACT; // Reached destination }

Throws an error if 'row' or 'col' is out of bounds

public Response getResponse(int row, int col) { // black box }

Example 1:
Input: [['o', 'o', 'o'], ['o', 'o', 'o'], ['x', 'o', 'o']]
Output: [2, 0] Example 2:

Example 2:
Input: [['o', 'o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o', 'o'], ['o', 'o', 'o', 'x', 'o'], ['o', 'o', 'o', 'o', 'o']]
Output: [4, 3] Assumptions:

There is always one and only one object. If it's not the target object the 1st call would always give HOTTER as result, ortherwise EXACT.

Solution
1. Linear Search
See archive for code
https://youtu.be/4n_RNFyv9RQ?t=3834
Time: O(NM), Space: O(1)

2. Optimized Linear Search
See archive for code
https://youtu.be/4n_RNFyv9RQ?t=3920
Time: O(N+M), Space: O(1)

3. Binary Search (optimal)
Perform binary search on the grid by converting 2D indices of the grid to 1D indices. Doing this, we are able to convert a 2D search into a 1D search which is simpler.

Eg. Let grid be of size = M x N
Then,
1D (id) -> 2D (row,col)
row = id // N
col = id % N

2D (row,col) -> 1D (id)
id = row*N + col

We compute the mid and call getResponse(mid) API for two reasons:
1. To register the mid index as the previous index with getResponse()
2. To check if mid == target (in which getResponse() will return EXACT)
(We don't care about other response types at this time)

Now, we would like to probe the left half. We make one more call to getResponse() using mid-1, i.e. getResponse(mid-1). Three possibilities:
1. If response=EXACT, we have reached our target and we return mid - 1
2. If response=HOTTER, it means that the target is in the left half. We move high = mid-1
3. If response=COLDER, it means that the target is in the right half. We move low = mid+1
(We didn't find response=SAME useful in this search)

Note: When probing the left half, why did we not use low and used mid-1 instead?
Using low will result in missing the target in some cases.

For eg, low=0,high=10,mid=5.
Let index of target=3
Thus, dist(low,target)(3) > dist(mid,target)(2).
This will cause getResponse(low=0) to return COLDER and hence we move low to
low = mid+1 = 5 + 1 = 6
Since low=6,high=10, we have moved to the right half but the target is in the left half target. Hence, we have missed the target.

https://youtu.be/4n_RNFyv9RQ?t=4102

Time: O(log(NM), Space: O(1)
'''
from enum import Enum

class Response(Enum):
    EXACT = 0
    SAME = 1
    HOTTER = 10
    COLDER = -10

class SearchObj:
    def __init__(self, M, N, target_row, target_col):
          if M == 0 and N == 0:
              return []
          self.M, self.N = M, N
          self.target_row = target_row
          self.target_col = target_col

          self.grid = [['o']*N for _ in range(M)]
          self.grid[self.target_row][self.target_col] = 'x'

          self.prev_row = -1
          self.prev_col = -1

    def distance(self,x1,y1,x2,y2):
        # convert 2D coordinates (x,y) to 1D coordinate
        i = x1*self.N + y1
        j = x2*self.N + y2
        return abs(i-j)

    def getResponse(self, r, c):
        if r == self.target_row and c == self.target_col:
            return Response.EXACT

        if self.prev_row == -1 or self.prev_col == -1:
            old_dist = float('inf')
        else:
            old_dist = self.distance(self.prev_row, self.prev_col, self.target_row, self.target_col)
        new_dist = self.distance(r, c, self.target_row, self.target_col)

        self.prev_row , self.prev_col = r, c

        if new_dist == 0:
            return Response.EXACT
        elif new_dist < old_dist:
            return Response.HOTTER
        elif new_dist > old_dist:
            return Response.COLDER
        elif new_dist == old_dist:
            return Response.SAME

    def binarySearch(self):
        low = 0
        high = self.M*self.N - 1

        while low <= high:
            mid = low + (high - low) // 2

            # get response of mid
            row = mid // self.N
            col = mid % self.N
            response_mid = self.getResponse(row, col)
            if response_mid == Response.EXACT:
                return [row, col]

            # get response of mid+1 to probe left half
            # Note: using low instead of mid+1 will result in
            # missing the target in some cases.
            # For eg, low=0,high=10,mid=5. Let index of target=4
            # This will cause response_left = COLDER and move low to
            # low = mid+1 = 5 + 1 = 6
            # Now, low=6,high=10,mid=8 ... thus missing the target
            # at index = 4 (left half)
            # Another eg. M=6,N=5,target=(3,4)
            row = (mid-1) // self.N
            col = (mid-1) % self.N
            response_left = self.getResponse(row, col)
            if response_left == Response.EXACT:
                return [row, col]
            elif response_left == Response.HOTTER:
                high = mid - 1
            else:
                low = mid + 1

        row = low // self.N
        col = low % self.N
        return [row,col]

def run_SearchObj():
    tests = [(6,5,4,3),
             (6,5,3,4),
             (6,5,0,0),
             (6,5,5,4),
             (6,5,3,0),
             (2,3,1,2),
             (1,5,0,4),
             (5,1,4,0),
    ]
    for test in tests:
        M, N, target_row, target_col = test[0], test[1], test[2], test[3]
        ans = [target_row, target_col]
        print(f"\nM, N = {M}, {N}")
        print(f"target (row, col) = ({target_row},{target_col})")
        sol = SearchObj(M,N,target_row,target_col)
        row, col = sol.binarySearch()
        success = (ans == [row, col])
        print(f"Pass: {success}")
        if not success:
            print("Failed")
            return

run_SearchObj()