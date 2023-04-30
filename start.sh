aria2c --allow-overwrite=true --auto-file-renaming=true \
       --check-integrity=true --continue=true --content-disposition-default-utf8=true --daemon=true \
       --disk-cache=40M --enable-rpc=true --force-save=true --http-accept-gzip=true \
       --max-connection-per-server=10 --max-concurrent-downloads=10 --max-file-not-found=0 --max-tries=20 \
       --min-split-size=10M --optimize-concurrent-downloads=true --reuse-uri=true \
       --rpc-max-request-size=1024M \
       --summary-interval=0 --user-agent=Wget/1.12 --disable-ipv6 & python3 -m bot
