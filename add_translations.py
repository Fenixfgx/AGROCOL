import re

# Leer el archivo
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Lista de reemplazos a realizar
replacements = [
    # About section - slider items
    (r'<h3>Organic foliage</h3>', '<h3><span data-lang="about.organicFoliage">Organic foliage</span></h3>'),
    (r'<h3>Natural foliage</h3>', '<h3><span data-lang="about.naturalFoliage">Natural foliage</span></h3>'),
    
    # Choose us section
    (r'<h4>Certified Natural Foliage</h4>', '<h4><span data-lang="about.certifiedNatural">Certified Natural Foliage</span></h4>'),
    (r"<h4>We're Distributors of Quality 100%</h4>", '<h4><span data-lang="about.distributorsQuality">We\'re Distributors of Quality 100%</span></h4>'),
    
    # More About Us button
    (r'More About Us <i class="far fa-arrow-right">', '<span data-lang="about.moreAboutUs">More About Us</span> <i class="far fa-arrow-right">'),
]

count = 0
# Aplicar cada reemplazo
for pattern, replacement in replacements:
    if pattern in content:
        content = content.replace(pattern, replacement)
        count += 1
        print(f'✓ Reemplazado: {pattern[:50]}...')

# Guardar el archivo
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\n✓ Total reemplazos aplicados: {count}')
