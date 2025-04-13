import random

def compute_optimal_prices(n, k):
    # Initialize tables
    R = [[0.0 for _ in range(k+1)] for _ in range(n)]  # Expected revenue
    P = [[0.0 for _ in range(k+1)] for _ in range(n)]   # Optimal prices

    # Base cases:
    # No tickets
    for c in range(n):
        R[c][0] = 0.0  

    # Last customer
    for t in range(1, k+1):
        R[n-1][t] = 0.25
        P[n-1][t] = 0.5

    # Backward induction
    # customer #
    for c in range(n-2, -1, -1):
        # tickets left
        for t in range(1, k+1):
            # Compute optimal price
            p = (1 + R[c+1][t] - R[c+1][t-1]) / 2
            p = max(0.0, min(1.0, p)) 
            P[c][t] = p
            
            # Compute expected revenue for induction
            R[c][t] = (1-p)*(p + R[c+1][t-1]) + p*R[c+1][t]
    
    return P


def get_optimal_price(c,t):
    return optimal_prices[c][t]

def get_basic_price():
    return 1 - K/N

N = 10
K = 4

optimal_prices = compute_optimal_prices(N,K)

def simulate_purchases(basic):
    total_revenue = 0
    remaining_tickets = K
    
    for customer in range(0, N):
        if remaining_tickets == 0:
            break  # No tickets left
        
        p = get_basic_price() if basic else get_optimal_price(customer, remaining_tickets)
        
        cust_val = random.uniform(0, 1)
        
        # If customer is happy with the price, sell
        if cust_val >= p:
            total_revenue += p
            remaining_tickets -= 1
    
    return total_revenue

breakeven = 0
for i in range(10000):
    basic = simulate_purchases(True)
    optimal = simulate_purchases(False)
    breakeven = breakeven + (1 if basic > optimal else -1)

print(breakeven)