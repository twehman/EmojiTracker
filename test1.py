from cs50 import SQL
import os
import xml.etree.ElementTree as ET

tree = ET.parse('sms-20191010095828 (1).xml')
root = tree.getroot()

db = SQL("sqlite:///test.db")

print(root.tag)