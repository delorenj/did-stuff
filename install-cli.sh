#!/bin/bash

# Colors and emojis for pretty output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
ROCKET='🚀'
SPARKLES='✨'
CHECK='✅'

# Configuration file paths
LOCAL_CONFIG_PATH="$(pwd)/.git-commit-message-generator-config.json"
GLOBAL_CONFIG_PATH="$HOME/.git-commit-message-generator-config.json"

# Function to ensure valid JSON in config file
ensure_valid_json() {
    local config_file="$1"
    if [ ! -s "$config_file" ] || ! jq empty "$config_file" 2>/dev/null; then
        echo '{"AI":{},"OpenAI":{},"AWS":{}}' > "$config_file"
    fi
}

# Function to update config file
update_config() {
    local config_file="$1"
    local provider="$2"
    local key="$3"
    local value="$4"
    
    ensure_valid_json "$config_file"
    if [ "$provider" = "OpenAI" ]; then
        jq --arg provider "$provider" --arg key "$key" --arg value "$value" \
           '.AI.provider = "openai" | .AI.model_id = "gpt-3.5-turbo" | .OpenAI[$key] = $value' \
           "$config_file" > "$config_file.tmp" && mv "$config_file.tmp" "$config_file"
    elif [ "$provider" = "AWS" ]; then
        jq --arg provider "$provider" --arg key "$key" --arg value "$value" \
           '.AI.provider = "aws-bedrock" | .AI.model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0" | .AWS[$key] = $value' \
           "$config_file" > "$config_file.tmp" && mv "$config_file.tmp" "$config_file"
    fi
}

# Function to check and install dependencies
check_and_install_dependencies() {
    if ! command -v python3 &> /dev/null || ! command -v pip3 &> /dev/null; then
        echo -e "${YELLOW}Installing Python and pip...${NC}"
        # Add commands to install Python and pip based on the OS
    fi

    echo -e "${YELLOW}Installing required Python packages...${NC}"
    pip3 install -q --no-cache-dir -r requirements.txt
}

# Function to set up configuration file
setup_config_file() {
    echo -e "${YELLOW}Where would you like to install the configuration file?${NC}"
    echo "1) Locally in the project root"
    echo "2) Globally in your home directory"
    read -p "Choose an option (1/2): " config_location_choice

    if [ "$config_location_choice" = "1" ]; then
        CONFIG_FILE="$LOCAL_CONFIG_PATH"
    elif [ "$config_location_choice" = "2" ]; then
        CONFIG_FILE="$GLOBAL_CONFIG_PATH"
    else
        echo -e "${YELLOW}Invalid choice. Defaulting to global installation.${NC}"
        CONFIG_FILE="$GLOBAL_CONFIG_PATH"
    fi

    if [ ! -f "$CONFIG_FILE" ]; then
        echo -e "${YELLOW}Creating configuration file...${NC}"
        cp git-config-message-generator-config.example.json "$CONFIG_FILE"
        echo -e "${GREEN}${CHECK} Configuration file created at $CONFIG_FILE${NC}"
    else
        echo -e "${GREEN}${CHECK} Configuration file already exists${NC}"
        echo -e "${YELLOW}Do you want to recreate the configuration file? (y/N)${NC}"
        read -p "> " recreate_config
        if [[ $recreate_config =~ ^[Yy]$ ]]; then
            cp git-config-message-generator-config.example.json "$CONFIG_FILE"
            echo -e "${GREEN}${CHECK} Configuration file recreated at $CONFIG_FILE${NC}"
        else
            echo -e "${GREEN}${CHECK} Keeping existing configuration file${NC}"
            echo "Current configuration file contents:"
            cat "$CONFIG_FILE"
            echo "Configuration file path: $CONFIG_FILE"
            return
        fi
    fi

    configure_ai_provider
}

# Function to configure AI provider
configure_ai_provider() {
    echo -e "${YELLOW}Let's set up your AI provider:${NC}"
    echo -e "1) OpenAI"
    echo -e "2) AWS Bedrock"
    read -p "Choose your provider (1/2): " provider_choice

    if [ "$provider_choice" = "1" ]; then
        configure_openai
    elif [ "$provider_choice" = "2" ]; then
        configure_aws_bedrock
    else
        echo -e "${YELLOW}Invalid choice. Exiting.${NC}"
        exit 1
    fi
}

# Function to configure OpenAI
configure_openai() {
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
            update_config "$CONFIG_FILE" "OpenAI" "api_key" "$openai_key"
            echo -e "${GREEN}${CHECK} OpenAI API key added to config file${NC}"
        elif [ "$key_storage_choice" = "2" ]; then
            shell_profile="$HOME/.$(basename $SHELL)rc"
            echo "export OPENAI_API_KEY='$openai_key'" >> "$shell_profile"
            echo -e "${GREEN}${CHECK} OpenAI API key added to $shell_profile${NC}"
            echo -e "${YELLOW}Please restart your terminal or run 'source $shell_profile' to apply changes${NC}"
        else
            echo -e "${YELLOW}Invalid choice. OpenAI API key will not be stored.${NC}"
        fi
    fi
    echo -e "${GREEN}${CHECK} OpenAI configuration updated${NC}"
}

# Function to configure AWS Bedrock
configure_aws_bedrock() {
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
    update_config "$CONFIG_FILE" "AWS" "profile_name" "$aws_profile"
    echo -e "${GREEN}${CHECK} AWS Bedrock configuration updated${NC}"
}

# Function to set up Git hook
setup_git_hook() {
    local git_dir="$1"
    if [ -z "$git_dir" ]; then
        if git rev-parse --git-dir > /dev/null 2>&1; then
            git_dir=$(git rev-parse --git-dir)
        else
            echo -e "${YELLOW}Not in a Git repository. Please provide a path to an existing Git repository.${NC}"
            return 1
        fi
    elif [ ! -d "$git_dir/.git" ]; then
        echo -e "${YELLOW}The provided path is not a valid Git repository.${NC}"
        return 1
    else
        git_dir="$git_dir/.git"
    fi

    echo -e "${YELLOW}Setting up Git hook...${NC}"
    cp src/prepare-commit-msg "$git_dir/hooks/"
    chmod +x "$git_dir/hooks/prepare-commit-msg"
    echo -e "${GREEN}${CHECK} Git hook installed successfully in $git_dir${NC}"
}

# Main installation process
main() {
    echo -e "${YELLOW}${ROCKET} Installing the DeLoOps Did Stuff hook! ${ROCKET}${NC}"

    check_and_install_dependencies
    setup_config_file

    if [ $# -eq 1 ]; then
        setup_git_hook "$1"
    else
        setup_git_hook
    fi

    echo -e "${GREEN}${SPARKLES} Installation complete! Go do stuff! ${SPARKLES}${NC}"
}

# Run the main installation process
main "$@"