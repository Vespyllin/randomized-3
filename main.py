import random
import statistics
import matplotlib.pyplot as plt


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
    (100, 10),
    (100, 25),
    (100, 50),
    (100, 70),
    (100, 90),
    (500, 50),
    (500, 125),
    (500, 250),
    (500, 350),
    (500, 450),
    (750, 75),
    (750, 187),
    (750, 375),
    (750, 525),
    (750, 675),
    (1000, 100),
    (1000, 250),
    (1000, 500),
    (1000, 700),
    (1000, 900),
]

ITER = 1000
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

# Extended test cases for 10%, 25%, 50%, 75%, 90% availability
test_cases = [
    # N=100 cases
    (100, 10), (100, 25), (100, 50), (100, 75), (100, 90),
    # N=1000 cases 
    (1000, 100), (1000, 250), (1000, 500), (1000, 750), (1000, 900)
]

# Beautiful color schemes
def generate_plot(n_value):
    plt.figure(figsize=(14, 8))
    
    cases = [(n,k) for n,k in test_cases if n == n_value]
    availability_labels = ['10%', '25%', '50%', '75%', '90%']
    
    for idx, (n, k) in enumerate(cases):
        optimal_prices = compute_optimal_prices(n, k)
        basic_revenues = []
        optimal_revenues = []
        
        for _ in range(ITER):
            basic_revenues.append(simulate_purchases(n, k))
            optimal_revenues.append(simulate_purchases(n, k, optimal_prices))
        
        # Plot with more transparency (alpha=1)
        plt.scatter([idx]*ITER, basic_revenues, 
                   color='blue',
                   alpha=0.5,  # Changed to more transparent
                   marker='o',
                   s=50,
                   edgecolor='white',
                   linewidth=0.5,
                   label='Basic' if idx == 0 else None)
        
        plt.scatter([idx]*ITER, optimal_revenues, 
                   color='green',
                   alpha=0.5,  # Changed to more transparent
                   marker='o',
                   s=50,
                   edgecolor='white',
                   linewidth=0.5,
                   label='Optimal' if idx == 0 else None)
    
    # Rest of your plotting code remains the same...
        
        # Customize plot
    plt.xticks(range(len(cases)), availability_labels)
    plt.xlabel('Ticket Availability (K/N)', fontsize=12)
    plt.ylabel('Revenue', fontsize=12)
    plt.title(f'Revenue Distribution Comparison (N={n_value})', fontsize=14)
    
    # Add grid and legend
    plt.grid(True, alpha=0.5, linestyle='--')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Add light background for each availability group
    # for i in range(len(cases)):
    #     plt.axvspan(i-0.5, i+0.5, facecolor='#F5F5F5', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'revenue_comparison_N{n_value}.png', dpi=300, bbox_inches='tight')
    print(f"Plot for N={n_value} saved as revenue_comparison_N{n_value}.png")

# Generate both plots
generate_plot(100)
generate_plot(1000)


test_cases = [
    (100, 10),
    (100, 25),
    (100, 50),
    (100, 70),
    (100, 90),
    (500, 50),
    (500, 125),
    (500, 250),
    (500, 350),
    (500, 450),
    (750, 75),
    (750, 187),
    (750, 375),
    (750, 525),
    (750, 675),
    (1000, 100),
    (1000, 250),
    (1000, 500),
    (1000, 700),
    (1000, 900),
]

ITER = 1000

for n, k in test_cases:
    basic, optimal, diff = run_simulations(ITER, n, k)
    print_statistics(basic, optimal, diff, n, k)
