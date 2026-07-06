import os
import re
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

images = {
    "kgl": "https://upload.wikimedia.org/wikipedia/commons/c/cb/Vishansar_Lake.jpg",
    "golden_triangle": "https://upload.wikimedia.org/wikipedia/commons/1/1d/Taj_Mahal_%28Edited%29.jpeg",
    "tarsar": "https://upload.wikimedia.org/wikipedia/commons/5/55/Tarsar_lake_Aru.jpg",
    "rajasthan": "https://upload.wikimedia.org/wikipedia/commons/9/9a/1996_-218-20A_Jodhpur_Hotel_Umaid_Bhawan_Palace_%282233393509%29.jpg",
    "kerala": "https://upload.wikimedia.org/wikipedia/commons/e/ee/House_Boat_DSW.jpg",
    "india": "https://upload.wikimedia.org/wikipedia/commons/7/75/India_Gate_%28All_India_War_Memorial%29.jpg"
}

# Download images
os.makedirs("images/blog_new", exist_ok=True)
for key, url in images.items():
    ext = url.split('.')[-1].split('&')[0]
    filepath = f"images/blog_new/{key}.{ext}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, context=ctx)
        with open(filepath, 'wb') as f:
            f.write(response.read())
        images[key] = filepath
    except Exception as e:
        print(f"Failed to download {url}: {e}")

# HTML File replacements
blog_data = {
    "blog-kgl-trek.html": {
        "old_title_pattern": r"<h3>The Ultimate Guide to the Kashmir Great Lakes Trek: What to Expect</h3>",
        "new_title": "<h3>Kashmir Great Lakes Trek Itinerary: The Most Beautiful Trek in India</h3>",
        "h1_pattern": r"<h1>The Ultimate Guide to the Kashmir Great Lakes Trek</h1>",
        "new_h1": "<h1>Kashmir Great Lakes Trek Itinerary: The Most Beautiful Trek in India</h1>",
        "meta_pattern": r"<div class=\"article-meta\">Trekking Guide • Published July 2026</div>",
        "new_meta": "<div class=\"article-meta\">Trekking Guide • 15 Min Read</div>",
        "card_meta_pattern": r"<div class=\"blog-meta\">Trekking • \d+ Min Read</div>",
        "new_card_meta": "<div class=\"blog-meta\">Trekking • 15 Min Read</div>",
        "img_key": "kgl",
        "old_img": "images/kgl.png"
    },
    "blog-golden-triangle.html": {
        "old_title_pattern": r"<h3>How to Plan the Perfect 6-Day Golden Triangle Luxury Tour</h3>",
        "new_title": "<h3>6-Day Golden Triangle Tour India Itinerary \(Luxury Guide\)</h3>",
        "h1_pattern": r"<h1>How to Plan the Perfect 6-Day Golden Triangle Luxury Tour</h1>",
        "new_h1": "<h1>6-Day Golden Triangle Tour India Itinerary (Luxury Guide)</h1>",
        "meta_pattern": r"<div class=\"article-meta\">Luxury Travel • Published July 2026</div>",
        "new_meta": "<div class=\"article-meta\">Luxury Travel • 15 Min Read</div>",
        "card_meta_pattern": r"<div class=\"blog-meta\">Luxury • \d+ Min Read</div>",
        "new_card_meta": "<div class=\"blog-meta\">Luxury • 15 Min Read</div>",
        "img_key": "golden_triangle",
        "old_img": "images/hero.png"
    },
    "blog-tarsar-marsar.html": {
        "old_title_pattern": r"<h3>Tarsar Marsar Trek vs Kashmir Great Lakes: Which is Right for You\?</h3>",
        "new_title": "<h3>Tarsar Marsar Trek vs Kashmir Great Lakes: Which is Best\?</h3>",
        "h1_pattern": r"<h1>Tarsar Marsar Trek vs Kashmir Great Lakes</h1>",
        "new_h1": "<h1>Tarsar Marsar Trek vs Kashmir Great Lakes: Which is Best?</h1>",
        "meta_pattern": r"<div class=\"article-meta\">Trekking Guide • Published July 2026</div>",
        "new_meta": "<div class=\"article-meta\">Trekking Guide • 15 Min Read</div>",
        "card_meta_pattern": r"<div class=\"blog-meta\">Trekking • \d+ Min Read</div>",
        "new_card_meta": "<div class=\"blog-meta\">Trekking • 15 Min Read</div>",
        "img_key": "tarsar",
        "old_img": "images/tarsar.png"
    },
    "blog-rajasthan-heritage.html": {
        "old_title_pattern": r"<h3>Palaces & Sands: 10 Must-Visit Heritage Hotels in Rajasthan</h3>",
        "new_title": "<h3>Top 10 Best Heritage Hotels in Rajasthan for a Royal Stay</h3>",
        "h1_pattern": r"<h1>Palaces & Sands: 10 Must-Visit Heritage Hotels in Rajasthan</h1>",
        "new_h1": "<h1>Top 10 Best Heritage Hotels in Rajasthan for a Royal Stay</h1>",
        "meta_pattern": r"<div class=\"article-meta\">Heritage • Published July 2026</div>",
        "new_meta": "<div class=\"article-meta\">Heritage • 15 Min Read</div>",
        "card_meta_pattern": r"<div class=\"blog-meta\">Heritage • \d+ Min Read</div>",
        "new_card_meta": "<div class=\"blog-meta\">Heritage • 15 Min Read</div>",
        "img_key": "rajasthan",
        "old_img": "images/jaipur.png"
    },
    "blog-kerala-houseboats.html": {
        "old_title_pattern": r"<h3>Exploring the Kerala Backwaters: A Luxury Houseboat Guide</h3>",
        "new_title": "<h3>Luxury Kerala Houseboats Guide: Exploring the Alleppey Backwaters</h3>",
        "h1_pattern": r"<h1>Exploring the Kerala Backwaters: A Luxury Houseboat Guide</h1>",
        "new_h1": "<h1>Luxury Kerala Houseboats Guide: Exploring the Alleppey Backwaters</h1>",
        "meta_pattern": r"<div class=\"article-meta\">Relaxation • Published July 2026</div>",
        "new_meta": "<div class=\"article-meta\">Relaxation • 15 Min Read</div>",
        "card_meta_pattern": r"<div class=\"blog-meta\">Relaxation • \d+ Min Read</div>",
        "new_card_meta": "<div class=\"blog-meta\">Relaxation • 15 Min Read</div>",
        "img_key": "kerala",
        "old_img": "images/kerala.png"
    },
    "blog-first-time-india.html": {
        "old_title_pattern": r"<h3>The First-Timer's Guide to Safe and Luxurious Travel in India</h3>",
        "new_title": "<h3>First-Time Travel Guide to India: Essential Tips & Advice</h3>",
        "h1_pattern": r"<h1>The First-Timer's Guide to Safe and Luxurious Travel in India</h1>",
        "new_h1": "<h1>First-Time Travel Guide to India: Essential Tips & Advice</h1>",
        "meta_pattern": r"<div class=\"article-meta\">Travel Tips • Published July 2026</div>",
        "new_meta": "<div class=\"article-meta\">Travel Tips • 15 Min Read</div>",
        "card_meta_pattern": r"<div class=\"blog-meta\">Travel Tips • \d+ Min Read</div>",
        "new_card_meta": "<div class=\"blog-meta\">Travel Tips • 15 Min Read</div>",
        "img_key": "india",
        "old_img": "images/culture.png"
    }
}

# Update individual blog pages
for filename, data in blog_data.items():
    try:
        with open(filename, 'r') as f:
            content = f.read()
        
        # Replace H1
        content = re.sub(data["h1_pattern"], data["new_h1"], content)
        # Replace Meta
        content = re.sub(data["meta_pattern"], data["new_meta"], content)
        # Replace Image
        new_img_path = images[data["img_key"]]
        content = re.sub(fr'src="{data["old_img"]}"', f'src="{new_img_path}"', content)
        
        with open(filename, 'w') as f:
            f.write(content)
        print(f"Updated {filename}")
    except Exception as e:
        print(f"Error updating {filename}: {e}")

# Update blog.html
try:
    with open('blog.html', 'r') as f:
        content = f.read()
    
    for filename, data in blog_data.items():
        # Replace Card Title (without escapes in replacement)
        content = re.sub(data["old_title_pattern"], data["new_title"].replace('\\', ''), content)
        # Replace Card Meta
        content = re.sub(data["card_meta_pattern"], data["new_card_meta"], content)
        # Replace Card Image
        new_img_path = images[data["img_key"]]
        content = re.sub(fr"url\('{data['old_img']}'\)", f"url('{new_img_path}')", content)

    with open('blog.html', 'w') as f:
        f.write(content)
    print("Updated blog.html")
except Exception as e:
    print(f"Error updating blog.html: {e}")
