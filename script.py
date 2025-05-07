import requests
import pandas as pd
import time
import os

channel_id = 'UCXRqdYwNwa0ZGxScFaUnStg'
API_KEY = os.getenv("YOUTUBE_API_KEY")

search_url = 'https://www.googleapis.com/youtube/v3/search'
video_ids = []
next_page_token = None
max_results = 500  # 取得上限（任意）
fetched = 0

# ページネーション対応
while True:
    params = {
        'key': API_KEY,
        'part': 'id',
        'channelId': channel_id,
        'order': 'date',
        'type': 'video',
        'maxResults': 50,
    }
    if next_page_token:
        params['pageToken'] = next_page_token

    res = requests.get(search_url, params=params).json()

    for item in res.get('items', []):
        video_id = item['id'].get('videoId')
        if video_id:
            video_ids.append(video_id)
            fetched += 1
            if fetched >= max_results:
                break

    next_page_token = res.get('nextPageToken')
    if not next_page_token or fetched >= max_results:
        break

    time.sleep(1)  # API制限対策

# 複数回に分けて video 情報取得（50件ずつ）
videos_url = 'https://www.googleapis.com/youtube/v3/videos'
video_data = []

for i in range(0, len(video_ids), 50):
    batch_ids = video_ids[i:i + 50]
    params = {
        'key': API_KEY,
        'part': 'snippet,statistics',
        'id': ','.join(batch_ids),
    }
    res = requests.get(videos_url, params=params).json()

    for item in res.get('items', []):
        video_data.append({
            'タイトル': item['snippet']['title'],
            '投稿日': item['snippet']['publishedAt'][:10],
            '再生数': int(item['statistics'].get('viewCount', 0))
        })

df = pd.DataFrame(video_data)
df['投稿日'] = pd.to_datetime(df['投稿日'])
df = df.sort_values(by='投稿日')

# 結果
print(f'取得動画数: {len(df)} 件')
print(df)
