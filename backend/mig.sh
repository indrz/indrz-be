mkdir backend
# Move everything except .git into backend
shopt -s extglob dotglob
mv !(backend|.git) backend/ 2>/dev/null || true
shopt -u dotglob

# Keep a top-level README that explains the new structure
cat > README.md <<'EOF'
# Monorepo

- backend/ — Django API
- frontend/ — Vue/Nuxt client
EOF

git add -A
git commit -m "chore(repo): move backend code under /backend"

