# Instagram Tracker 📈

Track changes in an Instagram profile's followers and following lists over time — even for private accounts (if you follow them). Built with Python + Instaloader, runs locally on your machine, and saves clean changelogs after each run.

---

## ✅ Features

- Detects:
  - ➕ New followers
  - ➖ Lost followers
  - ➕ Newly followed accounts
  - ➖ Unfollowed accounts
- Saves a **timestamped changelog** (`.md`) per run
- All users are output as **clickable Instagram links**
- Summary stats with **net gain/loss**
- Optional `--dry-run` mode to preview changes without saving
- Fully local and private — no remote logging or storage

---

## ⚙️ Setup

### 1. Clone this repo

```bash
git clone https://github.com/your-username/instagram-tracker.git
cd instagram-tracker
```

### 2. Create virtual environment (optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> Or manually:
```bash
pip install instaloader python-dotenv
```

---

## 🔐 Login to Instagram (one-time setup)

To track followers/following, you must be logged into an account that can view the target profile. Run:

```bash
instaloader --login=your_username
```

This will:
- Prompt for your IG password
- Ask for 2FA code if enabled
- Save a session file locally (usually at `~/.config/instaloader/session-your_username`)

If your session ever **expires or breaks**, just re-run the above command to refresh it.

> 💡 Tip: To avoid hardcoding usernames, we use a `.env` file.

Create one like this:

```bash
cp .env.example .env
```

Then edit `.env` with your info:

```env
TARGET_USERNAME=target_ig_username
YOUR_IG_USERNAME=your_ig_username
```

---

## 🚀 Usage

### Track a profile:

```bash
python3 main.py
```

Each run will:
- Compare current followers/following to the last saved snapshot
- Print changes in the terminal
- Save the latest state to disk
- Save a Markdown changelog with clickable profile links

### Preview changes only (no saving):

```bash
python3 main.py --dry-run
```

---

## 📁 Project Structure

```
instagram-tracker/
├── main.py         # Main script
├── .env                                 # Your actual config (not committed)
├── .env.example                         # Shared template
├── .gitignore
└── instagram_tracking/
    ├── followers.json                   # Latest followers list
    ├── following.json                   # Latest following list
    └── history/
        └── 2025-07-18_17-48-15_ig_username.md  # Timestamped changelog
```

---

## 🧼 Reset Snapshot (optional)

If you ever want to clear the saved snapshot and start fresh:

```bash
rm instagram_tracking/*.json
```

---

## 🤝 Credits

- Built with ❤️ using [Instaloader](https://instaloader.github.io/)

