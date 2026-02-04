# Quick Start: Product Website Management

## First Time: Export Your Current Site

If you have the Onion.Press product website running and want to save it to git:

```bash
# 1. Make sure Onion.Press is running
# 2. Export the site
cd product-website/scripts
./export-site.sh

# 3. Commit to git
cd ../..
git add product-website/
git commit -m "Initial export of product website"
git push
```

## Deploy to a New Instance

If you want to load the product website on a fresh Onion.Press installation:

```bash
# 1. Clone the repo
git clone https://github.com/brewsterkahle/onion.press.git
cd onion.press

# 2. Start Onion.Press (use the app or run the launcher)

# 3. Wait for it to fully start (check menubar icon is purple)

# 4. Import the website
cd product-website/scripts
./import-site.sh

# 5. Access your site
# Onion: http://[your-onion-address].onion
# Local: http://localhost:8080
```

## Regular Workflow

### Making Updates

1. Edit content through WordPress admin at http://localhost:8080/wp-admin
2. Preview changes
3. When satisfied, export:
   ```bash
   cd product-website/scripts
   ./export-site.sh
   ```
4. Commit changes:
   ```bash
   git add product-website/
   git commit -m "Update homepage hero section"
   git push
   ```

### Pulling Updates from Others

```bash
git pull
cd product-website/scripts
./import-site.sh
```

## What Gets Saved

✅ **All your content:**
- Posts and pages
- Media files (images, PDFs)
- Custom themes
- Plugins
- WordPress settings
- Users and roles

✅ **Portable:**
- Works on any Onion.Press instance
- URLs automatically updated to new onion address

❌ **Not saved:**
- WordPress core (comes from Docker image)
- Tor keys (generated per instance)

## Need Help?

See the full [README.md](README.md) for detailed documentation.
