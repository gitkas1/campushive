#!/usr/bin/env python3
import re

# Read the file
with open(r'c:\Users\kunva\OneDrive\Documents\lootcart\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove chat and inbox related variables and functions
removals = [
    # Variables at top of script section
    (r"    let chats = JSON\.parse\(localStorage\.getItem\('chats'\)\) \|\| \{\};[^\n]*\n", ""),
    (r"    let currentChat = null;[^\n]*\n", ""),
    (r"    let currentInboxConversation = null;[^\n]*\n", ""),
    (r"    let inboxConversations = \{\};[^\n]*\n", ""),
    
    # Functions - use broader patterns
    (r"\s+function openChat\(event, productId\)\s*\{[\s\S]*?(?=\s+function|\s+\/\/|$)", ""),
    (r"\s+function closeChatModal\(\)\s*\{[\s\S]*?(?=\s+function|\s+\/\/|$)", ""),
    (r"\s+function renderChatMessages\(\)\s*\{[\s\S]*?(?=\s+function|\s+\/\/|$)", ""),
    (r"\s+function sendChatMessage\(\)\s*\{[\s\S]*?(?=\s+function|\s+\/\/|$)", ""),
    (r"\s+function handleChatKeyPress\(event\)\s*\{[\s\S]*?(?=\s+function|\s+\/\/|$)", ""),
    (r"\s+function openConversationInInbox\(\)\s*\{[\s\S]*?(?=\s+function|\s+\/\/|$)", ""),
    (r"\s+function loadAllConversations\(\)\s*\{[\s\S]*?(?=\s+function|\s+\/\/|$)", ""),
    (r"\s+function renderConversationsList\(\)\s*\{[\s\S]*?(?=\s+function|\s+\/\/|$)", ""),
    (r"\s+function selectInboxConversation\(conversationId\)\s*\{[\s\S]*?(?=\s+function|\s+\/\/|$)", ""),
    (r"\s+function renderInboxChatMessages\(\)\s*\{[\s\S]*?(?=\s+function|\s+\/\/|$)", ""),
    (r"\s+function sendInboxMessage\(\)\s*\{[\s\S]*?(?=\s+function|\s+\/\/|$)", ""),
    (r"\s+function handleInboxKeyPress\(event\)\s*\{[\s\S]*?(?=\s+function|\s+\/\/|$)", ""),
    (r"\s+function startInboxListener\(\)\s*\{[\s\S]*?(?=\s+function|\s+\/\/|$)", ""),
    (r"\s+function debugInbox\(\)\s*\{[\s\S]*?(?=\s+function|\s+\/\/|$)", ""),
    (r"\s+\/\/ ==================== INBOX FUNCTIONS WITH FIREBASE ====================[\s\S]*?(?=\s+\/\/ ====================)", ""),
    (r"\s+\/\/ ==================== DEBUG FUNCTIONS ====================[\s\S]*?(?=\s+\/\/ Product Detail)", ""),
]

for pattern, replacement in removals:
    content = re.sub(pattern, replacement, content)

# Write the file back
with open(r'c:\Users\kunva\OneDrive\Documents\lootcart\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Removed chat functions successfully")
