import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs
import yt_dlp

# Load environment variables from .env file (looks for .env in the root directory)
load_dotenv()

# Securely fetch the API key
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

if not YOUTUBE_API_KEY:
    raise ValueError("YOUTUBE_API_KEY not found! Please check your .env file.")

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def get_youtube_view_count(artist, song):
    try:
        search_query = f"{artist} {song} official audio"
        
        search_request = youtube.search().list(
            q=search_query,
            part='id',
            type='video',
            maxResults=1
        )
        search_response = search_request.execute()
        
        if not search_response.get('items'):
            print("No video found.")
            return None
            
        video_id = search_response['items'][0]['id']['videoId']
        
        statistics_request = youtube.videos().list(
            part='statistics',
            id=video_id
        )
        statistics_response = statistics_request.execute()
        
        # Sadece viewCount yerine tüm statistics objesini döndürüyoruz
        statistics = statistics_response['items'][0].get('statistics', {})
        
        return statistics

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_bulk_youtube_statistics(video_ids):
    """
    Fetches all statistics for a list of YouTube video IDs in bulk.
    Automatically handles the API limit of 50 IDs per request.
    """
    video_statistics = {}
    
    # Split the video_ids list into chunks of 50
    for i in range(0, len(video_ids), 50):
        chunk = video_ids[i:i + 50]
        ids_string = ','.join(chunk)
        
        try:
            request = youtube.videos().list(
                part='statistics',
                id=ids_string
            )
            response = request.execute()
            
            # Map each video ID to its full statistics dictionary
            for item in response.get('items', []):
                vid_id = item['id']
                stats = item.get('statistics', {})
                video_statistics[vid_id] = stats
                
        except Exception as e:
            print(f"An error occurred while fetching a chunk: {e}")
            
    return video_statistics

def extract_youtube_video_id(url):
    """
    Verilen YouTube URL'sinden video ID'sini güvenli bir şekilde çıkarır.
    Süre (&t=), oynatma listesi (&list=) gibi ekstra parametreleri yoksayar.
    """
    parsed_url = urlparse(url)
    
    # Standart youtube.com formatları için
    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        # https://www.youtube.com/watch?v=ID formatı
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query).get('v', [None])[0]
        # https://www.youtube.com/embed/ID formatı
        elif parsed_url.path.startswith(('/embed/', '/v/')):
            return parsed_url.path.split('/')[2]
            
    # Kısa youtu.be formatları için (örn: https://youtu.be/ID?t=10)
    elif parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:] # Baştaki '/' işaretini atlar
        
    return None

def extract_multiple_youtube_video_ids(url_list, include_none=False):
    """
    Processes a list of YouTube URLs and returns only the valid video IDs.
    Broken or invalid URLs (returning None) are filtered out from the result list.
    """
    # Her bir URL'yi fonksiyona gönderiyoruz ve sadece geçerli (None olmayan) sonuçları listeye ekliyoruz
    return [
        extract_youtube_video_id(url) 
        for url in url_list 
        if include_none or extract_youtube_video_id(url) is not None
    ]

def download_music(link_list, output_dir):
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{output_dir}/%(id)s-%(title)s.%(ext)s',
        'quiet': False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download(link_list)
        except Exception as e:
            print(f"Bir hata oluştu: {e}")
