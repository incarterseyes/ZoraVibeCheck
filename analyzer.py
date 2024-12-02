from scraper import demo_scrape
import requests
from openai import OpenAI
import time
from PIL import Image
from io import BytesIO
import base64
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, rpm_limit=500):
        self.rpm_limit = rpm_limit
        self.requests = []
        
    def wait_if_needed(self):
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)
        
        # Remove requests older than 1 minute
        self.requests = [req_time for req_time in self.requests if req_time > minute_ago]
        
        # If we're at the limit, wait until oldest request is more than a minute old
        if len(self.requests) >= self.rpm_limit:
            wait_time = (self.requests[0] - minute_ago).total_seconds()
            if wait_time > 0:
                time.sleep(wait_time)
            self.requests = self.requests[1:]
        
        # Add current request
        self.requests.append(now)

class CollectionAnalyzer:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.rate_limiter = RateLimiter(rpm_limit=450)  # Using 450 to be safe

    def get_optimized_image_base64(self, image_url):
        """Download, optimize, and encode image"""
        try:
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            
            # Resize to optimal size
            ratio = 768 / min(img.size)
            new_size = tuple(int(dim * ratio) for dim in img.size)
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Convert to JPEG
            buffered = BytesIO()
            img.save(buffered, format="JPEG", quality=85)
            
            # Encode to base64
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            return img_str
            
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return None

    def analyze_piece(self, image_url):
        """Analyze a single piece with rate limiting"""
        try:
            base64_image = self.get_optimized_image_base64(image_url)
            if not base64_image:
                return None

            # Check rate limits before making request
            self.rate_limiter.wait_if_needed()

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Describe this artwork's style and mood in 2-3 short sentences."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=100
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error analyzing piece: {str(e)}")
            return None

    def analyze_collection_summary(self, descriptions):
        """Generate summary with rate limiting"""
        try:
            self.rate_limiter.wait_if_needed()
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": "Summarize this collector's style preferences in 3-4 sentences: " + descriptions
                    }
                ],
                max_tokens=150
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            return None

    def analyze_collection(self, items, max_items=5):
        print("\nAnalyzing collection...")
        piece_analyses = []
        start_time = time.time()
        
        for i, item in enumerate(items[:max_items]):
            print(f"\nAnalyzing piece {i+1}/{min(len(items), max_items)}: {item['title']}")
            analysis = self.analyze_piece(item['url'])
            
            if analysis:
                piece_analyses.append({
                    'title': item['title'],
                    'analysis': analysis
                })
                print(f"Analysis: {analysis}")

        if piece_analyses:
            all_analyses = "\n".join([p['analysis'] for p in piece_analyses])
            collection_summary = self.analyze_collection_summary(all_analyses)
        else:
            collection_summary = "Unable to analyze collection due to errors."

        total_time = time.time() - start_time
        print(f"\nTotal analysis time: {total_time:.2f} seconds")

        return {
            'summary': collection_summary,
            'piece_analyses': piece_analyses,
            'analysis_time': total_time
        }

def analyze_collection(username, api_key, max_items=5):
    print(f"Fetching collection for @{username}...")
    collection_data = demo_scrape(username, max_items=max_items)
    
    analyzer = CollectionAnalyzer(api_key)
    report = analyzer.analyze_collection(collection_data, max_items)
    
    print("\n🎨 Collection Analysis Report 🎨")
    print("===============================")
    print("\n📝 Collection Summary:")
    print(report['summary'])
    
    print("\n✨ Individual Pieces:")
    for piece in report['piece_analyses']:
        print(f"\n• {piece['title']}:")
        print(f"  {piece['analysis']}")
    
    return report