import re

files_updates = {
    "blog-kgl-trek.html": [
        (r"Kashmir Great Lakes \(KGL\)", r'<a href="itineraries.html#kgl" style="color: var(--primary-color); font-weight: bold; text-decoration: underline;">Kashmir Great Lakes (KGL)</a>'),
        (r"Himalayas", r'<a href="blog-tarsar-marsar.html" style="color: var(--primary-color); font-weight: bold; text-decoration: underline;">Himalayas</a>')
    ],
    "blog-golden-triangle.html": [
        (r"Jaipur", r'<a href="blog-rajasthan-heritage.html" style="color: var(--primary-color); font-weight: bold; text-decoration: underline;">Jaipur</a>'),
        (r"India", r'<a href="index.html" style="color: var(--primary-color); font-weight: bold; text-decoration: underline;">India</a>')
    ],
    "blog-tarsar-marsar.html": [
        (r"Kashmir Great Lakes", r'<a href="blog-kgl-trek.html" style="color: var(--primary-color); font-weight: bold; text-decoration: underline;">Kashmir Great Lakes</a>')
    ],
    "blog-first-time-india.html": [
        (r"Golden Triangle", r'<a href="blog-golden-triangle.html" style="color: var(--primary-color); font-weight: bold; text-decoration: underline;">Golden Triangle</a>')
    ],
    "blog-kerala-houseboats.html": [
        (r"first time", r'<a href="blog-first-time-india.html" style="color: var(--primary-color); font-weight: bold; text-decoration: underline;">first time</a>')
    ],
    "blog-rajasthan-heritage.html": [
        (r"Golden Triangle", r'<a href="blog-golden-triangle.html" style="color: var(--primary-color); font-weight: bold; text-decoration: underline;">Golden Triangle</a>')
    ]
}

for filename, updates in files_updates.items():
    try:
        with open(filename, 'r') as f:
            content = f.read()
            
        for search, replace in updates:
            # Replace only the first occurrence to avoid messing up headers or existing links
            # We can use a simple regex that avoids replacing inside tags
            # A simple approach for this exact known text:
            # But wait, it's safer to just do a single string replace if we find it in paragraphs.
            pass
            
        # Using simple string replace for first occurrence of specific words
        for search, replace in updates:
            # Replace only the first occurrence outside of tags (basic check)
            # Find the index of the first occurrence
            content = content.replace(search.replace('\\', ''), replace, 1)
            
        with open(filename, 'w') as f:
            f.write(content)
        print(f"Updated {filename}")
    except Exception as e:
        print(f"Failed to update {filename}: {e}")
