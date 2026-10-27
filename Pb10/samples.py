import random
import time
from Pb10 import optimal_transmitters as fast

R, TESTS = 250, 10

L1, L2 = 1, 5000       # Range of circumference
p1, p2 = 0, 800       # Range of number of posts
c1, c2 =500, 1000         # Range of number of candidates

for t in range(1, TESTS + 1):
    L = random.randint(L1, L2)
    posts = random.sample(range(L), random.randint(min(p1,L), min(p2, L)))
    candidates = random.sample(range(L), random.randint(min(c1,L), min(c2, L)))


    print(f"\nTest {t}: \nCircumference L = {L}, Radius = {R}")
    print(f"Posts ({len(posts)}): {posts}")
    print(f"Candidates ({len(candidates)}): {candidates}")

    t=time.time()
    result = fast(posts, L, candidates, R)
    ta=time.time()-t
    
    print("Output:=>")
    if result[1] == None:
        print("No such configuration exists.")
    else:
        print(f"Overlaps: {result[0]}")
        print(f"Configuration: {result[1]}")
        
    print(f"Time Taken to execute excluding I/O: {ta:.3f} seconds")
    print("-" * 80)