import qbittorrentapi
import os

MAGNET_RECORD_FILE = "added_magnets.txt"

def load_existing_keys():
    """Load previously added magnet key IDs from a file."""
    if not os.path.exists(MAGNET_RECORD_FILE):
        return set()
    
    with open(MAGNET_RECORD_FILE, "r") as file:
        return set(line.strip() for line in file)

def save_new_keys(key_ids):
    """Append new magnet key IDs to the record file."""
    with open(MAGNET_RECORD_FILE, "a") as file:
        file.write(key_ids + "\n")

def add_magnet_links(
    magnet_link,
    key_id,
    host="localhost",
    port=8080,
    username="admin",
    password="adminadmin",
    save_path=None
):
    """
    Adds a single magnet link to qBittorrent while avoiding duplicates based on key_id.

    :param magnet_link: A single magnet link to add.
    :param key_id: Unique ID for the magnet link to track.
    :param host: qBittorrent Web UI host (default: localhost).
    :param port: qBittorrent Web UI port (default: 8080).
    :param username: qBittorrent username (default: admin).
    :param password: qBittorrent password (default: adminadmin).
    :param save_path: Directory where torrents should be saved (default: qBittorrent's default).
    """
    existing_keys = load_existing_keys()

    if key_id in existing_keys:
        print(f"Magnet with key_id '{key_id}' is already added.")
        return

    try:
        qb = qbittorrentapi.Client(host=host, port=port, username=username, password=password)
        qb.auth_log_in()
        print("Connected to qBittorrent.")

        qb.torrents_add(urls=magnet_link, save_path=save_path)
        print(f"Added: {magnet_link} {'to ' + save_path if save_path else 'to default directory'}")

        save_new_keys(key_id)  # Save the newly added key_id
        print("Magnet link added and key_id recorded.")
    except Exception as e:
        print(f"Error: {e}")

# Run only if this script is executed directly
if __name__ == "__main__":
    magnet_link = "magnet:?xt=urn:btih:EXAMPLE1..."
    key_id = "unique_torrent_key"  # Unique ID for this magnet link

    save_directory = "/path/to/download/folder"

    add_magnet_links(magnet_link, key_id, save_path=save_directory)
