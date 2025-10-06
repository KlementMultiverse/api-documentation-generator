"""
API Documentation Generator
Auto-generate API docs from Python code using AST parsing and AI

Author: Klement Gunndu
Created: 2025-10-06
Updated: 2025-10-06 - Added full implementation
"""

import ast
import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from dotenv import load_dotenv

load_dotenv()


@dataclass
class APIEndpoint:
    """Represents an API endpoint"""
    name: str
    method: str
    path: str
    description: str
    parameters: List[Dict[str, str]]
    return_type: Optional[str]
    status_codes: List[Dict[str, str]]
    examples: List[Dict[str, Any]]


@dataclass
class APIClass:
    """Represents an API class"""
    name: str
    description: str
    methods: List[Dict[str, Any]]
    attributes: List[Dict[str, str]]


class PythonCodeParser:
    """Parse Python code to extract API information"""

    def parse_file(self, filepath: str) -> Dict[str, Any]:
        """Parse a Python file and extract API info"""
        with open(filepath, 'r') as f:
            code = f.read()

        tree = ast.parse(code)

        api_info = {
            'filename': os.path.basename(filepath),
            'classes': [],
            'functions': [],
            'imports': []
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                api_info['classes'].append(self._parse_class(node))
            elif isinstance(node, ast.FunctionDef):
                if not self._is_method(node):
                    api_info['functions'].append(self._parse_function(node))
            elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                api_info['imports'].append(self._parse_import(node))

        return api_info

    def _parse_class(self, node: ast.ClassDef) -> Dict[str, Any]:
        """Parse a class definition"""
        return {
            'name': node.name,
            'docstring': ast.get_docstring(node) or '',
            'methods': [self._parse_function(n) for n in node.body if isinstance(n, ast.FunctionDef)],
            'bases': [self._get_name(base) for base in node.bases]
        }

    def _parse_function(self, node: ast.FunctionDef) -> Dict[str, Any]:
        """Parse a function definition"""
        return {
            'name': node.name,
            'docstring': ast.get_docstring(node) or '',
            'parameters': [arg.arg for arg in node.args.args],
            'returns': self._get_return_annotation(node),
            'decorators': [self._get_decorator_name(d) for d in node.decorator_list]
        }

    def _is_method(self, node: ast.FunctionDef) -> bool:
        """Check if function is a method (has self parameter)"""
        return len(node.args.args) > 0 and node.args.args[0].arg in ['self', 'cls']

    def _get_name(self, node) -> str:
        """Get name from AST node"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return str(node)

    def _get_return_annotation(self, node: ast.FunctionDef) -> Optional[str]:
        """Get return type annotation"""
        if node.returns:
            return ast.unparse(node.returns)
        return None

    def _get_decorator_name(self, node) -> str:
        """Get decorator name"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Call):
            return self._get_name(node.func)
        return str(node)

    def _parse_import(self, node) -> str:
        """Parse import statement"""
        if isinstance(node, ast.Import):
            return ', '.join(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            names = ', '.join(alias.name for alias in node.names)
            return f"{module}: {names}"
        return ''


class MarkdownGenerator:
    """Generate markdown documentation"""

    def generate(self, api_info: Dict[str, Any], title: str = None) -> str:
        """Generate markdown documentation from API info"""
        md = []

        # Header
        title = title or f"API Documentation - {api_info['filename']}"
        md.append(f"# {title}\n")
        md.append(f"**Generated:** {self._get_timestamp()}\n")
        md.append("---\n")

        # Imports
        if api_info['imports']:
            md.append("## 📦 Imports\n")
            for imp in api_info['imports'][:10]:
                md.append(f"- `{imp}`")
            md.append("\n")

        # Classes
        if api_info['classes']:
            md.append("## 🏛️ Classes\n")
            for cls in api_info['classes']:
                md.append(f"### `{cls['name']}`\n")
                if cls['docstring']:
                    md.append(f"{cls['docstring']}\n")

                if cls['bases']:
                    md.append(f"**Inherits:** {', '.join(cls['bases'])}\n")

                # Methods
                if cls['methods']:
                    md.append("**Methods:**\n")
                    for method in cls['methods']:
                        params = ', '.join(method['parameters'])
                        returns = f" -> {method['returns']}" if method['returns'] else ""
                        md.append(f"- `{method['name']}({params}){returns}`")
                        if method['docstring']:
                            md.append(f"  - {method['docstring'].split(chr(10))[0]}")
                md.append("\n")

        # Functions
        if api_info['functions']:
            md.append("## 🔧 Functions\n")
            for func in api_info['functions']:
                params = ', '.join(func['parameters'])
                returns = f" -> {func['returns']}" if func['returns'] else ""
                md.append(f"### `{func['name']}({params}){returns}`\n")
                if func['docstring']:
                    md.append(f"{func['docstring']}\n")

                if func['decorators']:
                    md.append(f"**Decorators:** {', '.join(func['decorators'])}\n")
                md.append("\n")

        return '\n'.join(md)

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class OpenAPIGenerator:
    """Generate OpenAPI/Swagger documentation"""

    def generate(self, api_info: Dict[str, Any], version: str = "1.0.0") -> Dict[str, Any]:
        """Generate OpenAPI spec from API info"""
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": f"API - {api_info['filename']}",
                "version": version,
                "description": "Auto-generated API documentation"
            },
            "paths": {},
            "components": {
                "schemas": {}
            }
        }

        # Extract endpoints from decorators (Flask/FastAPI style)
        for cls in api_info.get('classes', []):
            for method in cls['methods']:
                if self._is_api_method(method):
                    endpoint = self._extract_endpoint(method)
                    if endpoint:
                        spec['paths'][endpoint['path']] = endpoint['spec']

        for func in api_info.get('functions', []):
            if self._is_api_method(func):
                endpoint = self._extract_endpoint(func)
                if endpoint:
                    spec['paths'][endpoint['path']] = endpoint['spec']

        return spec

    def _is_api_method(self, method: Dict) -> bool:
        """Check if method is an API endpoint"""
        api_decorators = ['app.route', 'router.get', 'router.post', 'router.put',
                         'router.delete', 'get', 'post', 'put', 'delete']
        return any(dec in method.get('decorators', []) for dec in api_decorators)

    def _extract_endpoint(self, method: Dict) -> Optional[Dict]:
        """Extract endpoint information from method"""
        # This is simplified - real implementation would parse decorators
        return {
            'path': f"/{method['name']}",
            'spec': {
                'get': {
                    'summary': method.get('docstring', '').split('\n')[0] if method.get('docstring') else method['name'],
                    'parameters': [
                        {'name': param, 'in': 'query', 'schema': {'type': 'string'}}
                        for param in method['parameters'] if param not in ['self', 'cls']
                    ],
                    'responses': {
                        '200': {
                            'description': 'Successful response',
                            'content': {'application/json': {}}
                        }
                    }
                }
            }
        }


class APIDocumentationGenerator:
    """Main application class"""

    def __init__(self):
        """Initialize the application"""
        self.config = self._load_config()
        self.parser = PythonCodeParser()
        self.md_generator = MarkdownGenerator()
        self.openapi_generator = OpenAPIGenerator()

    def _load_config(self):
        """Load configuration from environment"""
        return {
            'api_key': os.getenv('API_KEY'),
            'output_dir': os.getenv('OUTPUT_DIR', 'docs/api')
        }

    def generate_docs(self, source_path: str, output_format: str = 'markdown') -> str:
        """Generate documentation for a Python file or directory"""
        path = Path(source_path)

        if path.is_file():
            return self._generate_single_file(path, output_format)
        elif path.is_dir():
            return self._generate_directory(path, output_format)
        else:
            raise ValueError(f"Invalid path: {source_path}")

    def _generate_single_file(self, filepath: Path, output_format: str) -> str:
        """Generate docs for a single file"""
        print(f"📄 Parsing {filepath.name}...")
        api_info = self.parser.parse_file(str(filepath))

        if output_format == 'markdown':
            docs = self.md_generator.generate(api_info)
            output_file = filepath.stem + '_api.md'
        elif output_format == 'openapi':
            docs = json.dumps(self.openapi_generator.generate(api_info), indent=2)
            output_file = filepath.stem + '_openapi.json'
        elif output_format == 'json':
            docs = json.dumps(api_info, indent=2)
            output_file = filepath.stem + '_api.json'
        else:
            raise ValueError(f"Unsupported format: {output_format}")

        # Save to output directory
        output_dir = Path(self.config['output_dir'])
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / output_file

        with open(output_path, 'w') as f:
            f.write(docs)

        print(f"✅ Documentation saved to {output_path}")
        return str(output_path)

    def _generate_directory(self, dirpath: Path, output_format: str) -> str:
        """Generate docs for all Python files in directory"""
        py_files = list(dirpath.rglob('*.py'))
        print(f"📁 Found {len(py_files)} Python files in {dirpath}")

        results = []
        for py_file in py_files:
            if '__pycache__' not in str(py_file):
                try:
                    output_path = self._generate_single_file(py_file, output_format)
                    results.append(output_path)
                except Exception as e:
                    print(f"⚠️  Error processing {py_file}: {e}")

        print(f"\n✅ Generated documentation for {len(results)} files")
        return f"Generated {len(results)} documentation files"

    def run(self):
        """Main application logic"""
        print("🚀 API Documentation Generator")
        print("================================\n")

        # Demo: Generate docs for this file
        demo_file = __file__
        print(f"Demo: Generating docs for {demo_file}\n")

        try:
            self.generate_docs(demo_file, output_format='markdown')
            self.generate_docs(demo_file, output_format='json')
            print("\n✨ Demo complete! Check docs/api/ directory")
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='API Documentation Generator - Auto-generate docs from Python code'
    )
    parser.add_argument('source', nargs='?', help='Python file or directory to document')
    parser.add_argument('-f', '--format', default='markdown',
                       choices=['markdown', 'openapi', 'json'],
                       help='Output format (default: markdown)')
    parser.add_argument('-o', '--output', help='Output directory (default: docs/api)')
    parser.add_argument('--demo', action='store_true', help='Run demo mode')

    args = parser.parse_args()

    app = APIDocumentationGenerator()

    if args.output:
        app.config['output_dir'] = args.output

    if args.demo or not args.source:
        app.run()
    else:
        try:
            app.generate_docs(args.source, output_format=args.format)
        except Exception as e:
            print(f"❌ Error: {e}")
            return 1

    return 0


if __name__ == "__main__":
    exit(main())
