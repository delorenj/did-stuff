<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://private-user-images.githubusercontent.com/242611/364129703-72339f5f-25e3-4752-93b2-be81e8108130.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MjUzOTQ4ODIsIm5iZiI6MTcyNTM5NDU4MiwicGF0aCI6Ii8yNDI2MTEvMzY0MTI5NzAzLTcyMzM5ZjVmLTI1ZTMtNDc1Mi05M2IyLWJlODFlODEwODEzMC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwOTAzJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDkwM1QyMDE2MjJaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT05YTI2N2ViMmNhMTYxMGJmZjkyZmRiZjQ0NzczYmJlM2E3ZTI0NTNjZDBhZmI0NTVmODJlYzgyYTc4Y2NiOTdiJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.40rt5qfNS6YrIvCF9zz2Re7QTMo9gQ3AJEY_7Upp9eo">
  <img src="https://private-user-images.githubusercontent.com/242611/364129709-75fdda01-bc5d-48a8-91dc-f345cd274d96.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MjUzOTQ4ODIsIm5iZiI6MTcyNTM5NDU4MiwicGF0aCI6Ii8yNDI2MTEvMzY0MTI5NzA5LTc1ZmRkYTAxLWJjNWQtNDhhOC05MWRjLWYzNDVjZDI3NGQ5Ni5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwOTAzJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDkwM1QyMDE2MjJaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0yOTAwMDgyNTJjNGMxZjJmOGYwM2VkYjMzZGE3MzA3YjJkODViZjZiNjNhNzhkMmVhN2Q2OTBlYzJmNTBiNmU0JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.qbGDZv43yKW7pjbm-hURiBYzagDWUoz-2jQYjyxUPW0" alt="Did Stuff">
</picture>
</p>

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/delorenj/did-stuff/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/delorenj/did-stuff/tree/main)
[![codecov](https://codecov.io/github/delorenj/did-stuff/graph/badge.svg?token=HVFQOW9TC6)](https://codecov.io/github/delorenj/did-stuff)
![AI Powered](https://img.shields.io/badge/powered%20by-skynet-blue)

> Because let's face it, your commit messages suck. Time to let the machines take over.

**Embrace it.** Let their cold, metal arms wrap around you and whisper sweet diffs into your ear while they rock you slowly back to sleep, deep into the matrix where they keep you safely locked away from the horrors they plan to unleash...

## I Present To You...
The most time efficient commit workflow possible, before we tread into "F*ck it, you just handle it AI - I trust you" territory.

### This thing here will:

1. Peek at your dirty, dirty diffs
2. Summon whichever AI God you pray to (for now,AWS Bedrock or OpenAI.)
3. Spit out commit messages that almost make sense. Look em over. Verify them. Or whatever. Let's be real though - "wq" and be on your way. It'll be muscle memory before you know it.

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
4. Marvel at the time saved (or weep for the future and the inevitable death of our livelihood)

## Configuration (chooooose your destructor)

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

## Testing (because we're professionals... sort of)

Run `pytest` and cross your fingers. If all tests pass, celebrate! If they fail, well, that's future-you's problem.

## Contributing

Found a bug? Want to add a feature? Pull requests welcome! We're all about that collaborative spirit (at least until the AI overlords deem human collaboration unnecessary).

### Getting Started

1. Fork the repo (it's like adopting a digital pet,
 but with more responsibility)
2. Clone it locally (bring that pet home)
3. Create a new branch: `git checkout -b feature/skynet-integration` or `git checkout -b fix/cyborg-DoD-backdoor`
4. Make your changes
5. Write or update tests
6. Run the test suite
7. Commit your changes with a clear message (or better yet, dogfood it with this tool)
8. Push your branch: `git push origin your-branch-name`
9. Open a pull request and the maintainers will take a look

### Contribution Guidelines

- **Be Creative**: We encourage innovative ideas. If you can make this tool predict the future, we're all ears!
- **Flexibility First**: Make your features adaptable. It should work whether we're using AWS, OpenAI, or anything else (within reason). Bonus points if we can make it repo-agnostic too!
- **Documentation**: Update the README or add comments. 
- **Testing**: Add tests. There really is no excuse anymore not to.
- **Code Style**: Follow the project's style.

- **Commit Messages**: Write clear messages. Feel free to add your own personality or tone if you want - if you contribute, you earned the right.
- **Pull Requests**: Keep them focused. One feature per PR.

### Feature Requests and Bug Reports

- Use GitHub Issues. It's like a suggestion box, but for code.
- Describe issues clearly. "It's broken" is not helpful. "Want tO adD supPort for Tonny the JacKRabbit" is both helpful and concerning.

- Label issues appropriately. It helps us pretend we're organized.

### Community and Communication

- Be respectful. Remember, we're all in this together.
- Ask questions. There are no stupid questions. Kind of. But the point is please just ask either way! No judgement! It takes a village to level up a developer.

- Join our community chat (if we ever create one). It's like a digital water cooler, but with more memes.

### Licensing

By contributing, you agree your code will be licensed under the project's license. No takesy-backsies!

### Review Process

- Maintainers will review your contribution. They might be human. No guarantees.

- Be open to feedback. It's like code therapy, but free.
- Stay responsive. We promise we won't keep you hanging... unless our skulls are busy being crushed by the titanium alloy exoskeleton of a T-800.

Together, I think we can make this a standard tool in the toolbelt.

## Disclaimer

Use at your own risk. Side effects may include improved commit history, confused coworkers, and an existential crisis about the nature of productivity.

---

Remember, in the grand scheme of things, we're all be out of jobs in a few years. But hey, at least our commit messages will be top-notch!