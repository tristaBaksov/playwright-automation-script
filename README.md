# CSV-driven Browser Automation Video Recorder

A Python and Playwright tool that records a browser automation video for each row of `input.csv`.
For every row it opens DuckDuckGo, types a query with the city name, runs the search,
and opens the first result.

An optional Flask web service stores the recorded videos, looks them up by company name,
and serves them for preview in a browser.

## Installation

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

## Usage

```bash
python capture_video.py
```

Videos are saved to `video/<company_name>.webm`, and the path is printed to the console.

## Web service

Start the service in a separate terminal:

```bash
python web_service.py
```

It listens on `0.0.0.0:8000` by default. Use the `FLASK_HOST` and `FLASK_PORT` environment
variables to change this. On first start it creates `videos.db` and the `uploads/` folder.

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/upload` | Upload a video and return its URL |
| GET | `/get_video_url?company_name=<name>` | Return the video URL, or 404 if not found |
| GET | `/media/<filename>` | Serve an uploaded video |
| GET | `/videos` | List all records |

To record, upload, and preview each video, keep the service running and use:

```bash
python capture_video.py --server http://127.0.0.1:8000 --view-seconds 5
```

`--view-seconds 0` keeps the preview open until Enter is pressed.
A failed upload or preview is logged, and processing continues with the next row.

## Files

- `capture_video.py` reads `input.csv`, calls the recording function for each row,
  and uploads and previews each video when `--server` is set.
- `web_service.py` contains the Flask service and the SQLite database layer.
- `video_client.py` contains the `UploadVideo` and `GetVideoURL` client functions.
- `qscript.py` contains `CaptureVideo_Magento(...)`, the `PATH_TO_VIDEO_FOLDER` variable,
  and the injected JavaScript: SVG cursor, yellow highlight, click ripple, and `ShowCallout`.
- `input.csv` contains sample input data.

## Branches

- `dev` matches the behavior of the example video: it clicks the search mode toggle,
  then presses Enter in the search box.
- `master` clicks the real search button, as described in the task.

The mode toggle does not start a search by itself because it is outside the search form.
That is why `dev` submits the form with Enter. The `dev` branch contains the recorder only,
without the web service.

## Notes

- The browser runs with `headless=False`: in headless mode, DuckDuckGo returned a 418 error page
  instead of search results.
- Playwright does not record the OS cursor, so a custom cursor is injected with `add_init_script`.
- Tested on Windows 11 with Python 3.14 and Playwright 1.64.1.
