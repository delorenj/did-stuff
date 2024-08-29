#!/bin/bash

# Colors and emojis for pretty output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
ROCKET='🚀'
SPARKLES='✨'
CHECK='✅'

echo -e "${YELLOW}${ROCKET} Installing the DeLoOps Did Stuff hook! ${ROCKET}${NC}"

# Check for Python and pip
if ! command -v python3 &> /dev/null || ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}Installing Python and pip...${NC}"
    # Add commands to install Python and pip based on the OS
fi

# Install required packages
echo -e "${YELLOW}Installing required Python packages...${NC}"
pip3 install -q --no-cache-dir -r requirements.txt

# Copy configuration file
CONFIG_FILE="$HOME/.git-commit-message-generator-config.json"
if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${YELLOW}Creating configuration file...${NC}"
    cp git-config-message-generator-config.example.json "$CONFIG_FILE"
    echo -e "${GREEN}${CHECK} Configuration file created at $CONFIG_FILE${NC}"
else
    echo -e "${GREEN}${CHECK} Configuration file already exists${NC}"
fi

# Interactive configuration
echo -e "${YELLOW}Let's set up your AI provider:${NC}"
echo -e "1) OpenAI"
echo -e "2) AWS Bedrock"
read -p "Choose your provider (1/2): " provider_choice

if [ "$provider_choice" = "1" ]; then
    read -p "Enter your OpenAI API key: " openai_key
    # Update config file with OpenAI key
elif [ "$provider_choice" = "2" ]; then
    if command -v aws &> /dev/null; then
        echo -e "${YELLOW}Available AWS profiles:${NC}"
        aws configure list-profiles | cat -n
        echo -e "${YELLOW}Enter the number of the profile you want to use, or type a new profile name:${NC}"
        read -p "> " aws_profile_choice
        if [[ "$aws_profile_choice" =~ ^[0-9]+$ ]]; then
            aws_profile=$(aws configure list-profiles | sed -n "${aws_profile_choice}p")
        else
            aws_profile=$aws_profile_choice
        fi
        echo -e "${GREEN}Selected AWS profile: $aws_profile${NC}"
    else
        read -p "Enter your AWS profile name: " aws_profile
    fi
    # Update config file with AWS profile
else
    echo -e "${YELLOW}Invalid choice. Exiting.${NC}"
    exit 1
fi

# Set up Git hook
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${YELLOW}Setting up Git hook...${NC}"
    cp src/prepare-commit-msg "$(git rev-parse --git-dir)/hooks/"
    chmod +x "$(git rev-parse --git-dir)/hooks/prepare-commit-msg"
    echo -e "${GREEN}${CHECK} Git hook installed successfully${NC}"
else
    echo -e "${YELLOW}Not in a Git repository. You can manually set up the Git hook later.${NC}"
fi

echo -e "${GREEN}${SPARKLES} Installation complete! Go do stuff! ${SPARKLES}${NC}"