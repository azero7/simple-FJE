import argparse
import json
from config import icon_families  # 引入图标族配置

# 解析命令行参数
parser = argparse.ArgumentParser(description="Funny JSON Explorer")
parser.add_argument('-f', '--file', type=str, required=True, help='Path to the JSON file')
parser.add_argument('-s', '--style', choices=['tree', 'rectangle'], default='tree', help='Visualization style')
parser.add_argument('-i', '--icon_family', choices=list(icon_families.keys()), default='basic', help='Icon family to use')
args = parser.parse_args()

# 使用选择的图标族
try:
    selected_icon_family = icon_families[args.icon_family]
except KeyError:
    print(f"Error: Icon family '{args.icon_family}' not found in configuration.")
    exit(1)

class Component:
    def __init__(self, name):
        self.name = name

    def display(self, style, icon_family, prefix=''):
        raise NotImplementedError

class Container(Component):
    def __init__(self, name, level=0):
        super().__init__(name)
        self.children = []
        self.level = level
        self.icon = None

    def add(self, component):
        self.children.append(component)

    def display(self, style, icon_family, prefix=''):
        self.icon = icon_family['Container']
        return style.render_container(self, icon_family, prefix)

    # 通过实现 __iter__ 方法，Container 类可以被迭代，例如在 TreeStyle 和 RectangleStyle 中遍历其子组件。
    def __iter__(self):
        return iter(self.children)

class Leaf(Component):
    def __init__(self, name, value=None):
        super().__init__(name)
        self.value = value
        self.icon = None

    def display(self, style, icon_family, prefix=''):
        self.icon = icon_family['Leaf']
        return style.render_leaf(self, icon_family, prefix)

# 策略接口 Style 类
class Style:
    def render_container(self, container, icon_family, prefix):
        raise NotImplementedError

    def render_leaf(self, leaf, icon_family, prefix):
        raise NotImplementedError

# 具体的策略实现 TreeStyle 和 RectangleStyle 类
class TreeStyle(Style):
    def render_container(self, container, icon_family, prefix):
        result = f"{prefix}├─ {icon_family['Container']} {container.name}\n"
        new_prefix = prefix + "│   "
        for i, child in enumerate(container):
            if i == len(container.children) - 1:
                new_prefix = prefix + "    "
            result += child.display(self, icon_family, new_prefix)
        return result

    def render_leaf(self, leaf, icon_family, prefix):
        return f"{prefix}└─ {icon_family['Leaf']} {leaf.name}: {leaf.value}\n"

class RectangleStyle(Style):
    def render_container(self, container, icon_family, prefix):
        result = f"{prefix}┌─ {icon_family['Container']} {container.name} ─────\n"
        for child in container:
            result += child.display(self, icon_family, prefix + "│  ")
        result += f"{prefix}└─────────────\n"
        return result

    def render_leaf(self, leaf, icon_family, prefix):
        return f"{prefix}├─ {icon_family['Leaf']} {leaf.name}: {leaf.value}\n"

# 使用 StyleFactory 来创建具体的策略对象
class StyleFactory:
    def create_style(self):
        raise NotImplementedError

class TreeStyleFactory(StyleFactory):
    def create_style(self):
        return TreeStyle()

class RectangleStyleFactory(StyleFactory):
    def create_style(self):
        return RectangleStyle()

class JSONBuilder:
    def build(self, data):
        if isinstance(data, dict):
            parent = Container("root")
            for key, value in data.items():
                child = self.build(value)
                child.name = key
                parent.add(child)
            return parent
        elif data is not None:
            return Leaf("value", data)
        return Leaf("null")

def load_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: File '{filepath}' is not a valid JSON.")
        exit(1)

# FunnyJsonExplorer 中选择并使用具体的策略
class FunnyJsonExplorer:
    def __init__(self, style_factory, icon_family):
        self.style_factory = style_factory
        self.icon_family = icon_family

    def show(self, data):
        builder = JSONBuilder()
        root = builder.build(data)
        style = self.style_factory.create_style()
        print(root.display(style, self.icon_family))

# 根据命令行参数选择合适的策略，并展示 JSON 数据
def main():
    data = load_json(args.file)
    explorer = FunnyJsonExplorer(TreeStyleFactory() if args.style == 'tree' else RectangleStyleFactory(), selected_icon_family)
    explorer.show(data)

if __name__ == '__main__':
    main()
