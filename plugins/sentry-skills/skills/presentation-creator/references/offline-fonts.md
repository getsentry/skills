# Offline Font Inlining

By default, the presentation template loads Rubik and Material Symbols from Google Fonts via `<link>` tags. This works for development and online use, but the fonts will **not** be included in the single-file HTML build — `vite-plugin-singlefile` only inlines local assets.

If the presentation needs to work fully offline, follow these steps to inline the fonts.

## Step 1: Install @fontsource/rubik

Replace the Google Fonts `<link>` with the npm package:

```sh
npm install @fontsource/rubik
```

## Step 2: Import font weights in main.jsx

```jsx
import '@fontsource/rubik/300.css'
import '@fontsource/rubik/400.css'
import '@fontsource/rubik/500.css'
import '@fontsource/rubik/600.css'
import '@fontsource/rubik/700.css'
```

## Step 3: Remove Google Fonts links from index.html

Replace:
```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link href="https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
```

With:
```html
<!-- Rubik font loaded via @fontsource/rubik (inlined at build time) -->
```

## Step 4: Raise the asset inline limit in vite.config.js

Font files (woff2) are ~50–200KB each. Set a high limit so Vite base64-encodes them into the CSS, which `vite-plugin-singlefile` then embeds in the HTML:

```javascript
export default defineConfig({
  plugins: [react(), viteSingleFile()],
  build: { assetsInlineLimit: 1024 * 1024 },
})
```

## Step 5: Build

```sh
npm run build
```

The resulting `dist/index.html` will be ~1.5MB (vs ~200KB without fonts) but fully self-contained.

## Material Symbols

The `material-symbols` npm package can be installed similarly, but it is very large. For offline builds, prefer inline SVG or Unicode symbols for icons instead.
