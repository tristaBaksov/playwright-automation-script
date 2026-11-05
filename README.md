# CSV-driven Browser Automation Video Recorder

A Python and Playwright tool that records a browser automation video for each row of `input.csv`.
For every row it opens DuckDuckGo, types a query with the city name, runs the search,
and opens the first result.

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

## Files

- `capture_video.py` reads `input.csv` and calls the recording function for each row.
- `qscript.py` contains `CaptureVideo_Magento(...)`, the `PATH_TO_VIDEO_FOLDER` variable,
  and the injected JavaScript: SVG cursor, yellow highlight, click ripple, and `ShowCallout`.
- `input.csv` contains sample input data.

## Branches

- `dev` matches the behavior of the example video: it clicks the search mode toggle,
  then presses Enter in the search box.
- `master` clicks the real search button, as described in the task.

The mode toggle does not start a search by itself because it is outside the search form.
That is why `dev` submits the form with Enter.

## Notes

- The browser runs with `headless=False`: in headless mode, DuckDuckGo returned a 418 error page
  instead of search results.
- Playwright does not record the OS cursor, so a custom cursor is injected with `add_init_script`.
- Tested on Windows 11 with Python 3.14 and Playwright 1.64.1.
