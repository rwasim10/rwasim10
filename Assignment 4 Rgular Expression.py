#!/usr/bin/env python
# coding: utf-8

# # Advance Regular Expression Assignment

# # Assignment 1: Extracting Phone Numbers
# 
# Raw Text:
# Extract all valid Pakistani phone numbers from a given text.
# 
# Example:
# Text: Please contact me at 0301-1234567 or 042-35678901 for further details.

# In[2]:


import re
text = """
Please contact me at 0301-1234567 or 042-35678901 for further details.
"""
pattern = r"\d{4}-\d{7}"
a = re.findall(pattern, text)
a


# # Assignment 2: Validating Email Addresses
# 
# Raw Text:
# Validate email addresses according to Pakistani domain extensions (.pk).
# 
# Example:
# Text: Contact us at info@example.com or support@domain.pk for assistance.

# In[3]:


import re
text = """
Contact us at info@example.com or support@domain.pk for assistance
"""
pattern = r"\b([\w\-\.]+@[\w]+\.pk)\b"

a = re.findall(pattern, text, re.MULTILINE)
a


# # Assignment 3: Extracting CNIC Numbers
# 
# Raw Text:
# Extract all Pakistani CNIC (Computerized National Identity Card) numbers from a given text.
# 
# Example:
# Text: My CNIC is 12345-6789012-3 and another one is 34567-8901234-5.

# In[4]:


text = """
My CNIC is 12345-6789012-3 and another one is 34567-8901234-5.
"""
pattern = r"\d{5}[-]\d{7}[-]\d"
a = re.findall(pattern, text)
a


# # Assignment 4: Identifying Urdu Words
# 
# Raw Text:
# Identify and extract Urdu words from a mixed English-Urdu text.
# 
# Example:
# Text: یہ sentence میں کچھ English words بھی ہیں۔

# In[5]:


text = """
 یہ sentence میں کچھ English words بھی ہیں۔
"""
pattern = r"\b([^\s\-a-zA-Z]+\b)"

a = re.findall(pattern, text, re.MULTILINE)
a


# # Assignment 5: Finding Dates
# 
# Raw Text:
# Find and extract dates in the format DD-MM-YYYY from a given text.
# 
# Example:
# Text: The event will take place on 15-08-2023 and 23-09-2023.

# In[6]:


text = """
The event will take place on 15-08-2023 and 23-09-2023.
"""
pattern = r"\d{2}[-]\d{2}[-]\d{4}"
a = re.findall(pattern, text)
a


# # Assignment 6: Extracting URLs
# 
# Raw Text: 
# Extract all URLs from a text that belong to Pakistani domains.
# 
# Example:
# Text: Visit http://www.example.pk or https://website.com.pk for more information.

# In[7]:


import re
text = """
Visit http://www.example.pk or https://website.com.pk for more information.
"""
pattern = r"\b([https://]+[\w]+\.[\w]+.pk)\b"
a = re.findall(pattern, text, re.MULTILINE)
a


# # Assignment 7: Analyzing Currency
# 
# Raw Text:
# Extract and analyze currency amounts in Pakistani Rupees (PKR) from a given text.
# 
# Example:
# Text: The product costs PKR 1500, while the deluxe version is priced at Rs. 2500.

# In[8]:


text = """
The product costs PKR 1500, while the deluxe version is priced at Rs. 2500.
"""
pattern = r"[0-9]+"
a = re.findall(pattern, text)
a


# # Assignment 8: Removing Punctuation
# 
# Raw Text:
# Remove all punctuation marks from a text while preserving Urdu characters.
# 
# Example:
# Text: کیا! آپ, یہاں؟

# In[9]:


import re
text = """
کیا! آپ, یہاں؟
"""
pattern = r"[^\W]+"
a = re.findall(pattern, text, re.MULTILINE)
a


# # Assignment 9: Extracting City Names
# 
# Raw Text:
# Extract names of Pakistani cities from a given text.
# 
# Example:
# Text: Lahore, Karachi, Islamabad, and Peshawar are major cities of Pakistan.

# In[10]:


text = """
Lahore, Karachi, Islamabad, and Peshawar are major cities of Pakistan.
"""
pattern = r"(?:([\w]+)\,\s([\w]+)\,\s([\w]+)\,\sand\s([\w]+))"

a = re.findall(pattern, text, re.MULTILINE)
a


# # Assignment 10: Analyzing Vehicle Numbers
# 
# Raw Text:
# Identify and extract Pakistani vehicle registration numbers (e.g., ABC-123) from a text.
# 
# Example:
# Text: I saw a car with the number plate LEA-567 near the market.

# In[11]:


text = """
I saw a car with the number plate LEA-567 near the market.
"""
pattern = r"\w{3}[-]\d{3}"
a = re.findall(pattern, text)
a


# In[ ]:




