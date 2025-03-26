#!bin/bash

if [ -d "/home/frappe/frappe-bench/apps/frappe" ]; then
    echo "Bench already exists, skipping init"
    cd frappe-bench
    bench start
else
    echo "Creating new bench..."
fi

export PATH="${NVM_DIR}/versions/node/v${NODE_VERSION_DEVELOP}/bin/:${PATH}"

bench init --skip-redis-config-generation frappe-bench

cd frappe-bench

# Use containers instead of localhost
bench set-mariadb-host mariadb
bench set-redis-cache-host redis:6379
bench set-redis-queue-host redis:6379
bench set-redis-socketio-host redis:6379

# Remove redis, watch from Procfile
sed -i '/redis/d' ./Procfile
sed -i '/watch/d' ./Procfile

bench get-app lms

bench new-site lms.localhost \
--force \
--mariadb-root-password 123 \
--admin-password admin \
--no-mariadb-socket

bench --site lms.localhost install-app lms
bench --site lms.localhost set-config developer_mode 1

# Configure Google OAuth2 if environment variables are set
if [ ! -z "$GOOGLE_OAUTH2_CLIENT_ID" ] && [ ! -z "$GOOGLE_OAUTH2_CLIENT_SECRET" ]; then
    echo "Configuring Google OAuth2..."
    bench --site lms.localhost set-config google_oauth2_client_id "$GOOGLE_OAUTH2_CLIENT_ID"
    bench --site lms.localhost set-config google_oauth2_client_secret "$GOOGLE_OAUTH2_CLIENT_SECRET"
    bench --site lms.localhost set-config google_oauth2_redirect_uri "$GOOGLE_OAUTH2_REDIRECT_URI"
fi

bench --site lms.localhost clear-cache
bench use lms.localhost

bench start
