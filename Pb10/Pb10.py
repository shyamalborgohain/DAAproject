from bisect import bisect_left, bisect_right
from math import inf

def optimal_transmitters(posts, L, candidates, r=250):
    
    if posts==[]:
        return 0, []
    if candidates==[]:
        return -1, None
    if 2 * r >= L:
        return 0, [candidates[0]]
    
    P = sorted(q % L for q in posts)
    n = len(P)
    
    # Unrolling the Circle into Linear Arcs
    extP = [q - L for q in P] + P + [q + L for q in P]
    locs = {}
    # Finding the range of check posts covered by each candidate transmitter
    for ca in candidates:
        c = ca % L
        lo = bisect_left(extP, c - r)
        hi = bisect_right(extP, c + r) - 1
        if lo > hi:
            continue
        
        # making sure that 0<=lo<n
        if lo >= n: lo -= n; hi -= n
        elif lo < 0: lo += n; hi += n
        
        if hi - lo + 1 >= n:
            return 0, [ca]
        locs.setdefault((lo, hi), ca)
    
    arcs = sorted(locs) # interval/arc is the set of ordered checkpost covered by transmitters
    M = len(arcs)
    if M == 0:
        return -1, None
    
    start = [arc[0] for arc in arcs]
    end = [arc[1] for arc in arcs]
    
    best, best_chain = inf, None
    
    # O(M^3) DP Loops
    for a in range(M): # Fix the starting interval of the chain
        sa = start[a]
        dp = [inf] * M
        dp[a] = 0
        par = [-1] * M
        
        for i in range(a + 1, M):  # i as the last interval in the current sub-chain under anchor a
            if start[i] == sa:
                continue
            
            best_val = inf
            best_j = -1
            
            # Loop through all previous arcs in the current chain
            for j in range(a, i):
                if dp[j] < inf: # Check if a valid, unbroken chain exists from anchor a to j
                
                    if end[j] >= start[i] - 1:# ensure arc j reaches far enough to touch/overlap arc i (No gaps)
                        val = dp[j] + end[j]
                        if val < best_val:
                            best_val = val
                            best_j = j

            if best_val < inf: # Updating best_val and parent for chain where a is the anchor and i is the last interval
                dp[i] = best_val - start[i] + 1
                par[i] = best_j
            
        #Circle Wrap-Around Verification
        for i in range(a, M):
            # Verify if the chain closes the circular loop back to anchor a
            if dp[i] < inf and end[i] >= sa + n - 1: 
                cost = dp[i] + (end[i] - sa - n + 1)
                if cost < best:
                    best = cost
                    # Backtrack to reconstruct the optimal chain sequence
                    chain = [] # Temporary list storing the parent indices of the current valid loop
                    k = i
                    while k != -1:
                        chain.append(k)
                        k = par[k]
                    best_chain = chain[::-1] # Optimal sequence of intervals for the current anchor "a"
    
    if best == inf:
        return -1, None
    
    return best, [locs[arcs[k]] for k in best_chain]

if __name__ == "__main__":
    posts = [100, 400, 700, 900]
    L = 1000
    candidates = [50, 350, 650, 950]
    print(*optimal_transmitters(posts, L, candidates, r=250))