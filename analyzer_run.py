from analyzer import analyze_collection

# Your OpenAI API key
api_key = "your-api-key-here"

# Analyze collection
# Change the "username" to be your your username
# Cahnge the max_items value to how many tokens you want to test
report = analyze_collection("username", api_key, max_items=5)