Alita Index
===========

**Table of Contents**

{% for c in categories %}- [{{ c.name }}](#{{ c.name|slugify }})
{% for c in c.children_filtered %}  - [{{ c.name }}](#{{ c.name|slugify }})
{% for c in c.children_filtered %}    - [{{ c.name }}](#{{ c.name|slugify }})
{% for c in c.children_filtered %}      - [{{ c.name }}](#{{ c.name|slugify }})
{% for c in c.children_filtered %}        - [{{ c.name }}](#{{ c.name|slugify }})
{% endfor %}{% endfor %}{% endfor %}{% endfor %}{% endfor %}
{% for c in categories %}## {{ c.name }}

{% for e in c.entries_filtered %}{% include 'fragments/entry.md' %}{% endfor %}
{% for c in c.children_filtered %}### {{ c.name }}

{% for e in c.entries_filtered %}{% include 'fragments/entry.md' %}{% endfor %}
{% for c in c.children_filtered %}#### {{ c.name }}

{% for e in c.entries_filtered %}{% include 'fragments/entry.md' %}{% endfor %}
{% for c in c.children_filtered %}##### {{ c.name }}

{% for e in c.entries_filtered %}{% include 'fragments/entry.md' %}{% endfor %}
{% for c in c.children_filtered %}###### {{ c.name }}

{% for e in c.entries_filtered %}{% include 'fragments/entry.md' %}{% endfor %}{% endfor %}{% endfor %}{% endfor %}{% endfor %}{% endfor %}