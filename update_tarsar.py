import re
# HTML File replacements for tarsar
filename = "blog-tarsar-marsar.html"
with open(filename, 'r') as f:
    content = f.read()

content = re.sub(r'src="images/tarsar.png"', f'src="images/blog_new/tarsar.png"', content)

with open(filename, 'w') as f:
    f.write(content)

with open('blog.html', 'r') as f:
    content = f.read()

content = re.sub(r"url\('images/tarsar.png'\)", f"url('images/blog_new/tarsar.png')", content)

with open('blog.html', 'w') as f:
    f.write(content)
