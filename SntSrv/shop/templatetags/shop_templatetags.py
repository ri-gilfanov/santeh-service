from django import template

register = template.Library()

@register.simple_tag
def is_child(node, searched):
    def recursive_searching(node, searched):
        #set_.add(node.id)
        if searched.id is node.id or node.children.filter(id=searched.id).exists():
            return True
        else:
            for child in node.children.all():
                if child.children.filter(id=searched.id).exists():
                    return True
                else:
                    recursive_searching(child, searched)
    flag = False
    #set_ = set()
    flag = recursive_searching(node, searched)
    return flag
