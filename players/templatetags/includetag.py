from django import template
from django.template import Node, NodeList, TemplateSyntaxError
from django.template import loader_tags
from django.template.loader import get_template
from django.utils.html import escape


register = template.Library()

class IncludeNode(Node):
        def __init__(self, nodelist, path):
                self.template = get_template(path)
                self.nodelist, self.path = NodeList(nodelist), path

        def __repr__(self):
                return "<Include Node: %s Contents: %r>" % (self.path, self.nodelist)
        
        def render(self, context):
                parent_blocks = dict([(n.name, n) for n in self.template.nodelist.get_nodes_by_type(PartNode)])
                for part_node in self.nodelist.get_nodes_by_type(PartNode):
                        parent_block = parent_blocks[part_node.name]
                        parent_block.nodelist = part_node.nodelist
                return self.template.render(context)

class PartNode(Node):
        def __init__(self, name, nodelist):
                self.nodelist = nodelist
                self.name = name

        def __repr__(self):
                return "<Part Node: %s. Contents: %r>" % (self.name, self.nodelist)

        def render(self, context):
                return self.nodelist.render(context)

def do_include(parser, token):
        try:
                nodelist = parser.parse(('endinclude',))
        except:
                return loader_tags.do_include(parser, token)
        
        partnodes = nodelist.get_nodes_by_type(PartNode)
        
        bits = token.split_contents()
        path = bits[1][1:-1] #always string, delete quotes
        
        parser.delete_first_token()
        return IncludeNode(partnodes, path)

def do_part(parser, token):
        
        bits = token.contents.split()
        if len(bits) != 2:
                raise TemplateSyntaxError, "'%s' tag takes only one argument" % bits[0]
        part_name = bits[1]
        
        nodelist = parser.parse(('endpart',))
        parser.delete_first_token()
        return PartNode(part_name, nodelist)

register.tag('include', do_include)
register.tag('part', do_part)