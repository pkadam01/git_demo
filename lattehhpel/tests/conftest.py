import os


def pytest_html_report_title(report):
    this_path = os.path.dirname(os.path.abspath(__file__))
    meta = {}
    with open(os.path.join(this_path, '../about.py')) as f:
        exec(f.read(), meta)

    report.title = f"LATTE HH PEL{meta['__version__']} Qualification Kit Results"


def pytest_configure(config):
    config._metadata['Computer'] = os.environ['COMPUTERNAME']
    config._metadata['User'] = os.environ['USERNAME']
