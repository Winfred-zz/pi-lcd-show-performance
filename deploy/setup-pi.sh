#!/bin/sh
# One-time setup for push-to-deploy. Run this ON THE PI, e.g.:
#   scp deploy/setup-pi.sh pi@<pi-host>:~/ && ssh pi@<pi-host> sh setup-pi.sh
set -e

WORK_TREE=/opt/pi-lcd-show-performance
GIT_DIR="$WORK_TREE.git"

sudo mkdir -p "$WORK_TREE" "$GIT_DIR"
sudo chown "$(whoami)":"$(whoami)" "$WORK_TREE" "$GIT_DIR"

git init --bare "$GIT_DIR"
git -C "$GIT_DIR" symbolic-ref HEAD refs/heads/main

cat > "$GIT_DIR/hooks/post-receive" <<'EOF'
#!/bin/sh
set -e
WORK_TREE=/opt/pi-lcd-show-performance
GIT_DIR=/opt/pi-lcd-show-performance.git
git --work-tree="$WORK_TREE" --git-dir="$GIT_DIR" checkout -f main
sudo /usr/bin/systemctl restart lcdshowstatus.service
EOF
chmod +x "$GIT_DIR/hooks/post-receive"

# Lets this account restart the service passwordlessly (the hook runs as
# whoever pushes, but the service runs as root). Written directly to
# /etc/sudoers.d, generated from the current user at setup time — the
# username is never stored in the git repo.
echo "$(whoami) ALL=(root) NOPASSWD: /usr/bin/systemctl restart lcdshowstatus.service" | sudo tee /etc/sudoers.d/lcdshowstatus > /dev/null
sudo chmod 440 /etc/sudoers.d/lcdshowstatus

echo "Bare repo ready at $GIT_DIR"
echo ""
echo "On your dev machine, add the remote and push once to populate the work tree:"
echo "  git remote add pi $(whoami)@$(hostname):$GIT_DIR"
echo "  git push pi main"
echo ""
echo "Then, back on the Pi, finish the one-time install (needs root):"
echo "  sudo cp $WORK_TREE/lcdshowstatus.service /etc/systemd/system/"
echo "  sudo systemctl daemon-reload"
echo "  sudo systemctl enable --now lcdshowstatus.service"
echo ""
echo "After that, every 'git push pi main' will update the work tree and restart the service."
