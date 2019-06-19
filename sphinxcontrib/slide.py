# -*- coding: utf-8 -*-
"""
    sphinxcontrib.slide
    ~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2012 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

import re
import requests
import urllib2
from docutils import nodes
try:
    from sphinx.util.compat import Directive
except ImportError:
    from docutils.parsers.rst import Directive


class slide(nodes.General, nodes.Element):
    pass


class SlideDirective(Directive):
    """Directive for embedding slide"""

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
    }

    def run(self):
        try:
            node = slide()
            node['url'] = self.arguments[0]
            node['slide_options'] = get_slide_options(self.arguments[0])

            return [node]
        except Exception, e:
            reporter = self.state.document.reporter
            return [reporter.warning(str(e), line=self.lineno)]


def get_slide_options(url):
    if re.match('https://docs.google.com/presentation/(pub\?|d/)', url):
        return get_slide_options_for_googledocs(url)
    elif re.match('https?://www.slideshare.net/', url):
        return get_slide_options_for_slideshare(url)
    elif re.match('https://speakerdeck.com/', url):
        return get_slide_options_for_speakerdeck(url)
    elif re.match('https?://slides.com/', url):
        return get_slide_options_for_slides_com(url)
    else:
        msg = 'unknown slide URL: %s' % url
        raise Exception(msg)


def get_slide_options_for_googledocs(url):
    template = """<iframe src="%s/embed?start=false&loop=false&delayms=3000" frameborder="0" width="480" height="299" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>"""
    template_old = """<iframe src="%s" frameborder="0" width="480" height="375" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"> </iframe>"""
    options = {}
    embed_url = url.rstrip('/')
    if embed_url.endswith('embed'):
        embed_url = embed_url[:-len('embed')]
    embed_url = embed_url.rstrip('/')
    if embed_url:
        options['type'] = 'googledocs'
        options['html'] = template % embed_url
    else:
        options['type'] = 'googledocs failed'
        options['html'] = ''
    return options


def get_slide_options_for_slideshare(url):
    options = {'type': 'slideshare failed'}
    payload = {'url': url, 'format': 'json'}
    r = requests.get('https://www.slideshare.net/api/oembed/2', params=payload)
    if r.status_code == 200:
        options = r.json()
        options['type'] = 'slideshare'
    return options


def get_slide_options_for_speakerdeck(url):
    options = {}
    options['type'] = 'speakerdeck'

    content = urllib2.urlopen(url).read()
    matched = re.search('<h1>(.*?)</h1>', content)
    if matched:
        options['title'] = matched.group(1).decode('utf-8')

    matched = re.search('data-id="(.*?)"', content)
    if matched:
        options['data_id'] = matched.group(1).decode('utf-8')

    matched = re.search('data-ratio="(.*?)"', content)
    if matched:
        options['data_ratio'] = matched.group(1).decode('utf-8')

    return options


def get_slide_options_for_slides_com(url):
    options = {}
    options['type'] = 'slides.com'
    options['embed_url'] = re.sub('https?:', '', re.sub('#/$', '', url)) + '/embed'

    content = urllib2.urlopen(url).read()
    matched = re.search('<h4>(.*?)</h4>', content)
    if matched:
        options['title'] = matched.group(1).decode('utf-8')

    return options


def html_visit_slide_node(self, node):
    options = node['slide_options']

    if options['type'] == 'googledocs':
        self.body.append(options['html'])
    elif options['type'] == 'slideshare':
        self.body.append(options.get('html', ''))
    elif options['type'] == 'speakerdeck':
        template = """<script async="async" class="speakerdeck-embed" data-id="%s" data-ratio="%s" src="//speakerdeck.com/assets/embed.js"> </script>"""
        self.body.append(template % (options.get('data_id'), options.get('data_ratio')))
    elif options['type'] == 'slides.com':
        template = ('<iframe src="%s" width="576" height="420" scrolling="no"'
                    ' frameborder="0" webkitallowfullscreen mozallowfullscreen'
                    ' allowfullscreen></iframe>')
        self.body.append(template % options.get('embed_url'))


def latex_visit_slide_node(self, node):
    title = node['slide_options'].get('title')

    if title:
        self.body.append("\\href{%s}{%s}" % (self.encode_uri(node['url']), self.encode(title)))
    else:
        self.body.append("\\url{%s}" % self.encode_uri(node['url']))


def depart_slide_node(self, node):
    pass


def setup(app):
    app.add_node(slide,
                 html=(html_visit_slide_node, depart_slide_node),
                 latex=(latex_visit_slide_node, depart_slide_node))
    app.add_directive('slide', SlideDirective)


if 0 and __name__ == "__main__" and "probing slideshare":
    response_example = {
        "author_name": "TRITUM",
        "author_url": "https://www.slideshare.net/TRITUM",
        "conversion_version": 2,
        "height": 355,
        "html": "<iframe src=\"https://www.slideshare.net/slideshow/embed_code/key/28iL36exB50UkP\" width=\"427\" height=\"356\" frameborder=\"0\" marginwidth=\"0\" marginheight=\"0\" scrolling=\"no\" style=\"border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;\" allowfullscreen> </iframe> <div style=\"margin-bottom:5px\"> <strong> <a href=\"https://www.slideshare.net/TRITUM/whats-new-in-typo3-v9-lts\" title=\"What&#x27;s new in TYPO3 v9 LTS\" target=\"_blank\">What&#x27;s new in TYPO3 v9 LTS</a> </strong> from <strong><a href=\"https://www.slideshare.net/TRITUM\" target=\"_blank\">TRITUM</a></strong> </div>\n\n",
        "provider_name": "SlideShare",
        "provider_url": "https://www.slideshare.net/",
        "slide_image_baseurl": "//image.slidesharecdn.com/typo3v9lts-181007112714/95/slide-",
        "slide_image_baseurl_suffix": "-1024.jpg",
        "slideshow_id": 118556992,
        "thumbnail": "//cdn.slidesharecdn.com/ss_thumbnails/typo3v9lts-181007112714-thumbnail.jpg?cb=1538911762",
        "thumbnail_height": 128,
        "thumbnail_url": "https://cdn.slidesharecdn.com/ss_thumbnails/typo3v9lts-181007112714-thumbnail.jpg?cb=1538911762",
        "thumbnail_width": 170,
        "title": "What's new in TYPO3 v9 LTS",
        "total_slides": 52,
        "type": "rich",
        "version": "1.0",
        "version_no": "1538911762",
        "width": 425
    }
    url = 'http://www.slideshare.net/TRITUM/whats-new-in-typo3-v9-lts'
    get_slide_options_for_slideshare(url)

if 0 and __name__ == "__main__" and "probing google":
    embed_code = """<iframe src="https://docs.google.com/presentation/d/e/2PACX-1vQEjSEE6PtyibpB8ZhDHAEhUwkXqHfbTdCHHehJYrElzTTVy2MS7dh-Pvyz1qwVypKfOXI3TE0QUxk4/embed?start=false&loop=false&delayms=3000" frameborder="0" width="480" height="299" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>"""
    response_example = {
    }
    url = ('https://docs.google.com/presentation/d/1FOVjpJIJrHC4Wly9rsGelDdfXe4bgamLOJh1GlVx2Tk/present')
    get_slide_options_for_googledocs(url)

