from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import requests

def home(request):
    if request.method == 'POST':
        video_link = request.POST.get('video_link')
        save_path = "/Users/khalid/Desktop/video.mp4"
        
        video_src = extract_video_src(video_link)
        if video_src:
            download_video(video_src, save_path)

    return render(request, 'app/home.html')

def extract_video_src(video_link):
    """Extracts the video source URL from the given Likee video link."""
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1")
    driver = webdriver.Chrome(options=options)
    driver.get(video_link)

    wait = WebDriverWait(driver, 10)  # Increase the timeout if necessary

    content_wrap = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".content-wrap")))
    video_src = content_wrap.find_element(By.CSS_SELECTOR, "video").get_attribute("src")
    driver.quit()

    return video_src

def download_video(video_src, save_path):
    """Downloads the video from the given source URL to the specified path."""
    response = requests.get(video_src, stream=True)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"Successfully downloaded video to {save_path}")
    else:
        print(f"Failed to download video from {video_src}")
