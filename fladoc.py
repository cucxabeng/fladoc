from flask import Flask, render_template, redirect, abort
from documentation import Documentation
from lxml import html

DEFAULT_VERSION = '0.12'

app = Flask(__name__, static_url_path='')


@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/docs/')
def show_root_page():
    return redirect('/docs/' + DEFAULT_VERSION)


@app.route('/docs/<version>/')
@app.route('/docs/<version>/<page>')
def show(version, page=None):
    if not is_version(version):
        return redirect('/docs/' + DEFAULT_VERSION + '/' + version)

    if page is None:
        page = ''

    section_page = page if page else 'installation'

    content = Documentation.get(version, section_page)

    if content is None:
        abort(404)

    title = html.fromstring(content).xpath('//h1')[0].text

    section = ''

    if Documentation.section_exist(version, page):
        section += '/' + page
    elif page:
        return redirect('/docs' + version)

    canonical = ''

    if Documentation.section_exist(DEFAULT_VERSION, section_page):
        canonical = '/docs/' + DEFAULT_VERSION + '/' + section_page

    return render_template('docs.html',
                           title=title,
                           index=Documentation.get_index(version, page),
                           content=content,
                           current_version=version,
                           versions=Documentation.get_doc_versions(),
                           current_section=section,
                           canonical=canonical)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


def is_version(version):
    return version in Documentation.get_doc_versions()
