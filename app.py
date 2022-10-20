from flask import Flask, render_template
import json
import re
import generate_data

app = Flask(__name__)

JSON_FILE = 'data.json'

# from https://gist.github.com/guillaumepiot/4539986
def replace_url_to_link(value):
    # Replace url to link
    urls = re.compile(r"((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)", re.MULTILINE|re.UNICODE)
    value = urls.sub(r'<a href="\1" target="_blank">\1</a>', value)
    # Replace email to mailto
    urls = re.compile(r"([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)", re.MULTILINE|re.UNICODE)
    value = urls.sub(r'<a href="mailto:\1">\1</a>', value)
    return value

generate_data.execute()

with open(JSON_FILE) as json_file:
    data = json.load(json_file)

@app.route("/")
def main():
    return replace_url_to_link(render_template('index.html', data = data))