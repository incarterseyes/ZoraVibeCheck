from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from io import BytesIO
from PIL import Image
import time

class ZoraScraper:
    def __init__(self, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size(1920, 1080)
        
    def get_collected_works(self, username, max_items=100):  # Increased default to 100
        url = f"https://zora.co/@{username}/collected"
        print(f"Accessing URL: {url}")
        self.driver.get(url)
        
        print("Waiting for page to load...")
        wait = WebDriverWait(self.driver, 30)
        
        try:
            print("Waiting for images...")
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'img')))
            time.sleep(5)
            
            collection_data = []
            processed_urls = set()
            scroll_count = 0
            
            while len(collection_data) < max_items and scroll_count < 15:  # Increased scroll limit
                print(f"\nScroll {scroll_count + 1}: Looking for NFTs...")
                
                nft_elements = self.driver.find_elements(By.CSS_SELECTOR, 'img[alt]:not([alt=""])')
                
                for element in nft_elements:
                    if len(collection_data) >= max_items:
                        break
                        
                    try:
                        src = element.get_attribute('src')
                        title = element.get_attribute('alt')
                        
                        # Skip unwanted images
                        if (src and 
                            src not in processed_urls and 
                            not src.startswith('data:') and
                            not 'privy-zorb' in src and
                            not 'avatar' in title.lower()):  # Check title for 'avatar'
                            
                            processed_urls.add(src)
                            print(f"Processing: {title}")
                            
                            response = requests.get(src)
                            img_data = Image.open(BytesIO(response.content))
                            collection_data.append({
                                'image': img_data,
                                'title': title,
                                'url': src
                            })
                            print(f"Successfully processed item {len(collection_data)}")
                            
                    except Exception as e:
                        print(f"Error processing element: {str(e)}")
                
                scroll_count += 1
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )
                time.sleep(3)
            
            return collection_data
            
        except Exception as e:
            print(f"Error during scraping: {str(e)}")
            return []
        
    def cleanup(self):
        self.driver.quit()

def demo_scrape(username, max_items=100):
    scraper = ZoraScraper()
    try:
        print(f"Starting scrape for user: {username}")
        collection_data = scraper.get_collected_works(username, max_items)
        print(f"\nScraping Summary:")
        print(f"Successfully scraped {len(collection_data)} items")
        return collection_data
    except Exception as e:
        print(f"Scraping failed: {str(e)}")
        return []
    finally:
        scraper.cleanup()