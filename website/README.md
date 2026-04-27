# Cognitive Engine Website

GitHub Pages website for the Cognitive Engine project with a sci-fi theme.

## Structure

- `index.html` - Main homepage with sci-fi theme
- `wiki-viewer.html` - Wiki documentation viewer with markdown rendering
- `wiki/` - Markdown documentation files
- `licences/` - License documents
- `pages/` - Additional HTML pages (thesis, investor overview)
- `.nojekyll` - GitHub Pages configuration

## Features

- **Sci-Fi Theme**: Dark gradient backgrounds with cyan accent colors and glowing effects
- **Animated Grid Background**: Subtle grid pattern for visual depth
- **Responsive Design**: Works on desktop and mobile devices
- **Wiki Integration**: Markdown documentation rendered with styled output
- **Navigation**: Sidebar navigation for easy access to documentation

## Local Testing

Start a local web server:

```bash
cd website
python3 -m http.server 8000
```

Access at: http://localhost:8000

## GitHub Pages Deployment

### Option 1: Using gh-pages branch

1. Create a gh-pages branch:
```bash
git checkout --orphan gh-pages
git rm -rf .
cp -r ../website/* .
git add .
git commit -m "Initial GitHub Pages"
git push origin gh-pages
```

2. Enable GitHub Pages in repository settings:
   - Go to repository Settings → Pages
   - Select `gh-pages` branch
   - Save

### Option 2: Using main branch with docs folder

1. Move website to docs folder:
```bash
mv website docs
```

2. Enable GitHub Pages:
   - Settings → Pages
   - Select `docs` folder
   - Save

### Option 3: Using GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Setup Pages
        uses: actions/configure-pages@v3
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v2
        with:
          path: ./website
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v2
```

## Customization

### Colors

Main theme colors used:
- Background: `#0a0a1a` to `#1a1a3a` gradient
- Accent: `#00d4ff` (cyan)
- Text: `#e0e0ff` (light purple)
- Links: `#a0a0ff` (purple)

To customize, edit the CSS in `index.html` and `wiki-viewer.html`.

### Adding New Pages

1. Create markdown file in `wiki/` directory
2. Add link to sidebar in `wiki-viewer.html`
3. The page will be automatically rendered

## License

AGPL-3.0
