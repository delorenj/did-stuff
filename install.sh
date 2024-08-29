#!/bin/bash

# Colors and emojis for pretty output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
ROCKET='🚀'
SPARKLES='✨'
CHECK='✅'

# Function to ensure valid JSON in config file
ensure_valid_json() {
    if [ ! -s "$CONFIG_FILE" ] || ! jq empty "$CONFIG_FILE" 2>/dev/null; then
        echo '{"AI":{},"OpenAI":{},"AWS":{}}' > "$CONFIG_FILE"
    fi
}

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
echo -e "${YELLOW}Where would you like to install the configuration file?${NC}"
echo "1) Locally in the project root"
echo "2) Globally in your home directory"
read -p "Choose an option (1/2): " config_location_choice

if [ "$config_location_choice" = "1" ]; then
    CONFIG_FILE="$(pwd)/.git-commit-message-generator-config.json"
elif [ "$config_location_choice" = "2" ]; then
    CONFIG_FILE="$HOME/.git-commit-message-generator-config.json"
else
    echo -e "${YELLOW}Invalid choice. Defaulting to global installation.${NC}"
    CONFIG_FILE="$HOME/.git-commit-message-generator-config.json"
fi

if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${YELLOW}Creating configuration file...${NC}"
    cp git-config-message-generator-config.example.json "$CONFIG_FILE"
    echo -e "${GREEN}${CHECK} Configuration file created at $CONFIG_FILE${NC}"
else
    echo -e "${GREEN}${CHECK} Configuration file already exists${NC}"
    echo -e "${YELLOW}Do you want to recreate the configuration file? (y/N)${NC}"
    read -p "> " recreate_config
    if [[ $recreate_config =~ ^[Nn]$ ]]; then
        echo -e "${GREEN}${CHECK} Keeping existing configuration file${NC}"
        echo "Current configuration file contents:"
        cat "$CONFIG_FILE"
        echo "Configuration file path: $CONFIG_FILE"
    fi
fi

# Interactive configuration
if [[ $recreate_config =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Let's set up your AI provider:${NC}"
    echo -e "1) OpenAI"
    echo -e "2) AWS Bedrock"
    read -p "Choose your provider (1/2): " provider_choice

    if [ "$provider_choice" = "1" ]; then
        if [ -n "$OPENAI_API_KEY" ]; then
            echo -e "${GREEN}${CHECK} OpenAI API key found in environment${NC}"
            openai_key="$OPENAI_API_KEY"
        else
            read -p "Enter your OpenAI API key: " openai_key
            echo -e "${YELLOW}How would you like to store your OpenAI API key?${NC}"
            echo "1) Add to config file"
            echo "2) Add to shell profile"
            read -p "Choose an option (1/2): " key_storage_choice

            if [ "$key_storage_choice" = "1" ]; then
                # Update config file with OpenAI key
                ensure_valid_json
                jq '.AI.provider = "openai" | .AI.model_id = "gpt-3.5-turbo" | .OpenAI.api_key = $key' --arg key "$openai_key" "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
                echo -e "${GREEN}${CHECK} OpenAI API key added to config file${NC}"
            elif [ "$key_storage_choice" = "2" ]; then
                # Add to shell profile
                shell_profile="$HOME/.$(basename $SHELL)rc"
                echo "export OPENAI_API_KEY='$openai_key'" >> "$shell_profile"
                echo -e "${GREEN}${CHECK} OpenAI API key added to $shell_profile${NC}"
                echo -e "${YELLOW}Please restart your terminal or run 'source $shell_profile' to apply changes${NC}"
            else
                echo -e "${YELLOW}Invalid choice. OpenAI API key will not be stored.${NC}"
            fi
        fi
        echo -e "${GREEN}${CHECK} OpenAI configuration updated${NC}"
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
        ensure_valid_json
        jq '.AI.provider = "aws-bedrock" | .AI.model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0" | .AWS.profile_name = $profile' --arg profile "$aws_profile" "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
        echo -e "${GREEN}${CHECK} AWS Bedrock configuration updated${NC}"
    else
        echo -e "${YELLOW}Invalid choice. Exiting.${NC}"
        exit 1
    fi
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