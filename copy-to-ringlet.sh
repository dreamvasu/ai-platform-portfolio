#!/bin/bash

# Script to copy deployment files to Ringlet repository
# Usage: ./copy-to-ringlet.sh /path/to/ringlet

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if path provided
if [ -z "$1" ]; then
  echo -e "${RED}❌ Error: Please provide Ringlet repository path${NC}"
  echo ""
  echo "Usage: ./copy-to-ringlet.sh /path/to/ringlet"
  echo ""
  echo "Example:"
  echo "  ./copy-to-ringlet.sh ~/Downloads/ringlet"
  echo "  ./copy-to-ringlet.sh ~/Projects/ringlet"
  exit 1
fi

RINGLET_PATH="$1"

# Check if path exists
if [ ! -d "$RINGLET_PATH" ]; then
  echo -e "${RED}❌ Error: Directory not found: $RINGLET_PATH${NC}"
  exit 1
fi

# Check if it looks like a Django project
if [ ! -f "$RINGLET_PATH/manage.py" ]; then
  echo -e "${YELLOW}⚠️  Warning: No manage.py found in $RINGLET_PATH${NC}"
  echo "This might not be a Django project. Continue anyway? (y/n)"
  read -r response
  if [ "$response" != "y" ]; then
    echo "Aborted."
    exit 0
  fi
fi

echo -e "${GREEN}📦 Copying deployment files to Ringlet...${NC}"
echo "Target: $RINGLET_PATH"
echo ""

# Create directories
echo "Creating directories..."
mkdir -p "$RINGLET_PATH/terraform"
mkdir -p "$RINGLET_PATH/kubernetes"

# Copy Terraform
echo -e "${YELLOW}→${NC} Copying Terraform infrastructure..."
cp -r terraform/ "$RINGLET_PATH/"
echo -e "${GREEN}✅${NC} Terraform copied (16 files)"

# Copy Kubernetes
echo -e "${YELLOW}→${NC} Copying Kubernetes manifests..."
cp -r kubernetes/ringlet/ "$RINGLET_PATH/kubernetes/"
echo -e "${GREEN}✅${NC} Kubernetes manifests copied (8 files)"

# Copy Docker files to root
echo -e "${YELLOW}→${NC} Copying Docker files..."
cp kubernetes/ringlet/Dockerfile "$RINGLET_PATH/"
cp kubernetes/ringlet/.dockerignore "$RINGLET_PATH/"

# Backup existing requirements.txt if it exists
if [ -f "$RINGLET_PATH/requirements.txt" ]; then
  echo -e "${YELLOW}⚠️${NC}  Backing up existing requirements.txt to requirements.original.txt"
  cp "$RINGLET_PATH/requirements.txt" "$RINGLET_PATH/requirements.original.txt"
  echo -e "${YELLOW}⚠️${NC}  You'll need to merge requirements manually!"
else
  cp kubernetes/ringlet/requirements.txt "$RINGLET_PATH/"
fi

echo -e "${GREEN}✅${NC} Docker files copied"

# Copy documentation
echo -e "${YELLOW}→${NC} Copying documentation..."
cp RINGLET_DEPLOYMENT_GUIDE.md "$RINGLET_PATH/"
cp RINGLET_AKS_COMPLETION_STATUS.md "$RINGLET_PATH/"
cp RINGLET_SETUP_GUIDE.md "$RINGLET_PATH/"
cp RINGLET_CLAUDE.md "$RINGLET_PATH/CLAUDE.md"
echo -e "${GREEN}✅${NC} Documentation copied (4 files)"

# Copy READMEs
echo -e "${YELLOW}→${NC} Copying module READMEs..."
cp terraform/README.md "$RINGLET_PATH/terraform/" 2>/dev/null || true
cp kubernetes/ringlet/README.md "$RINGLET_PATH/kubernetes/" 2>/dev/null || true
echo -e "${GREEN}✅${NC} READMEs copied"

echo ""
echo -e "${GREEN}🎉 All deployment files copied successfully!${NC}"
echo ""
echo -e "${YELLOW}📋 Files copied to: $RINGLET_PATH${NC}"
echo ""
echo "Structure created:"
echo "  $RINGLET_PATH/"
echo "  ├── Dockerfile"
echo "  ├── .dockerignore"
echo "  ├── CLAUDE.md"
echo "  ├── RINGLET_DEPLOYMENT_GUIDE.md"
echo "  ├── RINGLET_AKS_COMPLETION_STATUS.md"
echo "  ├── RINGLET_SETUP_GUIDE.md"
echo "  ├── terraform/ (16 files)"
echo "  └── kubernetes/ (8 manifests)"
echo ""
echo -e "${YELLOW}⚠️  IMPORTANT NEXT STEPS:${NC}"
echo ""
echo "1. Review and merge requirements.txt:"
if [ -f "$RINGLET_PATH/requirements.original.txt" ]; then
  echo "   - Original saved to: requirements.original.txt"
  echo "   - New deps in: kubernetes/ringlet/requirements.txt"
  echo "   - Merge them into: requirements.txt"
else
  echo "   - Review: requirements.txt (copied from template)"
fi
echo ""
echo "2. Update Dockerfile WSGI path:"
echo "   - Open: Dockerfile"
echo "   - Check: CMD line matches your WSGI location"
echo "   - Example: config.wsgi:application or ringlet.wsgi:application"
echo ""
echo "3. Review ConfigMap:"
echo "   - Open: kubernetes/base/configmap.yaml"
echo "   - Update: DJANGO_SETTINGS_MODULE if needed"
echo "   - Add: Any Ringlet-specific environment variables"
echo ""
echo "4. Read deployment guide:"
echo "   cd $RINGLET_PATH"
echo "   cat RINGLET_DEPLOYMENT_GUIDE.md"
echo ""
echo "5. Start deployment:"
echo "   cd $RINGLET_PATH/terraform/environments/prod"
echo "   cp terraform.tfvars.example terraform.tfvars"
echo "   # Edit terraform.tfvars with your values"
echo "   terraform init"
echo ""
echo -e "${GREEN}Ready to deploy! 🚀${NC}"
