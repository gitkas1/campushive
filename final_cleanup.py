#!/usr/bin/env python3
import re

# Read the file
with open(r'c:\Users\kunva\OneDrive\Documents\lootcart\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Write back without chat/contact lines
with open(r'c:\Users\kunva\OneDrive\Documents\lootcart\index.html', 'w', encoding='utf-8') as f:
    skip_until = None
    for i, line in enumerate(lines):
        # Skip chat modal section
        if '<!-- Chat Modal -->' in line:
            skip_until = None
            for j in range(i, len(lines)):
                if '<!-- Product Detail Modal -->' in lines[j]:
                    skip_until = j
                    break
            if skip_until:
                continue
        
        # Skip inbox section
        if '<!-- Inbox Section -->' in line:
            skip_until = None
            for j in range(i, len(lines)):
                if '</div>\n' in lines[j] and j > i + 30:  # Roughly where inbox section ends
                    skip_until = j + 1
                    break
            if skip_until:
                continue
        
        # Skip the navbar inbox link
        if 'nav-inbox' in line:
            continue
        
        # Skip contact label and input in product detail
        if '"📞 Contact"' in line or 'detail-contact' in line:
            continue
        
        # Skip product-contact input field in sell form
        if 'product-contact' in line and 'input' in line:
            continue
        
        # Skip showing contact info call
        if 'showContactInfo' in line:
            continue
        
        # Skip chat button calls from products
        if 'openChat' in line and '<button' in line:
            continue
        if 'openChatFromDetail' in line:
            continue
        
        # Skip contact button styling in product list
        if 'contact-btn' in line or 'chat-btn' in line:
            continue
        
        # Skip the entire renderHomeProducts inline contact/chat buttons
        if 'Contact Seller' in line or '💬 Chat' in line:
            continue
        
        f.write(line)

print("✓ Removed remaining chat/contact references")
