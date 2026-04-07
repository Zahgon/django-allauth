from django import template
from django.template.base import FilterExpression, kwarg_re
from django.template.loader import render_to_string
from django.template.loader_tags import ExtendsNode
from django.utils.safestring import mark_safe


SLOTS_CONTEXT_KEY = "slots_context"
LAYOUT_CONTEXT_KEY = "layout_context"


def parse_tag(token, parser):
    pass


register = template.Library()


@register.tag(name="slot")
def do_slot(parser, token):
    pass


class SlotNode(template.Node):
    def __init__(self, name, nodelist):
        self.name = name
        self.nodelist = nodelist

    def render(self, context):
        slots = context.render_context.get(SLOTS_CONTEXT_KEY)
        with context.push():
            if slots is None:
                if self.name in context["slots"]:
                    return "".join(context["slots"][self.name])
                return self.nodelist.render(context)
            else:
                result = self.nodelist.render(context)
                slot_list = slots.setdefault(self.name, [])
                slot_list.append(result)
                return ""


@register.tag(name="element")
def do_element(parser, token):
    pass


class ElementNode(template.Node):
    def __init__(self, nodelist, element, kwargs):
        self.element = element
        self.kwargs = kwargs
        self.nodelist = nodelist

    def render(self, context):
        from allauth.account.app_settings import TEMPLATE_EXTENSION

        slots = {}
        extends_context = context.render_context.get(ExtendsNode.context_key)
        layout = None
        if extends_context:
            # Extract layout from the {% extends %} tags
            for ec in extends_context:
                prefix = "allauth/layouts/"
                if ec.template_name.startswith(prefix):
                    layout = ec.template_name[len(prefix) :].replace(".html", "")
                    break
        if not layout:
            # In case we're in a {% element %} element, the extends context is
            # not there.
            layout = context.render_context.get(LAYOUT_CONTEXT_KEY)
        if not layout:
            # Or, similarly, for {% include %} we also lose the extends context.
            layout = context.get("page_layout")
        template_names = []
        if layout:
            template_names.append(f"allauth/elements/{self.element}__{layout}.html")
        template_names.append(f"allauth/elements/{self.element}.html")
        with context.render_context.push(
            **{SLOTS_CONTEXT_KEY: slots, LAYOUT_CONTEXT_KEY: layout}
        ):
            slots["default"] = [self.nodelist.render(context)]
            attrs = {}
            for k, v in self.kwargs.items():
                attrs[k] = v.resolve(context)
            tags = attrs.get("tags")
            if tags:
                attrs["tags"] = [tag.strip() for tag in tags.split(",")]
            with context.push(
                slots=slots,
                attrs=attrs,
                origin=self.origin.template_name.replace(f".{TEMPLATE_EXTENSION}", ""),
            ) as element_context:
                return render_to_string(
                    template_names, element_context.context.flatten()
                )


@register.tag(name="setvar")
def do_setvar(parser, token):
    pass


class SetVarNode(template.Node):
    def __init__(self, nodelist, var):
        self.nodelist = nodelist
        self.var = var

    def render(self, context):
        context[self.var] = mark_safe(self.nodelist.render(context).strip())  # nosec
        return ""
