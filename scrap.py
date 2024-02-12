import requests
import math
import pandas as pd
import json
import time
import os
import re




# extract information from each post node
def extract_post_info(post_node):
    post_info = {
        'post_id': post_node.get('id'),
        'display_url': post_node.get('display_url'),
        'is_video': post_node.get('__typename') == 'GraphVideo',
        'video_url': post_node.get('video_url') if post_node.get('is_video') else None,
        'dimensions': f"{post_node.get('dimensions', {}).get('height')}x{post_node.get('dimensions', {}).get('width')}",
        'caption': '',
        'comments_count': post_node.get('edge_media_to_comment', {}).get('count', 0),
        'likes_count': post_node.get('edge_media_preview_like', {}).get('count', 0),
        'video_view_count': post_node.get('video_view_count') if post_node.get('is_video') else None,
        'taken_at_timestamp': post_node.get('taken_at_timestamp'),
        'shortcode': post_node.get('shortcode'),
        'thumbnail_url': post_node.get('thumbnail_src'),
        'tracking_token': post_node.get('tracking_token'),
        'display_resources': [res.get('src') for res in post_node.get('display_resources', [])],
        'carousel_media_urls': [],  # store information from edge_sidecar_to_children
        'end_cursor': '',
        'relevant_comments': []
    }
    
    # Extract caption 
    caption_edges = post_node.get('edge_media_to_caption', {}).get('edges', [])
    if caption_edges:
        post_info['caption'] = caption_edges[0].get('node', {}).get('text', '')
    
    # Extract end cursor 
    if 'edge_media_to_comment' in post_node and 'page_info' in post_node['edge_media_to_comment']:
        post_info['end_cursor'] = post_node['edge_media_to_comment']['page_info'].get('end_cursor', '')

    if 'edge_sidecar_to_children' in post_node:
        for edge in post_node['edge_sidecar_to_children']['edges']:
            node = edge['node']
            urls = [res.get('src') for res in node.get('display_resources', [])]
            post_info['carousel_media_urls'].extend(urls)  # Append URLs to the list

    # Extract relevant comments 
    comments_edges = post_node.get('edge_media_to_comment', {}).get('edges', [])
    for comment in comments_edges[:5]:  # Adjust the number to get all relevent comments
        comment_info = {
            'comment_id': comment['node'].get('id'),
            'text': comment['node'].get('text'),
            'created_at': comment['node'].get('created_at'),
            'username': comment['node']['owner'].get('username')
        }
        post_info['relevant_comments'].append(comment_info)

    return post_info


#  fetch posts from the API
def fetch_posts(cursor=None):
    task_params = {
        'username': username, #Change to fetch another user
        'target': 'instagram_graphql_user_posts',
        'locale': 'en-us',
        'count': 50,  # API's limit
        'geo': 'United States'
    }

    if cursor:
        task_params['cursor'] = cursor

    response = requests.post(
        'https://scraper-api.smartproxy.com/v2/scrape',
        headers=headers,
        json=task_params,
        auth=(userapi, password)
    )

    print("API Response:", response.text)  # Print the raw API response

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None
    
# handle the API request with retry logic
def make_api_request(cursor=None, retries=3, delay=2):
    for attempt in range(retries):
        response = fetch_posts(cursor)
        if response:
            return response
        else:
            print(f"Retry {attempt + 1}/{retries} after delay...")
            time.sleep(delay)  # Delay between retries
    return None  # Return None if all retries fail


def extract_highest_resolution_url(urls):
    highest_resolution_url = None
    max_resolution = 0

    for url in urls:
        resolution_match = re.search(r'p(\d+)x(\d+)', url)
        if resolution_match:
            resolution = int(resolution_match.group(1)) * int(resolution_match.group(2))
            if resolution > max_resolution:
                highest_resolution_url = url
                max_resolution = resolution

    return highest_resolution_url

def group_urls_by_image(urls):
    grouped_urls = {}
    for url in urls:
        # Extract the base part of the URL (ignoring resolution and other parameters)
        base_url = re.sub(r'p\d+x\d+_', '', url.split('?')[0])
        if base_url not in grouped_urls:
            grouped_urls[base_url] = []
        grouped_urls[base_url].append(url)
    return grouped_urls

def download_images(post_info, directory='instagram_images'):
    if not os.path.exists(directory):
        os.makedirs(directory)

    post_id = post_info['post_id']
    image_counter = 1

    if post_info.get('carousel_media_urls'):
        grouped_urls = group_urls_by_image(post_info['carousel_media_urls'])
        for urls in grouped_urls.values():
            highest_res_url = extract_highest_resolution_url(urls)
            if highest_res_url:
                try:
                    response = requests.get(highest_res_url)
                    response.raise_for_status()
                    filename = f"{post_id}_{image_counter}.jpg"
                    file_path = os.path.join(directory, filename)
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Image saved as {filename}")
                    image_counter += 1
                except requests.exceptions.RequestException as e:
                    print(f"Error downloading image from post {post_id}: {e}")
    else:
        display_url = post_info.get('display_url')
        if display_url:
            try:
                response = requests.get(display_url)
                response.raise_for_status()
                filename = f"{post_id}_{image_counter}.jpg"
                file_path = os.path.join(directory, filename)
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f"Image saved as {filename}")
            except requests.exceptions.RequestException as e:
                print(f"Error downloading image from post {post_id}: {e}")

# Put all the username you want to scrap here 
usernames = ['cartier','tiffanyandco','vancleefarpels','bulgari','rolex','omega','tagheuer','jaegerlecoultre','tissot_official','longines']

# Initial setup
headers = {
    'Content-Type': 'application/json'
}

#Replace your api here 
userapi = ''
password = ''

for username in usernames:
    brand_dir = f'Results/{username}'
    image_dir = f'{brand_dir}/images'
    if not os.path.exists(brand_dir):
        os.makedirs(brand_dir)
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    
    # First API call to fetch initial data
    initial_data = fetch_posts()
    if not initial_data or 'results' not in initial_data or not initial_data['results']:
        raise ValueError("Initial data fetch failed, 'results' not in response, or 'results' is empty")

    if 'content' not in initial_data['results'][0] or 'data' not in initial_data['results'][0]['content']:
        raise ValueError("Content or Data not found in results")

    user_data = initial_data['results'][0]['content']['data']['user']
    if 'edge_owner_to_timeline_media' not in user_data:
        raise ValueError("'edge_owner_to_timeline_media' not found in user data")

    total_posts = user_data['edge_owner_to_timeline_media'].get('count', 0)
    if not total_posts:
        raise ValueError("Total posts count not found")

    total_requests = math.ceil(total_posts / 50)
    all_posts_info = []
    current_cursor = None


    # Fetch all posts and process them
    for _ in range(total_requests):
        data = make_api_request(cursor=current_cursor, retries=3, delay=2)
        if data and 'results' in data and data['results']:
            user_data = data['results'][0]['content']['data']['user']
            if 'edge_owner_to_timeline_media' in user_data:
                posts = user_data['edge_owner_to_timeline_media'].get('edges', [])
                for edge in posts:
                    node = edge.get('node')
                    if node:
                        post_info = extract_post_info(node)
                        all_posts_info.append(post_info)
                current_cursor = user_data['edge_owner_to_timeline_media'].get('page_info', {}).get('end_cursor')
            else:
                print("Warning: 'edge_owner_to_timeline_media' not found in user data")
                break
        else:
            print("Failed to fetch data after retries. Exiting loop.")
            break
        time.sleep(2)  # Wait for 2 seconds bypass the limit 

    df = pd.DataFrame(all_posts_info)
    for index, row in df.iterrows():
        download_images(row, image_dir)
    df.to_csv(f'{brand_dir}/{username}_posts.csv', index=False)