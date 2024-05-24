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
selected_icon_family = icon_families[args.icon_family]


class FunnyJsonExplorer:
    def __init__(self, style_factory, icon_family):
        self.style_factory = style_factory
        self.icon_family = icon_family

    def show(self, data):
        builder = JSONBuilder()
        root = builder.build(data)
        style = self.style_factory.create_style()
        print(root.display(style, self.icon_family))

    def load(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)

# 组件基类
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

class Leaf(Component):
    def __init__(self, name, value=None):
        super().__init__(name)
        self.value = value
        self.icon = None

    def display(self, style, icon_family, prefix=''):
        self.icon = icon_family['Leaf']
        return style.render_leaf(self, icon_family, prefix)


# 风格接口
class Style:
    def render_container(self, container, icon_family, prefix):
        icon = icon_family['Container']
        # 渲染逻辑使用 icon 变量

    def render_leaf(self, leaf, icon_family, prefix):
        icon = icon_family['Leaf']
        # 渲染逻辑使用 icon 变量


# 树形风格
class TreeStyle(Style):
    def render_container(self, container, icon_family, prefix):
        result = f"{prefix}├─ {icon_family['Container']} {container.name}\n"
        for i, child in enumerate(container.children):
            if i == len(container.children) - 1:
                result += child.display(self, icon_family, prefix + "└── ")
            else:
                result += child.display(self, icon_family, prefix + "│   ")
        return result

    def render_leaf(self, leaf, icon_family, prefix):
        return f"{prefix}└─ {icon_family['Leaf']} {leaf.name}: {leaf.value}\n"

# 矩形风格
class RectangleStyle(Style):
    def render_container(self, container, icon_family, prefix):
        result = f"{prefix}┌─ {icon_family['Container']} {container.name} ─────\n"
        for child in container.children:
            result += child.display(self, icon_family, prefix + "│  ")
        result += f"{prefix}└─────────────\n"
        return result

    def render_leaf(self, leaf, icon_family, prefix):
        return f"{prefix}├─ {icon_family['Leaf']} {leaf.name}: {leaf.value}\n"

# 抽象工厂接口
class StyleFactory:
    def create_style(self):
        raise NotImplementedError

# 树形风格工厂
class TreeStyleFactory(StyleFactory):
    def create_style(self):
        return TreeStyle()

# 矩形风格工厂
class RectangleStyleFactory(StyleFactory):
    def create_style(self):
        return RectangleStyle()

# JSON 构建器
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

# 加载 JSON 文件
def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)
    
def main():
    data = load_json(args.file)
    explorer = FunnyJsonExplorer(TreeStyleFactory() if args.style == 'tree' else RectangleStyleFactory(), selected_icon_family)
    explorer.show(data)

if __name__ == '__main__':
    main()
