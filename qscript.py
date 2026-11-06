import os
from playwright.sync_api import sync_playwright

cursor_init = """
(() => {
    const cursor = document.createElement('div');
    cursor.id = "playwright-cursor";
    cursor.style.position = 'fixed';
    cursor.style.pointerEvents = 'none'; // чтобы курсор не мешал кликам
    cursor.style.zIndex = '2147483647'; 

    const highlight = document.createElement('div');
    highlight.id = "playwright-highlight";
    highlight.style.position = 'fixed';
    highlight.style.left = '-100px';
    highlight.style.top = '-100px';
    highlight.style.width = '64px';
    highlight.style.height = '64px';
    highlight.style.borderRadius = '50%';
    highlight.style.backgroundColor = 'rgba(255, 230, 0, 0.45)';
    highlight.style.transform = 'translate(-50%, -50%)';
    highlight.style.pointerEvents = 'none';
    highlight.style.zIndex = '2147483645'; 
    cursor.innerHTML = `
    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 6.4 20 20" style="display:block">
    <path fill="#ffffff" d="M6.56 25.48c-0.32 0-0.64-0.2-0.76-0.52l-1.8-4.28-2.84 1.12c-0.24 0.12-0.56 0.080-0.8-0.080s-0.36-0.4-0.36-0.68v-13.68c0-0.32 0.2-0.64 0.52-0.76s0.68-0.040 0.92 0.2l9.68 9.68c0.2 0.2 0.28 0.48 0.24 0.76s-0.24 0.52-0.48 0.6l-2.8 1.2 1.76 4.28c0.16 0.44-0.040 0.92-0.44 1.080l-2.48 1.040c-0.16 0.040-0.24 0.040-0.36 0.040z"/>
    <path fill="#000000" d="M6.56 25.48c-0.32 0-0.64-0.2-0.76-0.52l-1.8-4.28-2.84 1.12c-0.24 0.12-0.56 0.080-0.8-0.080s-0.36-0.4-0.36-0.68v-13.68c0-0.32 0.2-0.64 0.52-0.76s0.68-0.040 0.92 0.2l9.68 9.68c0.2 0.2 0.28 0.48 0.24 0.76s-0.24 0.52-0.48 0.6l-2.8 1.2 1.76 4.28c0.16 0.44-0.040 0.92-0.44 1.080l-2.48 1.040c-0.16 0.040-0.24 0.040-0.36 0.040zM4.48 18.76c0.32 0 0.64 0.2 0.76 0.52l1.76 4.28 0.92-0.4-1.76-4.28c-0.16-0.44 0.040-0.92 0.44-1.080l2.44-1.040-7.36-7.36v10.44l2.48-1c0.080-0.040 0.2-0.080 0.32-0.080z"/>
    </svg>
    `;

    document.addEventListener('DOMContentLoaded', () => {
        document.body.appendChild(cursor);
        document.body.appendChild(highlight);
    });

    // Слушаем движение мыши и двигаем SVG
    document.addEventListener('mousemove', (event) => {
        cursor.style.left = event.clientX + 'px';
        cursor.style.top = event.clientY + 'px';
        highlight.style.left = event.clientX + 'px';
        highlight.style.top = event.clientY + 'px';
    });

    document.addEventListener('mousedown', (event) => {
        const ripple = document.createElement('div');
        ripple.style.position = 'fixed';
        ripple.style.left = (event.clientX - 10) + 'px';
        ripple.style.top = (event.clientY - 10) + 'px';
        ripple.style.width = '20px';
        ripple.style.height = '20px';
        ripple.style.border = '2px solid rgba(0, 120, 255, 0.8)';
        ripple.style.borderRadius = '50%';
        ripple.style.pointerEvents = 'none';
        ripple.style.zIndex = '2147483646';
        ripple.style.transition = 'all 0.4s ease-out';
        document.body.appendChild(ripple);

        setTimeout(() => {
            ripple.style.transform = 'scale(1.6)';
            ripple.style.opacity = '0';
        }, 10);

        setTimeout(() => ripple.remove(), 400);
    }, true);

    window.ShowCallout = (text, bgColor = '#ffee00', textColor = '#000000', fade = true) => {
        const fadeMs = fade ? 2000 : 0;
        const holdMs = 1500;

        const callout = document.createElement('div');
        callout.textContent = text;
        callout.style.position = 'fixed';
        callout.style.left = '50%';
        callout.style.top = '80px';
        callout.style.transform = 'translateX(-50%)';
        callout.style.width = 'max-content';
        callout.style.maxWidth = '90vw';
        callout.style.padding = '10px 22px';
        callout.style.background = bgColor;
        callout.style.color = textColor;
        callout.style.font = '16pt Arial, sans-serif';
        callout.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.3)';
        callout.style.pointerEvents = 'none';
        callout.style.zIndex = '2147483644';
        callout.style.opacity = fade ? '0' : '1';
        callout.style.transition = `opacity ${fadeMs}ms ease`;
        document.body.appendChild(callout);

        return new Promise((resolve) => {
            callout.getBoundingClientRect();
            callout.style.opacity = '1';

            setTimeout(() => {
                callout.style.opacity = '0';
                setTimeout(() => {
                    callout.remove();
                    resolve();
                }, fadeMs);
            }, fadeMs + holdMs);
        });
    }
})();
"""

PATH_TO_VIDEO_FOLDER = "./video"

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
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            
            with browser.new_context(
                record_video_dir=PATH_TO_VIDEO_FOLDER,
                record_video_size={"width": 1280, "height": 720}
            ) as context:

                context.add_init_script(cursor_init)
                
                page = context.new_page()

                video = page.video

                page.goto(url)
                page.mouse.move(200, 200)

                search_box = page.locator("textarea[name='q']")
                search_box.wait_for()
                page.evaluate("text => window.ShowCallout(text)", "Test text")

                box = search_box.bounding_box()
                if box:
                    center_x = box["x"] + box["width"] / 2
                    center_y = box["y"] + box["height"] / 2
                    page.mouse.move(center_x, center_y, steps=150)

                page.wait_for_timeout(900)
                search_box.click()
                page.wait_for_timeout(500)
                search_box.press_sequentially(f"Magento developer in {city}", delay=120)

                search_button = page.locator("form button[type='submit']:visible")
                search_button.wait_for(state="visible")
                page.wait_for_timeout(1000)

                btn_box = search_button.bounding_box()
                if btn_box:
                    center_x = btn_box["x"] + btn_box["width"] / 2
                    center_y = btn_box["y"] + btn_box["height"] / 2
                    page.mouse.move(center_x, center_y, steps=150)
                    page.wait_for_timeout(900)
                    search_button.click(delay=300)
                    

                page.wait_for_selector('a[data-testid="result-title-a"]', timeout=30000)

                first_result = page.locator('a[data-testid="result-title-a"]').first
                first_result.wait_for()

                res_box = first_result.bounding_box()
                if res_box:
                    center_x = res_box["x"] + res_box["width"] / 2
                    center_y = res_box["y"] + res_box["height"] / 2
                    page.mouse.move(center_x, center_y, steps=145)
                    page.wait_for_timeout(1200)
                    with page.expect_navigation(wait_until="domcontentloaded"):
                        first_result.click(delay=300)

                    page.wait_for_timeout(1000)
                    page.mouse.move(center_x + 40, center_y + 40, steps=20)
                    page.wait_for_timeout(4000)

            target = os.path.join(PATH_TO_VIDEO_FOLDER, f"{company_name}.webm")
            os.replace(video.path(), target)
            browser.close()
            return os.path.abspath(target)           

    except Exception as e:
        print(f"Error for {company_name}: {e}")
        return None 