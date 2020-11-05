# Common Gateway Inteface to exchange information & data between the script and server
import cgi

import sys

""" The os.path module is always the path module suitable for the operating system Python is running on, and therefore usable for local paths"""

import os.path

"""The logging module is intended to be thread-safe without any special work needing to be done by its clients."""

import logging

""" module to decode mp3 data from web server"""

import base64

# important for apache web server:
project_path = os.environ["smart_alarm_path"]
if project_path not in sys.path:
    sys.path.append(project_path)
#os.chdir(project_path)

from modules.xml_data import Xml_data


logger = logging.getLogger(__name__)


xml_data = Xml_data(str(project_path) + '/data.xml')

# web-dev interface
MIME_TABLE = {'.txt': 'text/plain',
              '.html': 'text/html',
              '.css': 'text/css',
              '.xml': 'text/xml',
              '.js': 'application/javascript',
              '.png': 'image/png'}

"""Application function sin to take in two inputs,
   the environment array to contain the web environment application inputs
   the start response allocates when to react
   The application will return an array depending on the inputs"""
def application(environ, start_response):
    logger.warning("python_server application started")
    # response for POST
    if environ['REQUEST_METHOD'] == 'POST':
        post = cgi.FieldStorage(
           fp=environ['wsgi.input'],
           environ=environ,
           keep_blank_values=False
        )

        uploaded_mp3_file = {}
        for s in post:
            if 'uploadMp3File' in s:
                fieldName = s[s.find('[')+1:s.find(']')]
                uploaded_mp3_file[fieldName] = post.getvalue(s)
            elif s == 'deleteMp3File':
                os.remove('./music/' + post.getvalue(s))
                xml_data.readFileNamesInMusicDirectory()
            else:
                try:
                    xml_data.changeValue(s, post.getvalue(s))
                    logger.warning("{} changed to {}".format(s, post.getvalue(s)))
                except Exception as e:
                    logger.warning("Error: Couldn't change xml entry {} to {} with error: {}".format(s, post.getvalue(s), e))

        if uploaded_mp3_file:
            mp3_data_base64 = uploaded_mp3_file['fileData'][uploaded_mp3_file['fileData'].find('base64,')+7:]
            # mp3_data = decode_base64(mp3_data_base64)
            f = open('./music/' + uploaded_mp3_file['name'], 'w')
            f.write(base64.b64decode(mp3_data_base64))
            f.close()
            xml_data.readFileNamesInMusicDirectory()

    path = environ['PATH_INFO']
    if path != '/data.xml':
        path = './web' + path
    else:
        path = '.' + path

    if os.path.exists(path):
        if path == './web/':
            path = './web/index.html'
        h = open(path, 'rb')
        content = h.read()
        h.close()

        headers = [('content-type', content_type(path))]
        start_response('200 OK', headers)
        return [content]
    else:
        return show_404_app(environ, start_response, path)


def content_type(path):
    """Return a guess at the mime type for this path
    based on the file extension"""

    name, ext = os.path.splitext(path)

    if ext in MIME_TABLE:
        return MIME_TABLE[ext]
    else:
        return "application/octet-stream"


def show_404_app(environ, start_response, path):
    start_response('404 Not Found', [('content-type','text/html')])
    return ["""<html><h1>""" + path + """ not Found</h1><p>
               That page is unknown. Return to
               the <a href="/">alarm clock</a>.</p>
               </html>""", ]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    import webbrowser

    httpd = make_server('', 8090, application)
    logger.debug('Serving on port 8090...')

    url = "http://127.0.0.1:8090"
    webbrowser.open(url)

    try:
        while True:
            # continue checking the hardware
            logger.debug('Server request.')
            httpd.handle_request()
    except KeyboardInterrupt:
        # Close the server by typing Strg + C
        httpd.server_close()
        logger.warning('Server Closed.')
    except:
        # Serve3r not working
        httpd.server_close()
        logger.error('Error')
