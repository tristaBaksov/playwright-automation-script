import os 

def UploadVideo(server_url: str, video_path: str, company_name: str) -> str:
    """Uploads a video file to the server and returns its URL."""
    
    import requests

    with open(video_path, "rb") as video_file:
        response = requests.post(
            f"{server_url.rstrip('/')}/upload",
            files={"file": (os.path.basename(video_path), video_file)},
            data={"company_name": company_name},
            timeout=120,
        )

    response.raise_for_status()
    return response.json()["video_url"]

def GetVideoURL(server_url: str, company_name: str) -> str:
    """Returns the video URL for the given company name."""
    
    import requests
    
    response = requests.get(
        f"{server_url.rstrip('/')}/get_video_url",
        params={"company_name": company_name},
        timeout=30,
    )

    response.raise_for_status()
    return response.json()["video_url"]