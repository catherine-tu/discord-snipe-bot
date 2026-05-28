# 📸 Discord Snipe Bot

A simple Discord bot that tracks “snipes” between members using Google Sheets as a database.

---

## 🚀 Features

- `!sniped @user` → records a snipe event
  - +1 to sender’s **snipes**
  - +1 to target’s **got sniped**
- `!stats [@user]` → shows personal stats
- `!revoke @user snipe` → removes a snipe
- `!revoke @user gotsniped` → removes a “got sniped”
- `!leaderboard` → shows top snipers and most-sniped users

All data is stored in **Google Sheets**.

---

## 📊 Google Sheet Structure

Your sheet should look like this:

| Name  | Sniped | Got Sniped |
| ----- | ------ | ---------- |
| Cat   | 5      | 2          |
| Alex  | 3      | 7          |
| Chris | 0      | 5          |
| Sean  | 1      | 3          |
| Laura | 2      | 2          |

- Column A → Name (mapped from Discord ID)
- Column B → Snipes given
- Column C → Times got sniped

---

## ⚙️ Setup Instructions

### 1. Clone the project

```bash
git clone <your-repo-url>
cd discord-snipe-bot
```
