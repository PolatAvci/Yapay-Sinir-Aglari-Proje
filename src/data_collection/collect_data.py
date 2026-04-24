import os
import csv
import youtube_api

def main():
    links_file = "src/data_collection/links.txt"
    output_directory = "data/raw/music"
    stats_file = "data/raw/video_statistics.csv"

    if not os.path.exists(links_file):
        print(f"Hata: '{links_file}' dosyası bulunamadı.")
        return

    with open(links_file, "r", encoding="utf-8") as file:
        links = [line.strip() for line in file.readlines() if line.strip()]

    if not links:
        print("Uyarı: links.txt dosyası boş!")
        return

    print(f"Toplam {len(links)} link okundu.")

    print("\n--- Müzik İndirme İşlemi Başlıyor ---")
    youtube_api.download_music(links, output_directory)
    print("Müzik indirme işlemi tamamlandı.")

    print("\n--- Metadata (İstatistik) Çekimi Başlıyor ---")
    video_ids = youtube_api.extract_multiple_youtube_video_ids(links)
    
    if not video_ids:
        print("Geçerli bir video ID'si çıkarılamadı.")
        return

    statistics = youtube_api.get_bulk_youtube_statistics(video_ids)

    header = ['video_id', 'viewCount', 'likeCount', 'favoriteCount', 'commentCount']

    try:
        with open(stats_file, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=header)
            
            writer.writeheader()
            
            for vid_id, stats in statistics.items():
                row = {'video_id': vid_id}
                row.update(stats)
                
                # Only include keys that are in the header
                filtered_row = {key: row.get(key, 0) for key in header}
                writer.writerow(filtered_row)
        
        print(f"\nBaşarılı! Tüm istatistikler '{stats_file}' dosyasına CSV olarak kaydedildi.")
    
    except Exception as e:
        print(f"CSV yazılırken bir hata oluştu: {e}")

if __name__ == "__main__":
    main()