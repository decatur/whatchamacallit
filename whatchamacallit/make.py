import importlib
import re
import shutil
from html.parser import HTMLParser
from pathlib import Path
from typing import List, Tuple, Generator, Dict
import importlib.util

try:
    import importlib_resources as resources
except ModuleNotFoundError:
    from importlib import resources


class ImportToPackageMapper:
    def __init__(self, root_path: str):
        self.root_path = root_path

    def __contains__(self, item) -> bool:
        if not re.match(r'\w+/', item):
            return False
        return importlib.util.find_spec(item[:-1]) is not None

    def __getitem__(self, item):
        if not self.__contains__(item):
            raise KeyError(item)
        return self.root_path + '/@' + item


def process_file(source: Path, target: Path, spec_mapping: Dict[str, str]):
    if not target.parent.is_dir():
        target.parent.mkdir(parents=True)
    if source.suffix in {'.html', '.js'}:
        t = read_file(source, spec_mapping)
        target.write_text(t, encoding='utf8')
    else:
        shutil.copy2(source.as_posix(), target.as_posix())


def read_file(source: Path, imports: Dict[str, str]) -> str:
    print('read_file ' + source.as_posix())
    src = source.read_text(encoding='utf8')
    processor = process_imports if source.suffix == '.js' else process_imports_html
    src, was_patched = processor(src, imports)
    # TODO: Cache processed modules
    return src


def process_imports(src: str, imports: Dict[str, str], scopes: dict = None) -> Tuple[str, bool]:
    """
    Remaps the imports and exports in the specified Javascript module according the import map.
    This is the Python equivalence to https://github.com/guybedford/es-module-shims for Javascript.

    :param src:
    :param imports: See https://github.com/WICG/import-maps
    :param scopes: Not used. See https://github.com/WICG/import-maps
    :return:
    """

    # Skip initial comments. Note this always matches.
    m = re.match(r'(\s*(/\*.*?\*/|//[^\r\n]*))*', src, flags=re.DOTALL)
    # print(m.group())
    # index = 0
    # for m in re.finditer(r'(\s*(/\*.*?\*/|//[^\r\n]*))*', src, flags=re.DOTALL):
    #     print(m)
    #     index = m.end()
    #     print(m.group())
    end_of_comments = m.end()
    m = re.search(r'(function|const|let|var)\s', src[end_of_comments:], flags=re.DOTALL)
    if m is None:
        # TODO: Handle empty module
        return src, False

    import_section = src[end_of_comments:end_of_comments + m.start()]
    is_import_section = re.match(r'\s*(import|export)\s', import_section) is not None
    if is_import_section:
        was_patched = False
        a = []
        index = 0
        for spec_match in re.finditer(r'(import|export).*? ["\'](\w+/)', import_section, flags=re.DOTALL):
            specifier = spec_match.group(2)
            assert specifier in imports, f'EcmaScript bare specifier not mapped: {specifier}'
            was_patched = True
            a.append(import_section[index:spec_match.start(2)])
            index = spec_match.end(2)
            a.append(imports[specifier])

        a.append(import_section[index:])
        import_section = ''.join(a)

        if was_patched:
            return src[0:end_of_comments] + import_section + src[end_of_comments + m.start():], was_patched
        else:
            return src, False
    else:
        return src, False


class MyHTMLParser(HTMLParser):
    def error(self, message):
        raise Exception(message)

    def __init__(self, import_mappings):
        super().__init__()
        self.import_mappings = import_mappings
        self.is_script = False
        self.buffer: List[str] = []
        self.was_patched = False

    def print(self, data):
        self.buffer.append(data)

    def process_ref(self, ref: str) -> str:
        parts = ref.split('/')
        if len(parts) > 1 and parts[0] + '/' in self.import_mappings:
            return ref.replace(parts[0] + '/', self.import_mappings[parts[0] + '/'])
        return ref

    def handle_starttag(self, tag: str, attrs):
        tag = tag.lower()
        self.is_script = (tag == "script")
        self.print('<' + tag)
        for key, value in attrs:
            if key in {'src', 'href', 'cite', 'data', 'srcset'}:
                value = self.process_ref(value)
            self.print(f' {key}')
            if value is not None:
                self.print(f'="{value}"')
        self.print('>')
        if tag == "head":
            self.print(f'<link href="{self.import_mappings.root_path}/" rel="index">')

    def handle_endtag(self, tag):
        self.is_script = False
        self.print('</' + tag + '>')

    def handle_data(self, data):
        if self.is_script:
            data, was_patched = process_imports(data, self.import_mappings)
            self.was_patched |= was_patched

        self.print(data)

    def handle_decl(self, data):
        self.print(f'<!{data}>')


def process_imports_html(src: str, imports: Dict[str, str], scopes: dict = None) -> Tuple[str, bool]:
    parser = MyHTMLParser(imports)
    parser.feed(src)
    return ''.join(parser.buffer), False


def process_dir(source: Generator[Path, None, None], target_root: Path, spec_mapping: Dict[str, str]):
    for elem in source:
        if elem.is_file() and elem.suffix in {'.html', '.js', '.css'}:
            process_file(elem, target_root / elem, spec_mapping)


def process_dir_recursive(source: Path, target_root: Path, spec_mapping: Dict[str, str]):
    for elem in source.rglob('*.*'):
        p = Path('./') / elem
        if p.is_file() and elem.suffix in {'.html', '.js', '.css'}:
            process_file(p, target_root / elem, spec_mapping)


def resolve_package_resource(path: Path) -> Path:
    if len(path.parts) == 1 or not path.suffix or not path.parts[0][0] == '@':
        return path

    prefix = path.parts[0][1:]
    # Only finds the spec if package contains a __init__.py!

    spec = importlib.util.find_spec(prefix)
    if not spec:
        return path

    # Hopefully this also works for nested directories, see
    # https://gitlab.com/python-devs/importlib_resources/-/issues/58
    return resources.files(prefix).joinpath(Path(*path.parts[1:]))
