import os
import time
from playwright.sync_api import sync_playwright

cursor_init = """
(() => {
    // Создаём элемент курсора
    const cursor = document.createElement('div');
    cursor.id = "playwright-cursor";
    cursor.style.position = 'fixed';
    cursor.style.pointerEvents = 'none'; // чтобы курсор не мешал кликам
    cursor.style.zIndex = '1000'; 
    cursor.style.transition = 'transform 0.1s ease';

    // Добавляем элемент курсора в body
    cursor.innerHTML = `
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/>
    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17.93c-3.95.49-7.43-2.99-6.93-6.93.49-3.95 3.95-7.43 7.93-6.93C17.43 5.57 20.91 9.05 20.41 13c-.49 3.95-3.95 7.43-7.93 6.93Z12 4c-4.42 0-8 3.58-8 8s3.58 8 8 8c4.42 0 8-3.58 8-8s-3.58-8-8-8zm1 11h-2v-6h2v6z"/></svg>
    `;

    document.addEventListener('DOMContentLoaded', () => {
        document.body.appendChild(cursor);
    });

    // Слушаем движение мыши и двигаем SVG
    document.addEventListener('mousemove', (event) => {
        cursor.style.left = event.clientX + 'px';
        cursor.style.top = event.clientY + 'px';
    });

    // Эффект клик-рипла
    document.addEventListener('click', (event) => {
        const ripple = document.createElement('div');
        ripple.style.position = 'fixed';
        ripple.style.left = (event.clientX - 10) + 'px';
        ripple.style.top = (event.clientY - 10) + 'px';
        ripple.style.width = '20px';
        ripple.style.height = '20px';
        ripple.style.border = '2px solid rgba(0, 120, 255, 0.8)';
        ripple.style.borderRadius = '50%';
        ripple.style.pointerEvents = 'none';
        ripple.style.zIndex = '999';
        ripple.style.transition = 'all 0.4s ease-out';
        document.body.appendChild(ripple);

        setTimeout(() => {
            ripple.style.transform = 'scale(2.5)';
            ripple.style.opacity = '0';
        }, 10);

        setTimeout(() => ripple.remove(), 400);
    });
})();
"""

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
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        video_dir = os.environ.get('PATH_TO_VIDEO_DIR', './video')

        context = browser.new_context(
            record_video_dir=video_dir,
            record_video_size={"width": 1280, "height": 720}
        )

        context.add_init_script(cursor_init)
        
        page = context.new_page()

        page.goto(url)
        page.mouse.move(200, 200)

        search_box = page.locator("textarea[name='q']")
        search_box.wait_for()

        box = search_box.bounding_box()
        if box:
            center_x = box["x"] + box["width"] / 2
            center_y = box["y"] + box["height"] / 2
            page.mouse.move(center_x, center_y, steps=150)

        time.sleep(.9)
        search_box.click()
        time.sleep(.5)
        search_box.press_sequentially(f"Magento developer in {city}", delay=120)

        search_button = page.locator("button[type='button']").first
        search_button.wait_for()

        btn_box = search_button.bounding_box()
        if btn_box:
            center_x = btn_box["x"] + btn_box["width"] / 2
            center_y = btn_box["y"] + btn_box["height"] / 2
            page.mouse.move(center_x, center_y, steps=165)
            time.sleep(.8)
            search_button.click()
            search_box.press("Enter")
            

        page.wait_for_selector('a[data-testid="result-title-a"]', timeout=15000)

        first_result = page.locator('a[data-testid="result-title-a"]').first
        first_result.wait_for()

        res_box = first_result.bounding_box()
        if res_box:
            center_x = res_box["x"] + res_box["width"] / 2
            center_y = res_box["y"] + res_box["height"] / 2
            page.mouse.move(center_x, center_y, steps=145)
            time.sleep(1.2)
            first_result.click()

        time.sleep(5)