import os
import csv
from urllib.parse import urlparse, parse_qs
import youtube_api


def main():
    links_file = "src/data_collection/music_links.txt"
    playlist_file = "src/data_collection/playlist_links.txt"
    output_directory = "data/raw/music"
    stats_file = "data/raw/music_statistics.csv"

    links = []
    if os.path.exists(links_file):
        with open(links_file, "r", encoding="utf-8") as file:
            links = [line.strip() for line in file.readlines() if line.strip()]

    if not links:
        print(f"Uyarı: '{links_file}' boş veya bulunamadı. Playlist dosyası kontrol ediliyor...")
        
        if not os.path.exists(playlist_file):
            print(f"Hata: '{playlist_file}' dosyası da bulunamadı! Lütfen işlem yapabilmek için link ekleyin.")
            return
            
        with open(playlist_file, "r", encoding="utf-8") as file:
            playlist_urls = [line.strip() for line in file.readlines() if line.strip()]
            
        if not playlist_urls:
            print(f"Hata: '{playlist_file}' dosyası da boş! Çekilecek veri yok.")
            return
            
        print(f"Toplam {len(playlist_urls)} playlist bulundu. Şarkı linkleri toplanıyor...")
        
        all_links = []
        for purl in playlist_urls:
            pid = youtube_api.extract_playlist_id(purl)
            if pid:
                print(f"İşleniyor (Playlist ID): {pid}")
                pl_links = youtube_api.get_playlist_video_ids(pid)
                all_links.extend(pl_links)
        
        # For uniqueness
        links = list(set(all_links))
        
        if not links:
            print("Playlistlerden geçerli hiçbir şarkı linki çıkarılamadı.")
            return
            
        # If directory doesn't exist, create it and save the links
        os.makedirs(os.path.dirname(links_file), exist_ok=True)
        with open(links_file, "w", encoding="utf-8") as file:
            for link in links:
                file.write(f"{link}\n")
                
        print(f"Başarılı! Toplam {len(links)} adet benzersiz link otomatik olarak '{links_file}' dosyasına kaydedildi.")

    print(f"\nİşleme alınacak toplam link sayısı: {len(links)}")

    print("\n--- Müzik İndirme İşlemi Başlıyor ---")
    youtube_api.download_music(links, output_directory)
    print("Müzik indirme işlemi tamamlandı.")

    print("\n--- Metadata (İstatistik) Çekimi Başlıyor ---")
    video_ids = youtube_api.extract_multiple_youtube_video_ids(links)
    
    if not video_ids:
        print("Geçerli bir video ID'si çıkarılamadı.")
        return

    statistics = youtube_api.get_bulk_youtube_statistics(video_ids)

    header = ['video_id', 'viewCount', 'likeCount', 'favoriteCount', 'commentCount', 'publishedAt', 'duration']

    try:
        os.makedirs(os.path.dirname(stats_file), exist_ok=True)
        
        with open(stats_file, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=header)
            
            writer.writeheader()
            
            for vid_id, stats in statistics.items():
                row = {'video_id': vid_id}
                row.update(stats)
                
                # Add only the keys that are in the header, missing keys will default to 0
                filtered_row = {key: row.get(key, 0) for key in header}
                writer.writerow(filtered_row)
        
        print(f"\nBaşarılı! Tüm istatistikler '{stats_file}' dosyasına CSV olarak kaydedildi.")
    
    except Exception as e:
        print(f"CSV yazılırken bir hata oluştu: {e}")

if __name__ == "__main__":
    main()