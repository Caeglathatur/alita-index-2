Alita Index
===========

**Table of Contents**

{% for c in categories %}- [{{ c.name }}](#{{ c.name|slugify }})
{% for c in c.children.all %}  - [{{ c.name }}](#{{ c.name|slugify }})
{% for c in c.children.all %}    - [{{ c.name }}](#{{ c.name|slugify }})
{% for c in c.children.all %}      - [{{ c.name }}](#{{ c.name|slugify }})
{% for c in c.children.all %}        - [{{ c.name }}](#{{ c.name|slugify }})
{% endfor %}{% endfor %}{% endfor %}{% endfor %}{% endfor %}
{% for c in categories %}## {{ c.name }}

{% for e in c.entries_visible %}{% include 'fragments/entry.md' %}{% endfor %}
{% for c in c.children.all %}### {{ c.name }}

{% for e in c.entries_visible %}{% include 'fragments/entry.md' %}{% endfor %}
{% for c in c.children.all %}#### {{ c.name }}

{% for e in c.entries_visible %}{% include 'fragments/entry.md' %}{% endfor %}
{% for c in c.children.all %}##### {{ c.name }}

{% for e in c.entries_visible %}{% include 'fragments/entry.md' %}{% endfor %}
{% for c in c.children.all %}###### {{ c.name }}

{% for e in c.entries_visible %}{% include 'fragments/entry.md' %}{% endfor %}{% endfor %}{% endfor %}{% endfor %}{% endfor %}{% endfor %}