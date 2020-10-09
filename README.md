Alita Index
===========

![Python 3.8](https://img.shields.io/badge/python-3.8-blue)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: GNU Affero General Public License version 3](https://img.shields.io/badge/license-%20%09AGPL--3.0--only-blue)](LICENSE)

Source code for [www.alita-index.com](https://www.alita-index.com/). Written in
Python with Django and Django REST framework.

Dependencies (Ubuntu): `python3 python3-dev libz-dev libjpeg-dev libfreetype6-dev libmemcached-dev`

```sh
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```

License
-------

Copyright © 2019-2020 Alita Index / Caeglathatur

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License version 3 as
published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

-------------------------

normalize.css

Copyright © Nicolas Gallagher and Jonathan Neal

MIT License

-------------------------

Roboto font

Copyright © 2011 Google Inc.

Apache License, version 2.0
