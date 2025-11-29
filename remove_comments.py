import os
import re

PROJECT_ROOT = '/home/boomboy/projects/batlax2'
DOCS_ROOT = os.path.join(PROJECT_ROOT, 'docs')


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_docs_path(file_path):
    rel_path = os.path.relpath(file_path, PROJECT_ROOT)
    docs_path = os.path.join(DOCS_ROOT, rel_path)
    return docs_path + '_comments.md'

def process_python(content):
    lines = content.splitlines(keepends=True)
    new_lines = []
    comments = []
    
    for i, line in enumerate(lines):
        if '#' in line:
            
            if i == 0 and line.startswith('#!'):
                new_lines.append(line)
                continue
                
            parts = line.split('#', 1)
            code_part = parts[0]
            comment_part = '#' + parts[1]
            
            sq_count = code_part.count("'")
            dq_count = code_part.count('"')
            
            if sq_count % 2 == 0 and dq_count % 2 == 0:
                if code_part.strip() == '':
                    pass
                else:
                    if line.endswith('\n'):
                        new_lines.append(code_part.rstrip() + '\n')
                    else:
                        new_lines.append(code_part.rstrip())
                
                comments.append(f"Line {i+1}: {comment_part.strip()}")
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    return "".join(new_lines), comments

def process_js_style(content):
    comments = []
    
    
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )

    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            start_pos = match.start()
            line_num = content.count('\n', 0, start_pos) + 1
            comments.append(f"Line {line_num}: {s}")
            return " " if s.startswith('/*') else ""
        else:
            return s

    new_content = re.sub(pattern, replacer, content)
    
    
    final_lines = []
    for line in new_content.splitlines(keepends=True):
        if line.strip() == '':
            continue
        final_lines.append(line)
        
    return "".join(final_lines), comments

def process_html(content):
    comments = []
    
    pattern = re.compile(r'<!--.*?-->', re.DOTALL)
    
    def replacer(match):
        s = match.group(0)
        start_pos = match.start()
        line_num = content.count('\n', 0, start_pos) + 1
        comments.append(f"Line {line_num}: {s}")
        return ""

    new_content = re.sub(pattern, replacer, content)
    
    final_lines = []
    for line in new_content.splitlines(keepends=True):
        if line.strip() == '':
            continue
        final_lines.append(line)
        
    return "".join(final_lines), comments

def process_vue(content):
    
    content_no_html, html_comments = process_html(content)
    final_content, js_comments = process_js_style(content_no_html)
    
    return final_content, html_comments + js_comments

def main():
    for root, dirs, files in os.walk(PROJECT_ROOT):
        if '.git' in dirs: dirs.remove('.git')
        if 'venv' in dirs: dirs.remove('venv')
        if 'node_modules' in dirs: dirs.remove('node_modules')
        if '__pycache__' in dirs: dirs.remove('__pycache__')
        if 'docs' in dirs: dirs.remove('docs')
        if '.gemini' in dirs: dirs.remove('.gemini')
        
        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()
            
            new_content = None
            comments = []
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                if ext == '.py':
                    new_content, comments = process_python(content)
                elif ext in ['.js', '.css', '.ts', '.jsx']:
                    new_content, comments = process_js_style(content)
                elif ext in ['.html']:
                    new_content, comments = process_html(content)
                elif ext in ['.vue']:
                    new_content, comments = process_vue(content)
                
                if comments:
                    docs_path = get_docs_path(file_path)
                    ensure_dir(docs_path)
                    
                    
                    with open(docs_path, 'w', encoding='utf-8') as f:
                        f.write(f"# Comments extracted from {os.path.basename(file_path)}\n\n")
                        for c in comments:
                            f.write(f"- {c}\n")
                    
                    if new_content is not None:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                    
                    print(f"Processed {file_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

if __name__ == '__main__':
    main()
