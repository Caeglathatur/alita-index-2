- {% if e.url %}[{{ e.title }}]({{ e.url }}){% else %}{{ e.title }}{% endif %}.{% if e.authors_names %} {{ e.authors_names|join:', '}}.{% endif %}{% if e.description %} {{ e.description }}{% endif %}{% if e.length_display %} {{ e.length_display }}.{% endif %}{% for id in e.identifiers %} {{ id.type.name }}: {{ id.value }}.{% endfor %}
{% for s in e.children.all %}  {% include 'fragments/sub-entry.md' %}
{% for s in s.children.all %}    {% include 'fragments/sub-entry.md' %}
{% for s in s.children.all %}      {% include 'fragments/sub-entry.md' %}
{% for s in s.children.all %}        {% include 'fragments/sub-entry.md' %}
{% for s in s.children.all %}          {% include 'fragments/sub-entry.md' %}
{% for s in s.children.all %}            {% include 'fragments/sub-entry.md' %}
{% for s in s.children.all %}              {% include 'fragments/sub-entry.md' %}
{% for s in s.children.all %}                {% include 'fragments/sub-entry.md' %}
{% for s in s.children.all %}                  {% include 'fragments/sub-entry.md' %}
{% for s in s.children.all %}                    {% include 'fragments/sub-entry.md' %}{% endfor %}{% endfor %}{% endfor %}{% endfor %}{% endfor %}{% endfor %}{% endfor %}{% endfor %}{% endfor %}{% endfor %}