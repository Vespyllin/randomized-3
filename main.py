def compute_optimal_prices(n, k):
    # Initialize tables
    R = [[0.0 for _ in range(k+1)] for _ in range(n)]  # Expected revenue
    P = [[0.0 for _ in range(k+1)] for _ in range(n)]   # Optimal prices

    # Base cases:
    # No tickets
    for i in range(n):
        R[i][0] = 0.0  

    # Last customer
    for t in range(1, k+1):
        R[n-1][t] = 0.25
        P[n-1][t] = 0.5

    # Backward induction
    for i in range(n-2, -1, -1):
        for t in range(1, k+1):
            # Compute optimal price
            p = (1 + R[i+1][t] - R[i+1][t-1]) / 2
            p = max(0.0, min(1.0, p)) 
            P[i][t] = p
            
            # Compute expected revenue for induction
            R[i][t] = (1-p)*(p + R[i+1][t-1]) + p*R[i+1][t]
    
    return P

x = compute_optimal_prices(7,3)

print("======")
print("    ", end="")
for j in range(0,len(x[0])):
    print(j, "    ", end="")
print()
for i in range(0,len(x)):
    print(i,":", end=" ")
    for j in range(0,len(x[i])):
        print("{:.2f}".format(x[i][j]), end=", ")
    print()

