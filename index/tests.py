"""
Copyright © 2019-2020 Alita Index / Caeglathatur

This file is part of Alita Index.

Alita Index is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License version 3 as
published by the Free Software Foundation.

Alita Index is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Alita Index.  If not, see <https://www.gnu.org/licenses/>.
"""

from django.test import TestCase

from . import utils


class TestNewlineRemoval(TestCase):
    def test_1(self):
        self.assertEqual(
            utils.remove_newlines("asdf\nasf\n\n yuttyd uih \n uiygy\n\n"),
            "asdf asf  yuttyd uih   uiygy ",
        )

    def test_2(self):
        self.assertEqual(
            utils.remove_newlines(
                "\n\n\n\n\n\nuytf uyigyu uiygg 67uiyg 877 \noihiouhyg\n\niouhiuoh "
                "g8u7g kjh\n"
            ),
            " uytf uyigyu uiygg 67uiyg 877  oihiouhyg iouhiuoh g8u7g kjh ",
        )

    def test_3(self):
        self.assertEqual(
            utils.remove_newlines(
                "asdf iuh iuh liuh  iluh.\ncfidfsej sfdiosdf sf iosd sfio sf\n\n- "
                "item1\n- item 2\n- item3\n\nfinal line."
            ),
            "asdf iuh iuh liuh  iluh. cfidfsej sfdiosdf sf iosd sfio sf - item1 - item "
            "2 - item3 final line.",
        )

    def test_carriage_returns(self):
        self.assertEqual(
            utils.remove_newlines("asdf\n\rasf\n\r\n\r yuttyd uih \n\r uiygy\n\r\n\r"),
            "asdf asf  yuttyd uih   uiygy ",
        )
