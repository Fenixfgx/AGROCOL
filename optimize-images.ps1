# Script to add lazy loading to images in HTML files
$files = @("index.html", "contact.html")

foreach ($file in $files) {
    if (Test-Path $file) {
        $content = Get-Content $file -Raw
        
        # Add loading="lazy" to images that don't have it (except critical images)
        # Skip logos, flags in header, and hero images
        $content = $content -replace '(<img(?![^>]*loading=)[^>]*src="assets/img/(?!flag|logo)[^"]*"[^>]*)>', '$1 loading="lazy">'
        
        # Add loading="lazy" to images in gallery, products, news sections
        $content = $content -replace '(<img(?![^>]*loading=)[^>]*src="assets/img/(?:home-|inner-page/|shop/)[^"]*"[^>]*)>', '$1 loading="lazy">'
        
        Set-Content $file $content -NoNewline
        Write-Host "Optimized $file"
    }
}

Write-Host "Image optimization complete!"
