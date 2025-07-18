import instaloader
import json
import os
import argparse
from datetime import datetime
from typing import List
from dotenv import load_dotenv

try:
    from pyfiglet import Figlet
    f = Figlet(font='cybermedium')
    print(f.renderText('ig-tracker'))
except ImportError:
    print("\n=== IG TRACKER ===\n")


# Load environment variables
load_dotenv()
TARGET_USERNAME = os.getenv("TARGET_USERNAME")
YOUR_IG_USERNAME = os.getenv("YOUR_IG_USERNAME")

DATA_DIR = 'instagram_tracking'
HISTORY_DIR = os.path.join(DATA_DIR, 'history')
FOLLOWERS_FILE = os.path.join(DATA_DIR, 'followers.json')
FOLLOWING_FILE = os.path.join(DATA_DIR, 'following.json')

def save_json(filename: str, data: List[str]):
    with open(filename, 'w') as f:
        json.dump(sorted(data), f, indent=2)

def load_json(filename: str) -> List[str]:
    if os.path.exists(filename):
        with open(filename) as f:
            return json.load(f)
    return []

def linkify(users: List[str]) -> List[str]:
    return [f"https://instagram.com/{u}" for u in sorted(users)]

def compare(new: List[str], old: List[str]):
    added = sorted(list(set(new) - set(old)))
    removed = sorted(list(set(old) - set(new)))
    return added, removed

def display_and_log(label: str, added: List[str], removed: List[str], log_lines: List[str]):
    print(f"\n📈 {label.upper()} CHANGES")
    print("➕ Added:", "\n  " + "\n  ".join(linkify(added)) if added else "None")
    print("➖ Removed:", "\n  " + "\n  ".join(linkify(removed)) if removed else "None")

    log_lines.append(f"## {label.capitalize()} changes")
    log_lines.append(f"**Added ({len(added)}):**")
    log_lines.extend([f"- {u}" for u in linkify(added)] or ["- None"])
    log_lines.append(f"**Removed ({len(removed)}):**")
    log_lines.extend([f"- {u}" for u in linkify(removed)] or ["- None"])
    log_lines.append("")

def write_changelog(log_lines: List[str], timestamp: str):
    os.makedirs(HISTORY_DIR, exist_ok=True)
    filename = os.path.join(HISTORY_DIR, f"{timestamp}_{TARGET_USERNAME}.md")
    with open(filename, "w") as f:
        f.write("\n".join(log_lines))
    print(f"\n📝 Log saved to: {filename}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', help="Preview changes without saving")
    args = parser.parse_args()

    if not TARGET_USERNAME or not YOUR_IG_USERNAME:
        print("❌ Error: Please set TARGET_USERNAME and YOUR_IG_USERNAME in your .env file.")
        return

    os.makedirs(DATA_DIR, exist_ok=True)
    loader = instaloader.Instaloader()

    print("🔐 Loading saved session...")
    try:
        loader.load_session_from_file(YOUR_IG_USERNAME)
        print(f"✅ Logged in as @{YOUR_IG_USERNAME}")
    except Exception as e:
        print(f"❌ Failed to load session: {e}")
        return

    print(f"\n📦 Fetching profile for @{TARGET_USERNAME}...")
    try:
        profile = instaloader.Profile.from_username(loader.context, TARGET_USERNAME)
        print(f"✅ Profile found: {profile.full_name or TARGET_USERNAME}")
    except Exception as e:
        print(f"❌ Could not load profile: {e}")
        return

    try:
        print("📥 Getting followers...")
        current_followers = [f.username for f in profile.get_followers()]
    except Exception as e:
        print(f"⚠️ Could not fetch followers: {e}")
        current_followers = []

    try:
        print("📥 Getting following...")
        current_following = [f.username for f in profile.get_followees()]
    except Exception as e:
        print(f"⚠️ Could not fetch following: {e}")
        current_following = []

    if not current_followers and not current_following:
        print("⚠️ No follower/following data retrieved. Aborting comparison.")
        return

    print("💾 Comparing with last saved snapshot...")
    old_followers = load_json(FOLLOWERS_FILE)
    old_following = load_json(FOLLOWING_FILE)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_lines = [f"# Instagram Tracker Report – {timestamp}", ""]

    new_followers, lost_followers = compare(current_followers, old_followers)
    new_following, unfollowed = compare(current_following, old_following)

    display_and_log("followers", new_followers, lost_followers, log_lines)
    display_and_log("following", new_following, unfollowed, log_lines)

    print("\n📊 Summary:")
    print(f"👥 Followers: +{len(new_followers)}, -{len(lost_followers)}, Net: {len(new_followers) - len(lost_followers)}")
    print(f"➡️ Following: +{len(new_following)}, -{len(unfollowed)}, Net: {len(new_following) - len(unfollowed)}")

    log_lines.append("## Summary")
    log_lines.append(f"- Followers: +{len(new_followers)}, -{len(lost_followers)}, Net: {len(new_followers) - len(lost_followers)}")
    log_lines.append(f"- Following: +{len(new_following)}, -{len(unfollowed)}, Net: {len(new_following) - len(unfollowed)}")
    log_lines.append("")

    if args.dry_run:
        print("\n🚫 Dry run mode: no files saved.")
    else:
        save_json(FOLLOWERS_FILE, current_followers)
        save_json(FOLLOWING_FILE, current_following)
        write_changelog(log_lines, timestamp)
        print(f"\n✅ Tracking complete! Data saved to '{DATA_DIR}/' at {timestamp}")

if __name__ == "__main__":
    main()

