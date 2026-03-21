#!/usr/bin/env python3
import re

# Read the file
with open(r'c:\Users\kunva\OneDrive\Documents\lootcart\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove CSS classes related to chat and contact
css_removals = [
    # Contact button CSS
    (r"\s+\.contact-btn \{[^\}]+\}", ""),
    (r"\s+\.contact-btn:hover \{[^\}]+\}", ""),
    
    # Chat button CSS  
    (r"\s+\.chat-btn \{[^\}]+\}", ""),
    (r"\s+\.chat-btn:hover \{[^\}]+\}", ""),
    
    # Chat modal CSS
    (r"/\* Chat Modal \*/.+?(?=/\*|@)", ""),
    (r"\s+\.chat-modal \{[^\}]+\}", ""),
    (r"\s+\.chat-modal\.active \{[^\}]+\}", ""),
    (r"\s+\.chat-modal-content \{[^\}]+\}", ""),
    (r"\s+\.chat-header \{[^\}]+\}", ""),
    (r"\s+\.chat-header h3 \{[^\}]+\}", ""),
    (r"\s+\.chat-close \{[^\}]+\}", ""),
    (r"\s+\.chat-header-btn \{[^\}]+\}", ""),
    (r"\s+\.chat-header-btn:hover \{[^\}]+\}", ""),
    (r"\s+\.chat-messages \{[^\}]+\}", ""),
    (r"\s+\.message \{[^\}]+\}", ""),
    (r"\s+\.message\.sent \{[^\}]+\}", ""),
    (r"\s+\.message\.received \{[^\}]+\}", ""),
    (r"\s+\.message-bubble \{[^\}]+\}", ""),
    (r"\s+\.message\.sent \.message-bubble \{[^\}]+\}", ""),
    (r"\s+\.message\.received \.message-bubble \{[^\}]+\}", ""),
    (r"\s+\.chat-input-area \{[^\}]+\}", ""),
    (r"\s+\.chat-input-area input \{[^\}]+\}", ""),
    (r"\s+\.chat-input-area button \{[^\}]+\}", ""),
    (r"\s+\.chat-input-area button:hover \{[^\}]+\}", ""),
    
    # Contact verification and meeting related (keep minimal - they're part of meeting arrangement)
    # But remove if they only relate to contact features
]

for pattern, replacement in css_removals:
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Remove HTML elements
html_removals = [
    # Chat modal HTML
    (r"<!-- Chat Modal -->.*?<\/div>\s*<!-- Product Detail Modal -->", "<!-- Product Detail Modal -->", re.DOTALL),
    
    # Inbox section HTML  
    (r"<!-- Inbox Section -->.*?<\/div>\s*<\/div>\s*<!-- Chat Modal -->", "", re.DOTALL),
    
    # Chat button from nav-inbox
    (r'<a id="nav-inbox"[^>]*>.*?<\/a>', "", re.DOTALL),
]

for item in html_removals:
    if len(item) == 3:
        pattern, replacement, flags = item
        content = re.sub(pattern, replacement, content, flags=flags)
    else:
        pattern, replacement = item
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Remove contact/chat button from product rendering
# This handles: <button class="contact-btn"...> and <button class="chat-btn"...>
button_pattern = r'<button class="(contact|chat)-btn"[^>]*>.*?<\/button>\s*'
content = re.sub(button_pattern, "", content, flags=re.DOTALL)

# Remove contact button from detail modal
content = re.sub(r'<dt>📞 Contact<\/dt>.*?<\/dd>', "", content, flags=re.DOTALL)
content = re.sub(r'<button id="detail-chat-btn"[^>]*>.*?<\/button>\s*', "", content, flags=re.DOTALL)

# Write the file back
with open(r'c:\Users\kunva\OneDrive\Documents\lootcart\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Removed chat/contact HTML and CSS successfully")
