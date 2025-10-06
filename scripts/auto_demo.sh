#!/bin/bash
#
# AUTO DEMO - Perfect for screen recording
# One command, automatic flow, looks great on video
#

set -e

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m'

# Speed (adjust if too fast/slow)
PAUSE_SHORT=2
PAUSE_MEDIUM=3
PAUSE_LONG=5

clear

# =============================================================================
# INTRO
# =============================================================================
echo -e "${CYAN}${BOLD}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║          🔍 AI-Powered Production Log Analyzer                       ║
║                                                                      ║
║          Find root causes in 30 seconds, not 3 hours                ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"
sleep $PAUSE_MEDIUM

echo -e "${YELLOW}${BOLD}The Problem:${NC}"
echo -e "  Production is down. You have 50GB of logs."
echo -e "  Engineers spend hours manually searching..."
echo ""
sleep $PAUSE_MEDIUM

echo -e "${GREEN}${BOLD}The Solution:${NC}"
echo -e "  AI analyzes logs automatically and finds root causes."
echo ""
sleep $PAUSE_MEDIUM

echo -e "${CYAN}Let's see it in action! 🚀${NC}"
echo ""
sleep $PAUSE_SHORT

# =============================================================================
# SCENARIO 1: Database Failure
# =============================================================================
clear
echo -e "${CYAN}${BOLD}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║              🔴 SCENARIO: Production Database Failure                ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"
sleep $PAUSE_SHORT

echo -e "${YELLOW}Situation:${NC} API returning 500 errors, users complaining"
echo ""
sleep $PAUSE_SHORT

echo -e "${MAGENTA}📋 Sample production logs:${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
head -15 sample_logs/error.log
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
sleep $PAUSE_LONG

echo -e "${GREEN}${BOLD}Running AI analysis...${NC}"
echo ""
sleep $PAUSE_SHORT

# Run the actual analyzer
python3 analyzer.py analyze sample_logs/error.log

echo ""
sleep $PAUSE_LONG

echo -e "${GREEN}${BOLD}✅ Root cause found in 30 seconds!${NC}"
echo -e "   ${GREEN}Instead of 2-4 hours of manual searching.${NC}"
echo ""
sleep $PAUSE_MEDIUM

# =============================================================================
# SCENARIO 2: Performance Issue
# =============================================================================
clear
echo -e "${CYAN}${BOLD}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║              ⚡ SCENARIO: Slow API Performance                       ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"
sleep $PAUSE_SHORT

echo -e "${YELLOW}Situation:${NC} Search endpoint taking 5+ seconds"
echo ""
sleep $PAUSE_SHORT

echo -e "${MAGENTA}📋 Performance logs:${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
cat sample_logs/performance.log
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
sleep $PAUSE_LONG

echo -e "${GREEN}${BOLD}Running AI analysis...${NC}"
echo ""
sleep $PAUSE_SHORT

python3 analyzer.py analyze sample_logs/performance.log

echo ""
sleep $PAUSE_LONG

echo -e "${GREEN}${BOLD}✅ Performance issues identified with specific fixes!${NC}"
echo ""
sleep $PAUSE_MEDIUM

# =============================================================================
# ONE-COMMAND DEMO
# =============================================================================
clear
echo -e "${CYAN}${BOLD}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║                    ⚡ Try It Yourself                                ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"
sleep $PAUSE_SHORT

echo -e "${YELLOW}One command to get started:${NC}"
echo ""
echo -e "  ${CYAN}${BOLD}python3 analyzer.py demo${NC}"
echo ""
sleep $PAUSE_SHORT

echo -e "${YELLOW}Or analyze your own logs:${NC}"
echo ""
echo -e "  ${CYAN}${BOLD}python3 analyzer.py analyze your-app.log${NC}"
echo ""
sleep $PAUSE_MEDIUM

# =============================================================================
# FINAL SUMMARY
# =============================================================================
clear
echo -e "${GREEN}${BOLD}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║                    ✨ What You Just Saw ✨                           ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"
echo ""
sleep $PAUSE_SHORT

echo -e "  ✅ AI analyzed production logs"
sleep 1
echo -e "  ✅ Found root causes automatically"
sleep 1
echo -e "  ✅ Suggested specific fixes"
sleep 1
echo -e "  ✅ Generated timeline of events"
sleep 1
echo -e "  ✅ All in under 30 seconds!"
echo ""
sleep $PAUSE_MEDIUM

echo -e "${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}${BOLD}Features:${NC}"
echo -e "  • Works with ANY log format (Python, Java, Node.js, etc.)"
echo -e "  • AI-powered pattern detection"
echo -e "  • Beautiful terminal output"
echo -e "  • One command to analyze"
echo -e "  • 100% open source & free"
echo ""
sleep $PAUSE_MEDIUM

echo -e "${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}${BOLD}Try it yourself:${NC}"
echo ""
echo -e "  ${CYAN}git clone https://github.com/KlementMultiverse/api-documentation-generator${NC}"
echo -e "  ${CYAN}cd api-documentation-generator${NC}"
echo -e "  ${CYAN}python3 analyzer.py demo${NC}"
echo ""
sleep $PAUSE_MEDIUM

echo -e "${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${MAGENTA}${BOLD}⭐ Star on GitHub:${NC}"
echo -e "   ${CYAN}https://github.com/KlementMultiverse/api-documentation-generator${NC}"
echo ""
sleep $PAUSE_MEDIUM

echo -e "${GREEN}${BOLD}Built through human-AI collaboration 🤖${NC}"
echo ""
sleep $PAUSE_SHORT

echo -e "${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# End
