# Discord WowAudit Sim Bot

A simple Discord bot that allows raiders to submit their Raidbots Droptimizer reports and automatically upload their BiS wishlists to WowAudit.

---

## Features

- `/uploadsim link:<Raidbots report link>` command
- Validates that the posted link is a real Raidbots sim report
- Downloads the SimC input from the Raidbots report
- Uploads the SimC string directly to WowAudit
- Only users with the roles `Probe Raider` or `Raider` can use the command
- Replies directly in the channel with success or error messages

---

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://your-repo-link.git
cd discord-wowaudit-bot
```
