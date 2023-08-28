pyinstaller --name=resilio_sync_tray --onefile --noconsole --add-data="resilio_sync_tray/resilio-sync-icon.png:." resilio_sync_tray/__main__.py \
    && pyinstaller resilio_sync_tray.spec
