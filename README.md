# 🤖💬 git commit -m "Did stuff"

![Commit Like a Boss](https://img.shields.io/badge/commit%20like%20a-boss-brightgreen)
![AI Powered](https://img.shields.io/badge/powered%20by-skynet-blue)
![Works on my Machine](https://img.shields.io/badge/works%20on-my%20machine-red)

> Because let's face it, your commit messages suck. Time to let the machines take over. 

**Embrace it.** Let their cold, metal arms wrap around you and whisper sweet diffs into your ear while they rock you slowly back to sleep, deep into the matrix where they keep you safely locked away from the horrors they plan to unleash...

## What fresh hell is this?

It's 3am. You were in the zone for so long that it's 3:01am by the time the `git diff` output finishes pumping out the deluge of changes you made. What did you even do? Did I really touch that many files? Hm, I think I see what did..."Fixed stuff".

## Perhaps this is familiar?

It didn't take to realize that I could just copy the diff output and paste it into ChatGPT to get a pretty accurate commit message. But then I started thinking, "JFC, what at huge pain in the ass this is - typing commands in the terminal, switching between windows, pasting the output".

Then I realized I could just pipe the diff output into pbcopy. That saved me like 20 seconds! But I still had to spend another 20 seconds fiddling around in Claude or whatever. I don't have time for this s#$@! What is this, 2022? 

Alas, I present to you the most time efficient commit workflow possible, before we tread into "F$*@ it, you just handle it, AI - I trust you" territory.

### This thing here will:

1. Peek at your dirty, dirty diffs
2. Summon whichever AI God you pray to (AWS Bedrock or OpenAI. Yes, I can add more - chill buddy I have a day job and 3 kids.)
3. Spit out commit messages that almost make sense. Look em over. Verify them. Or whatever. Let's be real though - your lazy ass is just going to "wq" and be on your way. It'll be muscle memory before you know it.

## Features that'll make you question reality

- 🧠 Uses AI to understand your diff at a high level (probably better than you do)
- 🎭 Supports both AWS Bedrock and OpenAI (because if I release this to the wild, people will complain that my free gift wasn't good enough)
- 🌈 Generates commit messages that are informative, concise, and will never be "too tired" and just say "Did stuff"

## Installation

1. Clone this repo (or summon it via arcane rituals)
2. `pip install -r requirements.txt` (sacrifice a rubber duck for good measure)
3. Copy `config.example.json` to `~/.git-commit-message-config.json`
4. Edit the config file with your AI provider details (blood oath required)
5. `chmod +x prepare-commit-msg.aws-bedrock.llm-summary`
6. `ln -s /path/to/prepare-commit-msg.aws-bedrock.llm-summary /path/to/your/repo/.git/hooks/prepare-commit-msg`

## Usage (if you dare)

1. Code like your life depends on it
2. `git add .` (embrace the chaos)
3. `git commit` (and watch the magic/horror unfold)

## Configuration (choooose your destructor)

```json
{
  "AI": {
    "provider": "openai", // or "aws-bedrock" if you're feeling adventurous
    "model_id": "gpt-3.5-turbo", // or "claude-3-5-sonnet-20240620" for AWS
    "max_tokens": 300, // adjust for verbosity or brevity
    "temperature": 0.3 // higher for chaos, lower for boringness
  },
  "AWS": {
    "profile_name": "your-aws-profile" // if you're going the AWS route
  },
  "OpenAI": {
    "api_key": "your-openai-api-key" // for the OpenAI aficionados
  }
}
```

## Disclaimer

Use at your own risk. Side effects may include improved commit history, confused coworkers, and no more "Did stuff" commit messages.

## Contributing

Found a bug? Want to add a feature? Pull requests welcome!

I figure we have at least one more good year left in us before the corporate world realizes they can just fire everyone and replace us with AI agents.

---
