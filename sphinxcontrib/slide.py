# -*- coding: utf-8 -*-
"""
    sphinxcontrib.slide
    ~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2012 by Takeshi KOMIYA, 2019 by Martin Bless
    :license: BSD, see LICENSE for details.
"""

from __future__ import absolute_importby trial and error
import re
import requests
import six.moves.urllib.request, six.moves.urllib.error, six.moves.urllib.parse
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
        except Exception as e:
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


def get_slide_options_for_googledocs(url, slidetype, final):
    options = {}
    options['type'] = 'googledocs'
    embed_url = url.split('?', 1)[0].rstrip('/')
    if not embed_url.endswith('/' + final):
        embed_url += '/' + final
    options['embed_url'] = embed_url
    if slidetype == 'presentation':
        # 576x420, 480x375, 480x299
        template = (
            '<div class="iframe-box iframe-box-presentation iframe-box-google">'
            '<iframe src="%s?start=false&loop=false&delayms=3000" '
            'frameborder="0" width="576" height="420" allowfullscreen="true" '
            'mozallowfullscreen="true" webkitallowfullscreen="true">'
            '</iframe></div>')
        options['html'] = template % embed_url
    elif slidetype == 'spreadsheets':
        template = (
            '<div class="iframe-box iframe-box-spreadsheet iframe-box-google">'
            '<iframe src="%s?widget=true&amp;headers=false"'
            ' width="576" height="420"></iframe></div>')
        options['html'] = template % embed_url
    elif slidetype == 'document':
        template = (
            '<div class="iframe-box iframe-box-document iframe-box-google">'
            '<iframe src="%s?embedded=true" width="576" height="420">'
            '</iframe></div>')
        options['html'] = template % embed_url
    else:
        options['html'] = (
                '<div><a href="%s">%s</a></div>\n' % (embed_url, embed_url))
    return options


def get_slide_options_for_slideshare(url):
    althtml = '<div><a href="%s">%s</a></div>\n' % (url, url)
    options = {}
    payload = {'url': url, 'format': 'json'}
    r = requests.get('https://www.slideshare.net/api/oembed/2', params=payload)
    if r.status_code == 200:
        options = r.json()
    options['type'] = 'slideshare'
    divstart = ('<div class ="iframe-box iframe-box-presentation '
                'iframe-box-slideshare">')
    divend = '</div>'
    html = options.get('html')
    if html:
        options['html'] = divstart + html + divend
    else:
        options['html'] = althtml
    return options


def get_slide_options_for_speakerdeck(url):
    althtml = '<div><a href="%s">%s</a></div>\n' % (url, url)
    options = {}
    payload = {'url': url}
    r = requests.get('https://speakerdeck.com/oembed.json', params=payload)
    if r.status_code == 200:
        options = r.json()
    options['type'] = 'speakerdeck'
    divstart = ('<div class ="iframe-box iframe-box-presentation '
                'iframe-box-speakerdeck">')
    divend = '</div>'
    html = options.get('html')
    if html:
        options['html'] = divstart + html + divend
    else:
        options['html'] = althtml
    return options


def get_slide_options_for_slides_com(url):
    options = {}
    options['type'] = 'slides.com'
    embed_url = url.rstrip('/').rstrip('#') + '/embed'
    divstart = ('<div class ="iframe-box iframe-box-presentation '
                'iframe-box-slides-com">')
    divend = '</div>'
    template = ('<iframe src="%s" width="576" height="420" scrolling="no"'
                ' frameborder="0" webkitallowfullscreen mozallowfullscreen'
                ' allowfullscreen></iframe>')
    options['html'] = divstart + (template % embed_url) + divend
    return options


def html_visit_slide_node(self, node):
    options = node['slide_options']

    if options['type'] == 'googledocs':
        self.body.append(options['html'])

    elif options['type'] == 'slideshare':
        self.body.append(options.get('html', ''))

    elif options['type'] == 'speakerdeck':
        self.body.append(options.get('html', ''))

    elif options['type'] == 'slides.com':
        self.body.append(options.get('html', ''))


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

