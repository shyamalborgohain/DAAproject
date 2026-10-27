from optimized_Pb10 import optimal_transmitters

if __name__ == "__main__":
    posts = [100, 400, 700, 900]
    L = 1000
    candidates = [50, 350, 650, 950]
    print(*optimal_transmitters(posts, L, candidates, r=250))