# Update to run agent_r.py, agent_q.py, and agent_m.py and store results in a table with recommendations
import subprocess
import pandas as pd

# Function to run a script and capture its output
def run_script(script_name):
    try:
        result = subprocess.check_output(["python3", script_name], text=True)
        return result.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"

# Run all three scripts
result_q = run_script("agent_q.py")
result_r = run_script("agent_r.py")
result_m = run_script("agent_m.py")

# Extract prices from results (assuming the scripts print prices in a specific format)
def extract_price(result):
    try:
        return float(result.split(":")[-1].strip().replace("$", ""))
    except:
        return None

price_q = extract_price(result_q)
price_r = extract_price(result_r)
price_m = extract_price(result_m)

# Calculate recommended price based on conditions
if price_r is not None and price_q is not None:
    recommended_price = None
    if price_m is not None:
        if price_m > price_r * 1.1 or price_m < price_q * 0.7:
            recommended_price = f"Adjust to ${(price_r * 1.1 + price_q * 0.7) / 2:.2f}"  # Average of target range
        else:
            recommended_price = "Price is within the target range"
    else:
        recommended_price = "Motel M price not available"
else:
    recommended_price = "Competitor prices not available"

# Store results in a table
data = {
    "Script": ["agent_q.py", "agent_r.py", "agent_m.py"],
    "Result": [result_q, result_r, result_m],
    "Price": [price_q, price_r, price_m],
    "Recommendation": ["", "", recommended_price]
}
df = pd.DataFrame(data)

# Save the table to a CSV file
df.to_csv("results_table.csv", index=False)

print("Results saved to results_table.csv")