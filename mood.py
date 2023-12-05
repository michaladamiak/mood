import cv2
import base64
import requests
import json 
import spotipy 
import webbrowser

#taking the picture
cam = cv2.VideoCapture(0)
cv2.namedWindow("Mood")

while True:
    ret, frame = cam.read()
    
    if not ret:
        print("failed to grab frame")
        break
        
    cv2.imshow("test", frame)
    
    k = cv2.waitKey(1)
    
    if k%256 == 27:
        print("Closing the App")
        break
    elif k%256 == 32:
        img_name = "pic.png"
        cv2.imwrite(img_name, frame)
        
        #cropping image
        img = cv2.imread('pic.png')
        img = img[0:720, 280:1000]
        cv2.imwrite(img_name, img)
        
        print("Image taken")
        
        break
        
cam.release()
cv2.destroyAllWindows()
for i in range (1,5):
    cv2.waitKey(1)
    

    
#using OpenAI to get recommendation of song based on the mood from picture    
    
# OpenAI API Key
api_key = '' # enter your OpenAI API key

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')   
    
# Path to your image
image_path = "pic.png"

# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

payload = {
  "model": "gpt-4-vision-preview",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Your answer should be 20 tokens or less. What song would you recommend based on the mood of the pearson in the picture? Tell me only the name of the song and artist."
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
  "max_tokens": 40
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

print(response.json())


#playing song in spotify

username = '' # enter your Spotify username 
clientID = '' # enter your Spotify Web API clientID
clientSecret = '' # enter your Spotify Web API clientSecret
redirect_uri = 'http://google.com/callback/'
oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri) 
token_dict = oauth_object.get_access_token() 
token = token_dict['access_token'] 
spotifyObject = spotipy.Spotify(auth=token) 
user_name = spotifyObject.current_user() 
  
# To print the JSON response from  
# browser in a readable format. 
# optional can be removed 
print(json.dumps(user_name, sort_keys=True, indent=4)) 

search_song = f"{response.json()['choices'][0]['message']['content']}"
results = spotifyObject.search(search_song, 1, 0, "track") 
songs_dict = results['tracks'] 
song_items = songs_dict['items'] 
song = song_items[0]['external_urls']['spotify'] 
webbrowser.open(song) 
print('Song has opened in your browser.') 


