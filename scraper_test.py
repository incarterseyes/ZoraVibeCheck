from scraper import demo_scrape

# Get 100 items
collection_data = demo_scrape("carter")

# Print summary
print(f"\nFound {len(collection_data)} items")

# Print details of first few items to verify filtering
for i, item in enumerate(collection_data[:5]):
    print(f"\nItem {i+1}:")
    print(f"Title: {item['title']}")
    print(f"URL: {item['url']}")