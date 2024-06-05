import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

# Función para obtener todas las etiquetas <a> con sus respectivos enlaces
def get_links(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
        return links
    except requests.RequestException as e:
        print(f"Error al acceder a {url}: {e}")
        return []

# Función para obtener las etiquetas <h1> y <p> de una página
def get_h1_p_tags(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        h1_tags = [h1.get_text(strip=True) for h1 in soup.find_all('h1')]
        p_tags = [p.get_text(strip=True) for p in soup.find_all('p')]
        return h1_tags + p_tags
    except requests.RequestException as e:
        print(f"Error al acceder a {url}: {e}")
        return []

# Función principal del crawler
def web_crawler(start_url, max_pages=100):
    result = {}
    visited = set()
    to_visit = [start_url]

    while to_visit and len(visited) < max_pages:
        current_url = to_visit.pop(0)
        if current_url not in visited:
            visited.add(current_url)
            print(f"Visitando: {current_url}")
            links = get_links(current_url)
            content = get_h1_p_tags(current_url)
            result[current_url] = content
            for link in links:
                if link not in visited and link not in to_visit:
                    to_visit.append(link)

    return result

# URL inicial
start_url = "https://supercell.com/en/games/clashroyale/"

# Ejecutar el crawler
result = web_crawler(start_url)

# Guardar el resultado en un archivo JSON
with open('result.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

print("Crawling completado. Resultados guardados en result.json")
