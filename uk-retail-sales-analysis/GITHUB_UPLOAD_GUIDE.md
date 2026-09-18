# GitHub Upload Guide

## Option A — GitHub website
1. Create a new public repository called `uk-retail-sales-analysis`.
2. Do not initialise it with extra files if you plan to upload this folder as-is.
3. Upload the repository contents.
4. Make sure `README.md` appears on the repository home page.

## Option B — Git from your computer

```bash
cd uk-retail-sales-analysis
git init
git add .
git commit -m "Build end-to-end UK retail sales analytics project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/uk-retail-sales-analysis.git
git push -u origin main
```

After pushing, check the Actions tab. The included workflow should run the data-quality tests automatically.
