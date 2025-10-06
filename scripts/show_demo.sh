#!/bin/bash
#
# Complete Demo - Shows logs and analysis step by step
#

set -e

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

clear

echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                                                                      ║${NC}"
echo -e "${CYAN}║          🔍 AI-Powered Production Log Analyzer - DEMO                ║${NC}"
echo -e "${CYAN}║                                                                      ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}This demo shows how the AI analyzer processes real production logs.${NC}"
echo ""
echo -e "${GREEN}Press ENTER to continue...${NC}"
read

# =============================================================================
# DEMO 1: Database Connection Failure
# =============================================================================
clear
echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                                                                      ║${NC}"
echo -e "${CYAN}║           📋 SCENARIO 1: Database Connection Failure                 ║${NC}"
echo -e "${CYAN}║                                                                      ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}SITUATION:${NC} Your API is returning 500 errors. Users are complaining."
echo -e "${YELLOW}PROBLEM:${NC} Something went wrong, but you have 50GB of logs..."
echo ""
echo -e "${MAGENTA}Let's look at the logs:${NC}"
echo ""
cat sample_logs/error.log
echo ""
echo -e "${GREEN}Press ENTER to run AI analysis...${NC}"
read

echo ""
echo -e "${CYAN}🤖 Running AI Analysis...${NC}"
echo ""
python3 analyzer.py analyze sample_logs/error.log

echo ""
echo -e "${GREEN}✅ RESULT:${NC} Found root cause in 30 seconds!"
echo -e "${GREEN}   Instead of manually searching through logs for hours.${NC}"
echo ""
echo -e "${GREEN}Press ENTER for next demo...${NC}"
read

# =============================================================================
# DEMO 2: Performance Issues
# =============================================================================
clear
echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                                                                      ║${NC}"
echo -e "${CYAN}║              📋 SCENARIO 2: Performance/Slow API                     ║${NC}"
echo -e "${CYAN}║                                                                      ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}SITUATION:${NC} Users report that search is extremely slow."
echo -e "${YELLOW}PROBLEM:${NC} Some endpoints take 5+ seconds to respond."
echo ""
echo -e "${MAGENTA}Performance logs:${NC}"
echo ""
cat sample_logs/performance.log
echo ""
echo -e "${GREEN}Press ENTER to run AI analysis...${NC}"
read

echo ""
echo -e "${CYAN}🤖 Running AI Analysis...${NC}"
echo ""
python3 analyzer.py analyze sample_logs/performance.log

echo ""
echo -e "${GREEN}✅ RESULT:${NC} AI identified timeout issues and slow queries!"
echo -e "${GREEN}   Suggests specific optimizations.${NC}"
echo ""
echo -e "${GREEN}Press ENTER for final demo...${NC}"
read

# =============================================================================
# DEMO 3: Quick Demo Mode
# =============================================================================
clear
echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                                                                      ║${NC}"
echo -e "${CYAN}║                 📋 SCENARIO 3: Quick Demo Mode                       ║${NC}"
echo -e "${CYAN}║                                                                      ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}One command to try it:${NC}"
echo ""
echo -e "${CYAN}  python3 analyzer.py demo${NC}"
echo ""
echo -e "${GREEN}Running demo mode...${NC}"
echo ""
python3 analyzer.py demo

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                                      ║${NC}"
echo -e "${GREEN}║                       ✨ DEMO COMPLETE! ✨                            ║${NC}"
echo -e "${GREEN}║                                                                      ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}What you just saw:${NC}"
echo -e "  ✅ AI analyzed production logs"
echo -e "  ✅ Found root causes automatically"
echo -e "  ✅ Suggested specific fixes"
echo -e "  ✅ Generated timeline of events"
echo -e "  ✅ All in under 30 seconds!"
echo ""
echo -e "${YELLOW}Try it yourself:${NC}"
echo -e "  • ${CYAN}python3 analyzer.py demo${NC} - Quick demo"
echo -e "  • ${CYAN}python3 analyzer.py analyze your-log.log${NC} - Analyze any log file"
echo -e "  • ${CYAN}make demo${NC} - Run via Makefile"
echo ""
echo -e "${GREEN}GitHub:${NC} https://github.com/KlementMultiverse/api-documentation-generator"
echo ""
echo -e "${MAGENTA}⭐ Star the repo if you find this useful!${NC}"
echo ""
