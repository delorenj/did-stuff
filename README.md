# 🤖💬 git commit -m "Did stuff"

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/delorenj/did-stuff/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/delorenj/did-stuff/tree/main)
[![codecov](https://codecov.io/github/delorenj/did-stuff/graph/badge.svg?token=HVFQOW9TC6)](https://codecov.io/github/delorenj/did-stuff)
![AI Powered](https://img.shields.io/badge/powered%20by-skynet-blue)

> Because let's face it, your commit messages suck. Time to let the machines take over.


**Embrace it.** Let their cold, metal arms wrap around you and whisper sweet diffs into your ear while they rock you slowly back to sleep, deep into the matrix where they keep you safely locked away from the horrors they plan to unleash...

## What in the fresh hell is this?

It's 3am. You were in the zone for so long that it's 3:01am by the time the `git diff` output finishes pumping out the deluge of changes you made. What did you even do? Did I really touch that many files? Hm, I think I see what did..."Fixed stuff".

## Perhaps this is familiar?

It didn't take to realize that I could just copy the diff output and paste it into ChatGPT to get a pretty accurate commit message. But then I started thinking, "JFC, what at huge pain in the ass this is - typing commands in the terminal, switching between windows, pasting the output".

Then I realized I could just pipe the diff output into pbcopy. That saved me like 20 seconds! But I still had to spend another 20 seconds fiddling around in Claude or whatever. I don't have time for this s#$@! What is this, 2022? 

Alas, I present to you the most time efficient commit workflow possible, before we tread into "F$*@ it, you just handle it, AI - I trust you" territory.

### This thing here will:

1. Peek at your dirty, dirty diffs
2. Summon whichever AI God you pray to (AWS Bedrock or OpenAI. Yes, I can add more - chill buddy I have a day job and 3 kids.)
3. Spit out commit messages that almost make sense. Look em over. Verify them. Or whatever. Let's be real though - your lazy ass is just going to "wq" and be on your way. It'll be muscle memory before you know it.

## Check out these :foot:-churrs:

- 🧠 Uses AI to understand your diff at a high level (probably better than you do)
- 🎭 Supports both AWS Bedrock and OpenAI (because if I release this to the wild, people will complain that my free gift wasn't good enough)
- 🌈 Generates commit messages that are informative, concise, and will never be "too tired" and just say "Did stuff"
- 🚀 Comes with a fancy install script (because who doesn't love more automation?)
- 🧪 Includes tests (they probably work, who knows?)

## Installation

1. Clone this repo
2. Run `./install.sh`
3. Follow the prompts to set up your AI provider
4. Watch as your Git hooks are magically set up

## Usage

1. Code, like normal. Nothing to see here.
2. `git add .`
3. `git commit`
4. Marvel at the time saved (or weep for the future and the inevitable death of our livelyhood)

## Configuration (chooooose your destructor)

The install script will create a config file at `~/.git-commit-message-generator-config.json`. If you're feeling brave (or foolish), you can edit it manually:

#### Configured for OpenAI

> Note: If you choose OpenAI, you must ensure `OPENAI_API_KEY` is set in your environment variables.

```json
{
  "AI": {
    "provider": "openai", // or "aws-bedrock" if you're feeling adventurous
    "model_id": "gpt-3.5-turbo", // or "anthropic.claude-v2" for AWS
    "max_tokens": 300, // adjust for verbosity or brevity
    "temperature": 0.3 // higher for chaos, lower for boringness
  }
}
```

#### Configured for AWS Bedrock (Claude 3.5 Sonnet)

> Note: If you choose AWS Bedrock, you must ensure your AWS credentials are configured (and logged in if your company uses SSO).

```json
{
  "AI": {
    "provider": "aws-bedrock",
    "model_id": "anthropic.claude-3-5-sonnet-20240620-v1:0",
    "max_tokens": 300,
    "temperature": 0.3
  },
  "AWS": {
    "profile_name": "your-aws-profile-name"
  }
}
```

## Testing (because we're professionals... sort of)

Run `pytest` and cross your fingers. If all tests pass, celebrate! If they fail, well, that's future-you's problem.

## Disclaimer

Use at your own risk. Side effects may include improved commit history, confused coworkers, and an existential crisis about the nature of productivity.

## Contributing

Found a bug? Want to add a feature? Pull requests welcome!

I figure we have at least one more good year left in us before the corporate world realizes they can just fire everyone and replace us with AI agents. Make it count!

---

Remember, in the grand scheme of things, we're all just sacks of unsanitary meat trying to make sense of a bunch of 1s and 0s. Might as well let the machines help us along the way.