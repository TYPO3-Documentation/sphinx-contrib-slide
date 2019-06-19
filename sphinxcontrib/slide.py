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
    if re.match('https://docs.google.com/presentation/d/', url):
        return get_slide_options_for_googledocs(url, 'presentation', 'embed')
    elif re.match('https://docs.google.com/document/d/', url):
        return get_slide_options_for_googledocs(url, 'document', 'pub')
    elif re.match('https://docs.google.com/spreadsheets/d/', url):
        return get_slide_options_for_googledocs(url, 'spreadsheets', 'pubhtml')
    elif re.match('https?://www.slideshare.net/', url):
        return get_slide_options_for_slideshare(url)
    elif re.match('https://speakerdeck.com/', url):
        return get_slide_options_for_speakerdeck(url)
    elif re.match('https?://slides.com/', url):
        return get_slide_options_for_slides_com(url)
    else:
        msg = 'unknown slide URL: %s' % url
        raise Exception(msg)


def get_slide_options_for_googledocs(url, segment1, endseg):
    options = {}
    options['type'] = 'googledocs'
    embed_url = url.split('?', 1)[0].rstrip('/')
    if not embed_url.endswith('/' + endseg):
        embed_url += '/' + endseg
    options['embed_url'] = embed_url

    if segment1 == 'presentation':
        # 576x420, 480x375, 480x299
        template = """<iframe src="%s?start=false&loop=false&delayms=3000" frameborder="0" width="576" height="420" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>"""
        options['html'] = template % embed_url
    elif segment1 == 'spreadsheets':
        template = """<iframe src="%s?widget=true&amp;headers=false" width="576" height="420"></iframe>"""
        options['html'] = template % embed_url
    elif segment1 == 'document':
        template = """<iframe src="%s?embedded=true" width="576" height="420"></iframe>"""
        options['html'] = template % embed_url
    else:
        options['html'] = '<div><a href="%s">%s</a></div>' % (embed_url, embed_url)
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

