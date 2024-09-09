<p align="center" style="width: 100%; background-color: #13191d;">
<picture style="width: 100%;">
  <source media="(prefers-color-scheme: dark)" srcset="https://private-user-images.githubusercontent.com/242611/364165903-08980893-2898-43ca-89b7-23c35c4bd5d7.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MjU4OTA5MTAsIm5iZiI6MTcyNTg5MDYxMCwicGF0aCI6Ii8yNDI2MTEvMzY0MTY1OTAzLTA4OTgwODkzLTI4OTgtNDNjYS04OWI3LTIzYzM1YzRiZDVkNy5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwOTA5JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDkwOVQxNDAzMzBaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT03MTEyZThjNDg2N2IxYjczNWZkMmVkZWZmMmI5YjM2ZDM4OTgyZGJjNmE3NmI3M2Y2NDY0Y2RlYmM3YWIwZTY3JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.RehRrtfoo2_MW1eNfOKQTq7PHu9x61vHfVTWuCU9QdY">
  <img src="https://private-user-images.githubusercontent.com/242611/364165903-08980893-2898-43ca-89b7-23c35c4bd5d7.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MjU4OTA5MTAsIm5iZiI6MTcyNTg5MDYxMCwicGF0aCI6Ii8yNDI2MTEvMzY0MTY1OTAzLTA4OTgwODkzLTI4OTgtNDNjYS04OWI3LTIzYzM1YzRiZDVkNy5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwOTA5JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDkwOVQxNDAzMzBaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT03MTEyZThjNDg2N2IxYjczNWZkMmVkZWZmMmI5YjM2ZDM4OTgyZGJjNmE3NmI3M2Y2NDY0Y2RlYmM3YWIwZTY3JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.RehRrtfoo2_MW1eNfOKQTq7PHu9x61vHfVTWuCU9QdY" alt="Did Stuff" style="width: 100%;">
</picture>
</p>

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/delorenj/did-stuff/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/delorenj/did-stuff/tree/main)
[![codecov](https://codecov.io/github/delorenj/did-stuff/graph/badge.svg?token=HVFQOW9TC6)](https://codecov.io/github/delorenj/did-stuff)
![AI Powered](https://img.shields.io/badge/powered%20by-skynet-blue)
![made with love for](https://img.shields.io/badge/made%20with%20love%20for-Justworks-blue)
> Because let's face it, your commit messages suck. Time to let the machines take over.

**Embrace it.** Let their cold, metal arms wrap around you and whisper sweet diffs into your ear while they rock you slowly back to sleep, deep into the matrix where they keep you safely locked away from the horrors they plan to unleash...

## I Present To You...
The most time efficient commit workflow possible, before we tread into "Eh, you just handle it AI - I trust you" territory.

### This thing here will:

1. Peek at your dirty, dirty diffs
2. Summon whichever AI God you pray to (for now,AWS Bedrock or OpenAI.)
3. Spit out commit messages that almost make sense. Look em over. Verify them. Or whatever. Let's be real though - "wq" and be on your way. It'll be muscle memory before you know it.

## Check out these :foot:-churrs:

- 🧠 Uses AI to understand your diff at a high level (probably better than you do)
- 🎭 Supports both AWS Bedrock and OpenAI (because if I release this to the wild, people will complain that my free gift wasn't good enough)
- 🌈 Generates commit messages that are informative, concise, and will never be "too tired" and just say "Did stuff"
- 🚀 Comes with a fancy install script (because who doesn't love more automation?)
- 🧪 Includes tests!

## Installation

1. Clone this repo
2. Run `./install.sh`
3. Follow the prompts to set up your AI provider
4. Watch as your Git hooks are magically set up

## Usage

1. Code
2. `git add .`
3. `git commit`

## Configuration

The install script will create a config file at `~/.git-commit-message-generator-config.json`. If you're feeling frisky, you can edit it manually:

#### Configured for OpenAI

> Note: If you choose OpenAI, you must ensure `OPENAI_API_KEY` is set in your environment variables.

```json
{
  "AI": {
    "provider": "openai",
    "model_id": "gpt-3.5-turbo",
    "max_tokens": 300,
    "temperature": 0.3
  }
}
```

#### Configured for AWS Bedrock (Claude 3.5 Sonnet)

> Note: If you choose AWS Bedrock, you must ensure your AWS credentials are configured and you have access to the model requested.

If your company uses SSO make sure your session is logged in using `aws sso login`

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

## Testing (because we're professionals)

Run `pytest` and cross your fingers.

## Contributing

Found a bug? Want to add a feature? Pull requests welcome! We're all about that collaborative spirit (at least until the AI entities deem human collaboration unnecessary).

### Getting Started

1. Fork the repo (it's like adopting a digital pet,
 but with more responsibility)
2. Clone it locally
3. Create a new branch: `git checkout -b feature/skynet-integration` or `git checkout -b fix/cyborg-DoD-backdoor`
4. Make your changes
5. Write or update tests
6. Run the test suite
7. Commit your changes with a clear message (or better yet, dogfood it with this tool)
8. Push your branch: `git push origin your-branch-name`
9. Open a pull request

### Contribution Guidelines

- **Be Creative**: We encourage innovative ideas.
- **Flexibility First**: Make your features adaptable. It should work whether we're using AWS, OpenAI, or anything else (within reason). Bonus points if we can make it repo-agnostic too!
- **Documentation**: Update the README or add comments. 
- **Testing**: Add tests. There really is no excuse anymore not to.
- **Code Style**: Follow the project's style.

- **Commit Messages**: Whatever
- **Pull Requests**: Keep them focused. One feature per PR.

### Feature Requests and Bug Reports

- Use GitHub Issues.
- Describe issues clearly. "It's broken" is not helpful.
- Label issues appropriately.

### Community and Communication

- Be respectful. Remember, we're all in this together.
- Ask questions. There are no stupid questions. Kind of. But the point is please just ask either way! No judgement! It takes a village to level up a developer.
- Join our community chat (if we ever create one).

### Licensing

By contributing, you agree your code will be licensed under the project's license.

### Review Process

- Maintainers will review your contribution. They might be human. No guarantees.
- Be open to feedback.
- Stay responsive. We promise we won't keep you hanging... unless our skulls are busy being crushed by the titanium alloy exoskeleton of a T-800.

---

Remember, in the grand scheme of things, we're all be out of jobs in a few years. But hey, at least our commit messages will be top-notch!
