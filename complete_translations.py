#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para agregar traducciones completas al index.html
"""

import re

# Leer el archivo HTML
with open('index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Lista de reemplazos para HTML
html_replacements = [
    # Hero Section - Slide 1
    ("We're Distributors of <span data-lang=\"features.feature1.title\">Certified Quality</span>",
     '<span data-lang="hero.distributors">We\'re Distributors of</span> <span data-lang="features.feature1.title">Certified Quality</span>'),
    
    # Hero Section - Slide 2
    ("<i class=\"fas fa-star\"></i>\n                                                We're Distributors of Quality 100%",
     '<i class="fas fa-star"></i>\n                                                <span data-lang="hero.distributorsQuality">We\'re Distributors of Quality 100%</span>'),
    
    # Hero Slide 2 button
    (">Nuestros Productos\n                                                <i class=\"far fa-arrow-right\">",
     '><span data-lang="products.ourProducts">Our Products</span>\n                                                <i class="far fa-arrow-right">'),
    
    # About Section - Fresh Ornamental Plants
    ("<h3>Fresh Ornamental Plants</h3>",
     '<h3><span data-lang="about.freshOrnamental">Fresh Ornamental Plants</span></h3>'),
    
    # Choose Us Section - About Us label
    ('<span class="wow fadeInUp"><img src="assets/img/sub-title.svg" alt="img">About Us</span>',
     '<span class="wow fadeInUp"><img src="assets/img/sub-title.svg" alt="img"><span data-lang="chooseUs.aboutUs">About Us</span></span>'),
    
    # Choose Us Section - Title
    ('<h2 class="text-anim">Currently We\'re Cultivating & Selling Natural Foliage</h2>',
     '<h2 class="text-anim" data-lang="chooseUs.title">Currently We\'re Cultivating & Selling Natural Foliage</h2>'),
    
    # Choose Us - first paragraph (already has content, needs data-lang)
    ('<p class="choose-text wow fadeInUp" data-wow-delay=".2s">\n                                    We specialize in the commercialization and export of certified natural foliage from Colombia.</p>',
     '<p class="choose-text wow fadeInUp" data-wow-delay=".2s" data-lang="about.description">\n                                    We specialize in the commercialization and export of certified natural foliage from Colombia.</p>'),
    
    # Choose Us - Distributors quality
    ('<h4>We\'re Distributors of Quality 100%</h4>',
     '<h4><span data-lang="about.distributorsQuality">We\'re Distributors of Quality 100%</span></h4>'),
    
    # Choose Us - second paragraph (Spanish text - need to make it English by default)
    ('<p class="choose-text-2 wow fadeInUp" data-wow-delay=".6s">\n                                    Comercializamos y exportamos follajes naturales y productos ornamentales mediante una gestión completa, asegurando calidad, cumplimiento fitosanitario y coordinación logística para operaciones confiables y trazables.\n                                </p>',
     '<p class="choose-text-2 wow fadeInUp" data-wow-delay=".6s" data-lang="about.mission">\n                                    Our mission is to guarantee reliable and traceable operations that meet the highest technical, regulatory, and commercial standards of the international floriculture industry.\n                                </p>'),
    
    # Phone label
    ('<p>Phone:</p>',
     '<p data-lang="contactInfo.phoneLabel">Phone:</p>'),
    
    # Service section - More Details links (multiple)
    ('>More Details <i class="far fa-arrow-right"></i></a>',
     ' data-lang="features.moreDetails">More Details <i class="far fa-arrow-right"></i></a>'),
    
    # Counter section - second counter (duplicated text without data-lang)
    ('<p>Export Shipments</p>\n                        </div>\n                    </div>\n                    <div class="line"></div>\n                    <div class="counter-box-items wow fadeInUp" data-wow-delay=".6s">',
     '<p data-lang="counter.counter2.label">Satisfied Clients</p>\n                        </div>\n                    </div>\n                    <div class="line"></div>\n                    <div class="counter-box-items wow fadeInUp" data-wow-delay=".6s">'),
    
    # Choose Us List Items
    ('<h3>Tropical Natural Foliage</h3>\n                                                <p>We specialize in the commercialization and export of certified natural foliage from Colombia.</p>',
     '<h3 data-lang="chooseUs.item1.title">Tropical Natural Foliage</h3>\n                                                <p data-lang="about.description">We specialize in the commercialization and export of certified natural foliage from Colombia.</p>'),
    
    ('<h3>Healthy Foods</h3>\n                                                <p>We specialize in the commercialization and export of certified natural foliage from Colombia.</p>',
     '<h3 data-lang="chooseUs.item2.title">Healthy Products</h3>\n                                                <p data-lang="about.description">We specialize in the commercialization and export of certified natural foliage from Colombia.</p>'),
    
    ('<h3>Professional Farmers</h3>\n                                                <p>We specialize in the commercialization and export of certified natural foliage from Colombia.</p>',
     '<h3 data-lang="chooseUs.item3.title">Professional Farmers</h3>\n                                                <p data-lang="about.description">We specialize in the commercialization and export of certified natural foliage from Colombia.</p>'),
    
    ('<h3>Acinia Simply</h3>\n                                                <p>We specialize in the commercialization and export of certified natural foliage from Colombia.</p>',
     '<h3 data-lang="chooseUs.item4.title">Simple Process</h3>\n                                                <p data-lang="about.description">We specialize in the commercialization and export of certified natural foliage from Colombia.</p>'),
    
    ('<h3>New Technology</h3>\n                                                <p>We specialize in the commercialization and export of certified natural foliage from Colombia.</p>',
     '<h3 data-lang="chooseUs.item5.title">New Technology</h3>\n                                                <p data-lang="about.description">We specialize in the commercialization and export of certified natural foliage from Colombia.</p>'),
    
    ('<h3>Fresh Foliage Varieties</h3>\n                                                <p>We specialize in the commercialization and export of certified natural foliage from Colombia.</p>',
     '<h3 data-lang="chooseUs.item6.title">Fresh Foliage Varieties</h3>\n                                                <p data-lang="about.description">We specialize in the commercialization and export of certified natural foliage from Colombia.</p>'),
    
    # CTA Banner - second part
    ('. <br> Foliage Export for a better future</h2>',
     '. <br> <span data-lang="ctaBanner.subtitle">Foliage Export for a better future</span></h2>'),
    
    # Products Section
    ('<span class="wow fadeInUp"><img src="assets/img/sub-title.svg" alt="img">Our Products</span>',
     '<span class="wow fadeInUp"><img src="assets/img/sub-title.svg" alt="img"><span data-lang="products.sectionSubtitle">Our Products</span></span>'),
    
    ('<h2 class="text-anim">Export Portfolio</h2>',
     '<h2 class="text-anim" data-lang="products.sectionTitle">Export Portfolio</h2>'),
    
    # Product names
    ('<h3><a href="project-details.html">Tropical Foliage</a></h3>',
     '<h3><a href="project-details.html"><span data-lang="products.product1.name">Tropical Foliage</span></a></h3>'),
    
    ('<h3><a href="project-details.html">Exotic Palms</a></h3>',
     '<h3><a href="project-details.html"><span data-lang="products.product2.name">Exotic Palms</span></a></h3>'),
    
    ('<h3><a href="project-details.html">Philodendron</a></h3>',
     '<h3><a href="project-details.html"><span data-lang="products.product3.name">Philodendron</span></a></h3>'),
    
    ('<h3><a href="project-details.html">Monstera</a></h3>',
     '<h3><a href="project-details.html"><span data-lang="products.product4.name">Monstera</span></a></h3>'),
    
    ('<h3><a href="project-details.html">Dracaena</a></h3>',
     '<h3><a href="project-details.html"><span data-lang="products.product5.name">Dracaena</span></a></h3>'),
    
    ('<h3><a href="project-details.html">Organic Beans</a></h3>',
     '<h3><a href="project-details.html"><span data-lang="products.product6.name">Organic Beans</span></a></h3>'),
    
    ('<h3><a href="project-details.html">Green Beans</a></h3>',
     '<h3><a href="project-details.html"><span data-lang="products.product7.name">Green Beans</span></a></h3>'),
    
    ('<h3><a href="project-details.html">Natural Artoke</a></h3>',
     '<h3><a href="project-details.html"><span data-lang="products.product8.name">Natural Artoke</span></a></h3>'),
    
    # Projects Section
    ('<span class="wow fadeInUp"><img src="assets/img/sub-title.svg" alt="img">Our Projects</span>',
     '<span class="wow fadeInUp"><img src="assets/img/sub-title.svg" alt="img"><span data-lang="projects.sectionSubtitle">Our Projects</span></span>'),
    
    ('<h2 class="text-anim">Our Latest Projects</h2>',
     '<h2 class="text-anim" data-lang="projects.sectionTitle">Our Latest Projects</h2>'),
    
    # FAQ Section
    ('<span class="wow fadeInUp"><img src="assets/img/sub-title.svg" alt="img">Our FAQs</span>',
     '<span class="wow fadeInUp"><img src="assets/img/sub-title.svg" alt="img"><span data-lang="faq.sectionSubtitle">Our FAQs</span></span>'),
    
    ('<h2 class="text-anim">Frequently Asked Questions About Us</h2>',
     '<h2 class="text-anim" data-lang="faq.sectionTitle">Frequently Asked Questions About Us</h2>'),
    
    # FAQ Contact items
    ('<h5>Call Us</h5>',
     '<h5 data-lang="contactInfo.callUs">Call Us</h5>'),
    
    ('<h5>Our Location</h5>',
     '<h5 data-lang="contactInfo.ourLocation">Our Location</h5>'),
    
    ('<h5>Mail us</h5>',
     '<h5 data-lang="contactInfo.mailUs">Mail us</h5>'),
    
    # FAQ Questions
    ('1. What services does your horticultural company offer?',
     '<span data-lang="faq.q1">1. What services does your horticultural company offer?</span>'),
    
    ('2. Do you specialize in foliage exporting?',
     '<span data-lang="faq.q2">2. Do you specialize in foliage exporting?</span>'),
    
    ('3. What types of foliage do you grow?',
     '<span data-lang="faq.q3">3. What types of foliage do you grow?</span>'),
    
    ('4. Do you sell plants and foliage export equipment?',
     '<span data-lang="faq.q4">4. Do you sell plants and foliage export equipment?</span>'),
    
    ('5. How can I place an order for your products?',
     '<span data-lang="faq.q5">5. How can I place an order for your products?</span>'),
    
    # FAQ Answers
    ('You can place an order through our website by selecting your desired products, adding them to the cart, and checking out.',
     '<span data-lang="faq.a1">You can place an order through our website by selecting your desired products, adding them to the cart, and checking out.</span>'),
    
    # Feature Info Section
    ('<h5>Member Discount</h5>\n                                <p>Back guarantee under 7 days</p>',
     '<h5 data-lang="featureInfo.discount.title">Member Discount</h5>\n                                <p data-lang="featureInfo.discount.desc">Back guarantee under 7 days</p>'),
    
    ('<h5>Free Shipping</h5>\n                                <p>Free shipping on all order</p>',
     '<h5 data-lang="featureInfo.shipping.title">Free Shipping</h5>\n                                <p data-lang="featureInfo.shipping.desc">Free shipping on all order</p>'),
    
    ('<h5>Money Return</h5>\n                                <p>Support online 24 hours a day</p>',
     '<h5 data-lang="featureInfo.return.title">Money Return</h5>\n                                <p data-lang="featureInfo.return.desc">Support online 24 hours a day</p>'),
    
    ('<h5>Online Support</h5>\n                                <p>Back guarantee under 7 days</p>',
     '<h5 data-lang="featureInfo.support.title">Online Support</h5>\n                                <p data-lang="featureInfo.support.desc">Back guarantee under 7 days</p>'),
    
    # Footer
    ('<p>We specialize in the commercialization and export of certified natural foliage from Colombia.</p>\n                                    <form action="#">',
     '<p data-lang="about.description">We specialize in the commercialization and export of certified natural foliage from Colombia.</p>\n                                    <form action="#">'),
    
    # Footer headline
    ('<h2 data-lang="footer.headline">If it\'s good for the planet, <br> it\'s good for you.</h2>',
     '<h2 data-lang="footer.headline">If it\'s good for the planet, <br> it\'s good for you.</h2>'),
    
    ('>View Online Shop <i class="far fa-arrow-right">',
     ' data-lang="footer.viewShop">View Services <i class="far fa-arrow-right">'),
    
    # Project slides - Gallery text (first slide without data-lang)
    ('<span class="project-text">Gallery</span>\n                                    <h4 class="text-title">\n                                        Eco and Natural Foliage',
     '<span class="project-text" data-lang="projects.gallery">Gallery</span>\n                                    <h4 class="text-title" data-lang="projects.project1.title">\n                                        Eco and Natural Foliage'),
    
    ('<span>Gallery</span>\n                                    <h3>Eco and Natural Foliage</h3>\n                                    <p>\n                                        We specialize in the commercialization and export of certified natural foliage from Colombia.</p>',
     '<span data-lang="projects.gallery">Gallery</span>\n                                    <h3 data-lang="projects.project1.title">Eco and Natural Foliage</h3>\n                                    <p data-lang="about.description">\n                                        We specialize in the commercialization and export of certified natural foliage from Colombia.</p>'),
]

# Aplicar reemplazos
count = 0
for old, new in html_replacements:
    if old in html_content:
        html_content = html_content.replace(old, new)
        count += 1
        print(f"✓ Reemplazado: {old[:50]}...")

# Guardar HTML
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"\n✓ Total de reemplazos HTML: {count}")
print("\nAhora actualizando translations.js...")
