# Homebrew Installation for Onion.Press

This directory contains the Homebrew Cask formula for installing Onion.Press.

## For Users

### Installing via Homebrew

```bash
# Add the tap
brew tap brewsterkahle/onion-press https://github.com/brewsterkahle/onion.press

# Install
brew install --cask onion-press
```

### Uninstalling

```bash
# Uninstall and remove all data
brew uninstall --zap onion-press
```

## For Maintainers

### Publishing to Homebrew

There are two options for distributing the cask:

#### Option 1: Submit to homebrew/cask (Official)

To make `brew install --cask onion-press` work without a tap:

1. Fork https://github.com/Homebrew/homebrew-cask
2. Copy `onion-press.rb` to `Casks/o/onion-press.rb`
3. Submit a PR to the Homebrew/homebrew-cask repository
4. Wait for review and approval

**Requirements:**
- App must be popular/notable
- Must meet Homebrew's quality guidelines
- Regular updates and maintenance expected

#### Option 2: Create a Homebrew Tap (Easier)

Keep the formula in this repository:

1. Users run: `brew tap brewsterkahle/onion-press https://github.com/brewsterkahle/onion.press`
2. Then: `brew install --cask onion-press`

This method gives you full control and doesn't require Homebrew maintainer approval.

### Updating the Formula

When releasing a new version:

1. Build the new DMG: `./build/build-dmg-simple.sh`
2. Calculate SHA256: `shasum -a 256 build/onion.press.dmg`
3. Update `homebrew/onion-press.rb`:
   - Update `version` number
   - Update `sha256` hash
4. Commit and push changes
5. Create GitHub release with the DMG

Users will automatically get updates via `brew upgrade`.

### Testing Locally

Test the formula before publishing:

```bash
# Install from local file
brew install --cask homebrew/onion-press.rb

# Test uninstall
brew uninstall --cask onion-press

# Test with zap (removes all data)
brew uninstall --zap onion-press
```

### Verifying SHA256

Always verify the SHA256 hash matches the released DMG:

```bash
# Calculate hash
shasum -a 256 build/onion.press.dmg

# Or download from GitHub and verify
curl -L -o /tmp/onion.press.dmg https://github.com/brewsterkahle/onion.press/releases/download/v2.1.4/onion.press.dmg
shasum -a 256 /tmp/onion.press.dmg
```

## Cask Documentation

For more information about Homebrew Cask formulas:
- https://docs.brew.sh/Cask-Cookbook
- https://github.com/Homebrew/homebrew-cask/blob/master/CONTRIBUTING.md
