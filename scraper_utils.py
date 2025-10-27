import re
import time
import random
from selenium.webdriver.common.by import By

def is_real_image(url: str) -> bool:
    if not url:
        return False
    valid_exts = (".jpg", ".jpeg", ".webp")
    url = url.lower()
    if not url.endswith(valid_exts):
        return False
    # Exclude archive thumbnails and icons
    if any(ext in url for ext in [".rar.", ".zip.", ".7z.", ".ico"]):
        return False
    return True

def scrape_page(driver):
    posts_data = []
    posts = driver.find_elements(By.CSS_SELECTOR, "article.message[data-author]")

    for idx, post in enumerate(posts, start=1):
        # --- Expand spoilers and "click to expand" ---
        toggles = post.find_elements(By.CSS_SELECTOR, ".bbCodeBlock--spoiler button, .spoiler-title, .js-expandLink")
        for t in toggles:
            try:
                driver.execute_script("arguments[0].click();", t)
                time.sleep(0.2)  # small delay to let DOM update
            except:
                pass

        # --- Post title (first line of body) ---
        try:
            title = post.find_element(By.CSS_SELECTOR, ".message-body, .bbWrapper").text.splitlines()[0].strip()
        except:
            title = ""

        try:
            post_number = post.find_element(By.XPATH,".//a[starts-with(normalize-space(.), '#')]").text.strip()
        except:
            continue

        post_number_clean = re.sub(r"[#,]", "", post_number)

        # --- Post date ---
        try:
            date = post.find_element(By.CSS_SELECTOR, "time, .message-attribution time").text.strip()
        except:
            date = ""

        # --- Collect all image URLs ---
        imgs = [img.get_attribute("src") for img in post.find_elements(By.TAG_NAME, "img") if is_real_image(img.get_attribute("src"))]
        imgs += [a.get_attribute("href") for a in post.find_elements(By.TAG_NAME, "a") if is_real_image(a.get_attribute("href"))]
        imgs = list(set(imgs))  # deduplicate

        # --- If more than 4 images, pick 3 random ones ---
        sample_imgs = []
        if len(imgs) > 4:
            sample_imgs = random.sample(imgs, 3)
        else:
            sample_imgs = imgs

        # --- Collect all external links (skip internal forum links) ---
        links = [a.get_attribute("href") for a in post.find_elements(By.TAG_NAME, "a") if a.get_attribute("href")]
        external_links = [l for l in links if not re.search(r"simpcity|#|javascript", l, re.I) and not ("jpg6.su" in l and "/img/" in l) and not ("jpg7.cr" in l and "/img/" in l) ]

        posts_data.append({
            "post_number": post_number_clean,
            "date": date,
            "title": title,
            "sample_images": sample_imgs,
            "external_links": external_links
        })
    return posts_data
