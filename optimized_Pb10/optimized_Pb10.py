from bisect import bisect_left, bisect_right
from collections import deque
from math import inf

def optimal_transmitters(posts, L, candidates, r=250):
    
    if posts==[]:
        return 0, []
    if candidates==[]:
        return -1,None
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
    # Pre-calculate the first index where each unique start/end value appears
    sg, eg = [0]*M, [0]*M
    for i in range(1, M):
        # sg["i"] and eg["i"] indicate the first indices in arcs sharing the exact same start and end positions as arc "i", respectively
        sg[i] = sg[i-1] if start[i] == start[i-1] else i
        eg[i] = eg[i-1] if end[i] == end[i-1] else i

    # lo_idx["i"]: First interval ending close enough to start["i"] to avoid coverage gaps
    lo_idx = [bisect_left(end, start[i]-1) for i in range(M)]
    
    # hi_idx["i"]: Latest interval that can safely link to "i" without
    # any endpoints in common
    hi_idx = [min(sg[i], eg[i]) - 1 for i in range(M)]
    
    best, best_chain = inf, None
    for a in range(M): # Fix the starting interval of the chain at index "a"
        sa = start[a]
        dp = [inf]*M # dp["i"]: Minimum penalty to cover from anchor "a" upto interval "i" first set to inf
        dp[a] = 0
        par = [-1]*M # Parent pointers for path reconstruction
        
        dq = deque() # Monotonic queue tracking pairs of (transition_value, interval_index)
        ptr = a
        for i in range(a+1, M): # Evaluate interval "i" as the last interval in the current sub-chain under anchor "a"
            if start[i] == sa:
                continue
            while ptr <= hi_idx[i]: # Queue candidates whose endpoints do not match interval "i"
                if dp[ptr] < inf: # checking reachability before queuing
                    val = dp[ptr] + end[ptr]
                    while dq and dq[-1][0] >= val: 
                        # Maintain a strictly ascending cost order by removing sub-optimal options from the tail of dq
                        dq.pop()
                    dq.append((val, ptr))
                ptr += 1
            
            lo = max(a, lo_idx[i]) # Remove out-of-bounds intervals from the front that create an uncovered gap
            while dq and dq[0][1] < lo:
                dq.popleft()
            if dq: # update the dp state from the minimum valid predecessor
                dp[i] = dq[0][0] - start[i] + 1
                par[i] = dq[0][1]

        #Circle Wrap-Around Verification
        for i in range(a, M):
        # Verify if the chain closes the circular loop back to anchor a
            if dp[i] < inf and end[i] >= sa + n - 1:
                cost = dp[i] + max(0, end[i] - sa - n + 1)
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

# if __name__ == "__main__":
#     posts = [100, 400, 700, 900]
#     L = 1000
#     candidates = [50, 350, 650, 950]
#     print(*optimal_transmitters(posts, L, candidates, r=250))