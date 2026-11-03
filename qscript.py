from playwright.sync_api import sync_playwright

def CaptureVideo_Magento(
        url: str,
        company_name: str,
        language: str,
        country: str,
        postcode: str,
        city: str,
        street: str,
        house_no: str
):
    with sync_plawright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)
        browser.close()