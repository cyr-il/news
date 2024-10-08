from flask import Flask, jsonify, render_template
import requests
from flask_cors import CORS
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)
load_dotenv()


YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')


# Routes for YouTube videos
@app.route('/videos/<channel_name>')
def get_videos(channel_name):
    channel_id = get_channel_id(channel_name)
    if not channel_id:
        return jsonify({"error": "Channel not found"}), 404

    url = f'https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={channel_id}&part=snippet&order=date&maxResults=9'
    response = requests.get(url)
    data = response.json()

    videos = []
    if 'items' in data:
        for item in data['items']:
            details_url = f'https://www.googleapis.com/youtube/v3/videos?key={YOUTUBE_API_KEY}&id={item["id"]["videoId"]}&part=contentDetails'
            details_response = requests.get(details_url)
            details_data = details_response.json()
            print(details_data)
            video_info = {
                "title": item['snippet']['title'],
                "videoId": item['id']['videoId'],
                "description": item['snippet']['description'],
                "thumbnail": item['snippet']['thumbnails']['high']['url'],
                "publishedAt": item['snippet']['publishedAt'],
                "duration" : details_data['items'][0]['contentDetails']['duration'] if 'contentDetails' in details_data['items'][0] else ""
            }
            videos.append(video_info)

    return jsonify(videos)

# Helper function to get the channel ID based on the channel name
def get_channel_id(channel_name):
    channel_ids = {
        'vincent': 'UCTQQb3F6qDKXObGAE27HtVw',
        'anthony': 'UC0eA9hN3ho9kh7RwqCbExgQ',
    }
    return channel_ids.get(channel_name)

# Route for Tech Articles (using a fake API or News API)
@app.route('/tech-articles')
def get_tech_articles():
    url = f'https://newsapi.org/v2/top-headlines?category=technology&apiKey={NEWS_API_KEY}&pageSize=10&country=us'
    response = requests.get(url)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
