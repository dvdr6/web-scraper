import os
import sys
import requests
import argparse
import zipfile
import time
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
from pathlib import Path

def get_safe_path(url, output_dir):
    parsed = urlparse(url)
    path = unquote(parsed.path)
    if not path or path.endswith('/'):
        path = os.path.join(path, 'index.html')
    elif '.' not in os.path.basename(path):
        path = path + '.html'
    path = path.lstrip('/')
    return os.path.abspath(os.path.join(output_dir, path))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('--depth', type=int, default=3)
    parser.add_argument('--output', default='website_dump')
    parser.add_argument('--zip', action='store_true')
    args = parser.parse_args()

    start_url = args.url
    if not start_url.startswith(('http://', 'https://')):
        start_url = 'https://' + start_url
    
    domain = urlparse(start_url).netloc
    output_dir = os.path.abspath(args.output)
    visited = {}
    queue = [(start_url, 0)]

    while queue:
        url, depth = queue.pop(0)
        if url in visited or depth > args.depth:
            continue
        
        try:
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code != 200:
                continue
            
            local_path = get_safe_path(url, output_dir)
            visited[url] = local_path
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            content_type = response.headers.get('Content-Type', '').lower()
            
            if 'text/html' in content_type:
                soup = BeautifulSoup(response.content, 'html.parser')
                tags_attrs = {'a': 'href', 'link': 'href', 'script': 'src', 'img': 'src', 'source': 'src', 'video': 'src'}
                
                for tag, attr in tags_attrs.items():
                    for element in soup.find_all(tag, **{attr: True}):
                        link = element[attr]
                        if link.startswith(('data:', 'mailto:', 'tel:', '#')):
                            continue
                        
                        abs_url = urljoin(url, link)
                        parsed_link = urlparse(abs_url)
                        
                        if parsed_link.netloc == domain:
                            target_local = get_safe_path(abs_url, output_dir)
                            rel_path = os.path.relpath(target_local, os.path.dirname(local_path))
                            element[attr] = rel_path
                            
                            if abs_url not in visited:
                                if tag == 'a':
                                    queue.append((abs_url, depth + 1))
                                else:
                                    queue.append((abs_url, depth))
                
                with open(local_path, 'wb') as f:
                    f.write(soup.prettify('utf-8'))
            
            elif 'text/css' in content_type:
                css_content = response.text
                urls = re.findall(r'url\((["\']?)([^)]*)\1\)', css_content)
                for quote, css_url in urls:
                    css_url = css_url.strip('"\'')
                    if css_url.startswith(('data:', 'http', '//')):
                        if not css_url.startswith(('http', '//')) or urlparse(urljoin(url, css_url)).netloc != domain:
                            continue
                    
                    abs_url = urljoin(url, css_url)
                    target_local = get_safe_path(abs_url, output_dir)
                    rel_path = os.path.relpath(target_local, os.path.dirname(local_path))
                    css_content = css_content.replace(css_url, rel_path)
                    
                    if abs_url not in visited:
                        queue.append((abs_url, depth))
                
                with open(local_path, 'w', encoding='utf-8') as f:
                    f.write(css_content)
            else:
                with open(local_path, 'wb') as f:
                    f.write(response.content)
            
            print(f"Downloaded: {url}")
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error downloading {url}: {e}")
            continue

    if args.zip:
        zip_name = f"{args.output}.zip"
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(output_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, output_dir))
        print(f"Created archive: {zip_name}")

if __name__ == '__main__':
    main()
