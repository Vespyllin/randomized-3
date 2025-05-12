import random
import statistics

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

def simulate_purchases(n, k, optimal_prices = None):
    total_revenue = 0
    remaining_tickets = k
    
    for customer in range(0, n):
        if remaining_tickets == 0:
            break  # No tickets left
        
        p = (1 - k/n) if not optimal_prices else optimal_prices[customer][remaining_tickets]
        
        cust_val = random.uniform(0, 1)
        
        # If customer is happy with the price, sell
        if cust_val >= p:
            total_revenue += p
            remaining_tickets -= 1
    
    return total_revenue

def print_statistics(basic_revenues, optimal_revenues, diff, n, k):
    print(f"=== Statistics for N={n}, K={k} ===")
    print("Basic Pricing Strategy:")
    print(f"  Avg Revenue: {statistics.mean(basic_revenues):.4f}")
    print(f"  Std Dev: {statistics.stdev(basic_revenues):.4f}")
    print(f"  Min: {min(basic_revenues):.4f}")
    print(f"  Max: {max(basic_revenues):.4f}")
    
    print("\nOptimal Pricing Strategy:")
    print(f"  Avg Revenue: {statistics.mean(optimal_revenues):.4f}")
    print(f"  Std Dev: {statistics.stdev(optimal_revenues):.4f}")
    print(f"  Min: {min(optimal_revenues):.4f}")
    print(f"  Max: {max(optimal_revenues):.4f}")
    
    print("\nComparison:")
    print(f"  Avg Improvement: {statistics.mean(diff):.4f}")
    print(f"  Improvement %: {statistics.mean(diff)/statistics.mean(basic_revenues)*100:.2f}%")
    print(f"  Optimal better: {sum(i > 0 for i in diff)/len(diff)*100:.2f}% of cases")
    print(f"  Basic better: {sum(i < 0 for i in diff)/len(diff)*100:.2f}% of cases\n")

def run_simulations(num_simulations, n, k):
    optimal_prices = compute_optimal_prices(n,k)

    basic_revenues = []
    optimal_revenues = []
    diff = []
    
    for _ in range(num_simulations):
        basic_rev = simulate_purchases(n, k)
        optimal_rev = simulate_purchases(n, k, optimal_prices)
        
        basic_revenues.append(basic_rev)
        optimal_revenues.append(optimal_rev)
        diff.append(optimal_rev - basic_rev)
    
    return basic_revenues, optimal_revenues, diff

test_cases = [
    (10, 2),
    (10, 5),  
    (100, 10),
    (100, 50),
    (500, 50),
    (500, 200),
    (1000, 50),
    (1000, 400),
]

ITER = 1000

for n, k in test_cases:
    basic, optimal, diff = run_simulations(ITER, n, k)
    print_statistics(basic, optimal, diff, n, k)
