import flickrapi
import os
import json
import requests
import time
import re
from pathlib import Path
from dotenv import load_dotenv
import sys

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# API keys now loaded from environment variables (via .env file or system env)
API_KEY = os.getenv('FLICKR_API_KEY')
API_SECRET = os.getenv('FLICKR_API_SECRET')

TARGET_USERNAME = 'daniel_friedman'
# Add URL as a backup method
TARGET_URL = 'https://www.flickr.com/photos/daniel_friedman/'
OUTPUT_DIR = Path('flickr_output')
X_LARGE_SIZE_LABEL = 'X-Large' # Adjust if necessary, check API response for available sizes

# --- Helper Functions ---
def extract_username_from_url(url):
    """Extract the username from a Flickr URL"""
    pattern = r'flickr\.com/photos/([^/]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def get_user_id(flickr, username):
    """Get the Flickr user ID for a given username."""
    try:
        print(f"Looking up user: {username}")
        user = flickr.people.findByUsername(username=username)
        nsid = user['user']['nsid']
        print(f"Found user {username} with ID: {nsid}")
        return nsid
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_user_id_from_url_path(flickr, url_path):
    """Try using the URL path component as the NSID or lookup."""
    try:
        # First try if the path is directly a valid NSID
        try:
            print(f"Trying URL path as NSID: {url_path}")
            user_info = flickr.people.getInfo(user_id=url_path)
            if user_info:
                nsid = user_info['person']['nsid']
                print(f"URL path is a valid NSID: {nsid}")
                return nsid
        except Exception as e:
            print(f"URL path is not directly a valid NSID: {e}")
        
        # Try looking up as username
        try:
            return get_user_id(flickr, url_path)
        except Exception as e:
            print(f"Could not find user with URL path as username: {e}")
            
        return None
    except Exception as e:
        print(f"Error trying URL path methods: {e}")
        return None

def extract_nsid_from_html(url):
    """Extract NSID from the HTML content of a Flickr page."""
    try:
        print(f"Trying to extract NSID from HTML of {url}")
        response = requests.get(url)
        if response.status_code == 200:
            # Look for pattern like "nsid":"NSID" in the HTML - this is more reliable
            nsid_pattern = r'"nsid":"([^"]+)"'
            matches = re.findall(nsid_pattern, response.text)
            if matches:
                for potential_nsid in matches:
                    if re.match(r'^\d+@N\d+$', potential_nsid):
                        print(f"Found potential NSID in HTML: {potential_nsid}")
                        return potential_nsid
            
            # Fall back to older patterns
            nsid_pattern = r'"owner":"([^"]+)"'
            matches = re.findall(nsid_pattern, response.text)
            if matches:
                for potential_nsid in matches:
                    if re.match(r'^\d+@N\d+$', potential_nsid):
                        print(f"Found potential NSID in HTML: {potential_nsid}")
                        return potential_nsid
                print(f"Found potential owner but not in NSID format: {matches[0]}")
                return None
            
            # Try another pattern for albums
            nsid_pattern = r'data-user="([^"]+)"'
            matches = re.findall(nsid_pattern, response.text)
            if matches:
                print(f"Found potential NSID from data-user: {matches[0]}")
                return matches[0]
                
            print("Could not find NSID pattern in HTML")
        else:
            print(f"Failed to fetch HTML: {response.status_code}")
        return None
    except Exception as e:
        print(f"Error extracting NSID from HTML: {e}")
        return None

def download_photo(url, filepath):
    """Downloads a photo from a URL to a specified filepath."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {filepath.name}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return False

def save_metadata(photo_info, filepath):
    """Saves photo metadata as a JSON file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(photo_info, f, indent=4, ensure_ascii=False)
        print(f"Saved metadata: {filepath.name}")
        return True
    except IOError as e:
        print(f"Error saving metadata {filepath.name}: {e}")
        return False

# --- Main Script ---
def main():
    # Check if API keys were loaded successfully
    if not API_KEY or not API_SECRET:
        print("ERROR: FLICKR_API_KEY or FLICKR_API_SECRET not found.")
        print("       Ensure they are set in your .env file or environment variables.")
        return

    # Authenticate
    # Using non-OAuth for public data access, adjust if private data is needed
    try:
        flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET, format='parsed-json')
        print("Flickr API authentication successful (public access).")
    except Exception as e:
        print(f"Error authenticating with Flickr API: {e}")
        return

    # Get the user ID using multiple methods
    user_id = None
    
    # Method 1: Directly try the username
    user_id = get_user_id(flickr, TARGET_USERNAME)
    
    # Method 2: Try extracting username from URL and use that
    if not user_id:
        url_username = extract_username_from_url(TARGET_URL)
        if url_username and url_username != TARGET_USERNAME:
            print(f"Trying URL extracted username: {url_username}")
            user_id = get_user_id(flickr, url_username)
    
    # Method 3: Try using the URL path as an NSID
    if not user_id:
        url_path = extract_username_from_url(TARGET_URL)
        if url_path:
            user_id = get_user_id_from_url_path(flickr, url_path)
    
    # Method 4: Try extracting NSID from HTML
    if not user_id:
        user_id = extract_nsid_from_html(TARGET_URL)
        if user_id:
            # Verify this NSID works
            try:
                user_info = flickr.people.getInfo(user_id=user_id)
                print(f"Verified NSID from HTML: {user_id}")
                username = user_info['person']['username']['_content']
                print(f"Username for this NSID: {username}")
            except Exception as e:
                print(f"Could not verify NSID from HTML: {e}")
                user_id = None
    
    if not user_id:
        print("ERROR: Could not find a valid Flickr user ID by any method.")
        print("Please check the username or URL and try again.")
        return

    # Create output directory
    user_output_dir = OUTPUT_DIR / TARGET_USERNAME
    user_output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {user_output_dir}")

    # Get photos for the user
    page = 1
    total_pages = 1 # Will be updated after first call
    photos_processed = 0
    photos_downloaded = 0
    photos_failed = 0

    while page <= total_pages:
        print(f"Fetching page {page}...")
        try:
            # Fetch photos list for the current page
            # extras includes tags, description, date_taken, owner_name, geo, url_o (original), url_k (2048), url_h (1600), url_l (1024), url_c (800), etc.
            # We explicitly ask for X-Large size URL if available. Check documentation for all size suffixes.
            photos_data = flickr.people.getPublicPhotos(
                user_id=user_id,
                extras='description,tags,date_taken,geo,owner_name,machine_tags,o_dims,views,media',
                per_page=100, # Max 500
                page=page
            )

            total_pages = photos_data['photos']['pages']
            current_photos = photos_data['photos']['photo']
            print(f"Found {len(current_photos)} photos on page {page}/{total_pages}.")

            for photo in current_photos:
                photos_processed += 1
                photo_id = photo['id']
                photo_title = photo.get('title', 'untitled')
                safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in photo_title) # Sanitize title for filename
                base_filename = f"{photo_id}_{safe_title[:50]}" # Limit filename length

                print(f"Processing photo {photos_processed}: {photo_id} ('{photo_title}')")

                # Prepare metadata to save
                metadata = {
                    'id': photo_id,
                    'title': photo_title,
                    'description': photo.get('description', {}).get('_content', ''),
                    'tags': photo.get('tags', '').split(),
                    'machine_tags': photo.get('machine_tags', ''),
                    'date_taken': photo.get('datetaken', ''),
                    'owner_name': photo.get('ownername', ''),
                    'views': photo.get('views', 0),
                    'media': photo.get('media', ''),
                    'latitude': photo.get('latitude'),
                    'longitude': photo.get('longitude'),
                    'accuracy': photo.get('accuracy'),
                    'flickr_url': f"https://www.flickr.com/photos/{user_id}/{photo_id}"
                }

                # --- Find desired photo size URL ---
                photo_url = None
                try:
                    sizes = flickr.photos.getSizes(photo_id=photo_id)
                    available_sizes = {s['label']: s['source'] for s in sizes['sizes']['size']}
                    metadata['available_sizes'] = available_sizes # Add sizes info to metadata

                    # Prioritize sizes: X-Large, 2048, 1600, 1024, Original, Large
                    size_priority = [X_LARGE_SIZE_LABEL, 'Large 2048', 'Large 1600', 'Large', 'Original']
                    for label in size_priority:
                        if label in available_sizes:
                            photo_url = available_sizes[label]
                            print(f"Found '{label}' size URL.")
                            break
                    if not photo_url:
                        # Fallback to largest available if specific labels not found
                        largest_size = sizes['sizes']['size'][-1] # Assume last is largest
                        photo_url = largest_size['source']
                        print(f"Desired sizes not found. Falling back to largest available: '{largest_size['label']}'.")

                except flickrapi.exceptions.FlickrError as e:
                    print(f"Error getting sizes for photo {photo_id}: {e}")
                    metadata['download_error'] = f"Could not get sizes: {e}"
                    photos_failed += 1
                except Exception as e:
                     print(f"Unexpected error getting sizes for photo {photo_id}: {e}")
                     metadata['download_error'] = f"Unexpected error getting sizes: {e}"
                     photos_failed += 1


                # Save metadata regardless of download success
                metadata_filepath = user_output_dir / f"{base_filename}_metadata.json"
                save_metadata(metadata, metadata_filepath)

                # Download the photo if URL was found
                if photo_url:
                    # Determine file extension
                    file_extension = Path(requests.utils.urlparse(photo_url).path).suffix or '.jpg' # Default to .jpg if no extension
                    photo_filepath = user_output_dir / f"{base_filename}{file_extension}"

                    if download_photo(photo_url, photo_filepath):
                        photos_downloaded += 1
                    else:
                        photos_failed += 1
                        metadata['download_error'] = metadata.get('download_error', '') + " Download failed."
                        # Re-save metadata with download error
                        save_metadata(metadata, metadata_filepath)
                else:
                    print(f"Could not find suitable download URL for photo {photo_id}.")
                    photos_failed += 1


                # Respect Flickr API usage limits
                time.sleep(1) # Add a small delay between API calls

            page += 1

        except flickrapi.exceptions.FlickrError as e:
            print(f"Error fetching photos page {page}: {e}")
            # Consider adding retry logic or stopping
            break # Stop processing if a page fetch fails
        except Exception as e:
            print(f"Unexpected error fetching photos page {page}: {e}")
            break

    print("--- Scraping Complete ---")
    print(f"Total photos processed: {photos_processed}")
    print(f"Photos downloaded successfully: {photos_downloaded}")
    print(f"Photos failed/skipped: {photos_failed}")
    print(f"Data saved in: {user_output_dir.resolve()}")

if __name__ == "__main__":
    main() 