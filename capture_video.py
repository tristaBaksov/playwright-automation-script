import argparse
import csv

from playwright.sync_api import sync_playwright

from qscript import CaptureVideo_Magento
from video_client import UploadVideo

def parse_args():
    parser = argparse.ArgumentParser(description="Record, upload and preview videos.")
    parser.add_argument("--server", help="Web service URL, e.g. http://127.0.0.1:8000")
    parser.add_argument(
        "--view-seconds",
        type=float,
        default=5,
        help="Preview time in seconds; 0 keeps the browser open until Enter is pressed"
    )
    return parser.parse_args()

def PreviewVideo(video_url, view_seconds):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(video_url)

        if view_seconds > 0:
            page.wait_for_timeout(view_seconds*1000)
        else:
            input("Press Enter to close the preview...")

        browser.close()

def main():
    args = parse_args()

    with open("input.csv", "r", encoding="utf-8", newline="") as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')

        for row in csv_reader:
            company_name = row["Company Name"]
                
            path = CaptureVideo_Magento(
                row['URL'],
                company_name,
                row['Language'],
                row['Country'],
                row['Postcode'],
                row['City'],
                row['Street'],
                row['HouseNo']
            )
            print(f"Saved: {path}")

            if not args.server or path is None:
                continue

            try:
                video_url = UploadVideo(args.server, path, company_name)
                print(f"Uploaded: {video_url}")
                PreviewVideo(video_url, args.view_seconds)
            except Exception as e:
                print(f"Upload or preview failed for {company_name}: {e}")

if __name__ == "__main__":
    main()