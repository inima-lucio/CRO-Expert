#!/usr/bin/env python3
"""
CRO Expert — Premium Report Generator v2.0
Usage: python report_generator.py <analysis_dir> [--output report.html] [--pdf]
"""

import sys, json, os, base64, math
from datetime import datetime
from pathlib import Path


# ─── Brand asset ─────────────────────────────────────────────────────────────
INIMA_LOGO_B64 = "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4KPCEtLSBHZW5lcmF0b3I6IEFkb2JlIElsbHVzdHJhdG9yIDE2LjAuMCwgU1ZHIEV4cG9ydCBQbHVnLUluIC4gU1ZHIFZlcnNpb246IDYuMDAgQnVpbGQgMCkgIC0tPgo8IURPQ1RZUEUgc3ZnIFBVQkxJQyAiLS8vVzNDLy9EVEQgU1ZHIDEuMS8vRU4iICJodHRwOi8vd3d3LnczLm9yZy9HcmFwaGljcy9TVkcvMS4xL0RURC9zdmcxMS5kdGQiIFsKCTwhRU5USVRZIG5zX2V4dGVuZCAiaHR0cDovL25zLmFkb2JlLmNvbS9FeHRlbnNpYmlsaXR5LzEuMC8iPgoJPCFFTlRJVFkgbnNfYWkgImh0dHA6Ly9ucy5hZG9iZS5jb20vQWRvYmVJbGx1c3RyYXRvci8xMC4wLyI+Cgk8IUVOVElUWSBuc19ncmFwaHMgImh0dHA6Ly9ucy5hZG9iZS5jb20vR3JhcGhzLzEuMC8iPgoJPCFFTlRJVFkgbnNfdmFycyAiaHR0cDovL25zLmFkb2JlLmNvbS9WYXJpYWJsZXMvMS4wLyI+Cgk8IUVOVElUWSBuc19pbXJlcCAiaHR0cDovL25zLmFkb2JlLmNvbS9JbWFnZVJlcGxhY2VtZW50LzEuMC8iPgoJPCFFTlRJVFkgbnNfc2Z3ICJodHRwOi8vbnMuYWRvYmUuY29tL1NhdmVGb3JXZWIvMS4wLyI+Cgk8IUVOVElUWSBuc19jdXN0b20gImh0dHA6Ly9ucy5hZG9iZS5jb20vR2VuZXJpY0N1c3RvbU5hbWVzcGFjZS8xLjAvIj4KCTwhRU5USVRZIG5zX2Fkb2JlX3hwYXRoICJodHRwOi8vbnMuYWRvYmUuY29tL1hQYXRoLzEuMC8iPgpdPgo8c3ZnIHZlcnNpb249IjEuMSIgaWQ9IkNhcGFfMSIgeG1sbnM6eD0iJm5zX2V4dGVuZDsiIHhtbG5zOmk9IiZuc19haTsiIHhtbG5zOmdyYXBoPSImbnNfZ3JhcGhzOyIKCSB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB4PSIwcHgiIHk9IjBweCIgd2lkdGg9IjE3MHB4IiBoZWlnaHQ9IjYzcHgiCgkgdmlld0JveD0iMCAwIDE3MCA2MyIgZW5hYmxlLWJhY2tncm91bmQ9Im5ldyAwIDAgMTcwIDYzIiB4bWw6c3BhY2U9InByZXNlcnZlIj4KPG1ldGFkYXRhPgoJPHNmdyAgeG1sbnM9IiZuc19zZnc7Ij4KCQk8c2xpY2VzPjwvc2xpY2VzPgoJCTxzbGljZVNvdXJjZUJvdW5kcyAgaGVpZ2h0PSI2Mi41MjQiIHdpZHRoPSIxNjUuOTQ5IiB5PSItMTIiIHg9Ii0yNS4yMTIiIGJvdHRvbUxlZnRPcmlnaW49InRydWUiPjwvc2xpY2VTb3VyY2VCb3VuZHM+Cgk8L3Nmdz4KPC9tZXRhZGF0YT4KPGc+Cgk8cGF0aCBmaWxsPSIjRkZGRkZGIiBkPSJNOS4zNzYsMy41MmMwLDAuODMyLTAuMywxLjU0Ny0wLjg5OCwyLjE0NWMtMC41OTksMC42LTEuMzE0LDAuODk4LTIuMTQ1LDAuODk4CgkJYy0wLjgzMywwLTEuNTQ4LTAuMjk5LTIuMTQ3LTAuODk4QzMuNTg4LDUuMDY3LDMuMjg4LDQuMzUyLDMuMjg4LDMuNTJjMC0wLjgzMywwLjMtMS41NDgsMC44OTgtMi4xNDYKCQljMC41OTktMC42LDEuMzE0LTAuODk4LDIuMTQ3LTAuODk4YzAuODMxLDAsMS41NDYsMC4yOTksMi4xNDUsMC44OThDOS4wNzcsMS45NzIsOS4zNzYsMi42ODgsOS4zNzYsMy41MnogTTMuODk3LDEzLjI2CgkJYzAtMC42NjksMC4yMzktMS4yNDMsMC43MTYtMS43MmMwLjQ3Ny0wLjQ3NywxLjA1LTAuNzE2LDEuNzItMC43MTZjMC42NjgsMCwxLjI0MiwwLjIzOSwxLjcxOSwwLjcxNgoJCWMwLjQ3OCwwLjQ3NywwLjcxNSwxLjA1LDAuNzE1LDEuNzJ2MjkuMjIyYzAsMC42NjktMC4yMzgsMS4yNDItMC43MTUsMS43MmMtMC40NzcsMC40NzctMS4wNSwwLjcxNS0xLjcxOSwwLjcxNQoJCWMtMC42NywwLTEuMjQ0LTAuMjM4LTEuNzItMC43MTVjLTAuNDc3LTAuNDc4LTAuNzE2LTEuMDUxLTAuNzE2LTEuNzJWMTMuMjZ6Ii8+Cgk8cGF0aCBmaWxsPSIjRkZGRkZGIiBkPSJNMTYuMDczLDEzLjI2YzAtMC42NjksMC4yMzgtMS4yNDMsMC43MTUtMS43MnMxLjA1MS0wLjcxNiwxLjcyLTAuNzE2YzAuNjcsMCwxLjI0NCwwLjIzOSwxLjcyMSwwLjcxNgoJCWMwLjQ3NiwwLjQ3NywwLjcxNCwxLjA1LDAuNzE0LDEuNzJ2MS45NzhjMy4wNDQtMi45NDEsNi42OTctNC40MTQsMTAuOTU3LTQuNDE0YzQuMzY0LDAsOC4wOTMsMS41NDcsMTEuMTg3LDQuNjQyCgkJYzMuMDk0LDMuMDk2LDQuNjQzLDYuODI0LDQuNjQzLDExLjE4NnYxNS44M2MwLDAuNjY5LTAuMjM5LDEuMjQyLTAuNzE2LDEuNzJjLTAuNDc3LDAuNDc3LTEuMDUsMC43MTUtMS43MiwwLjcxNQoJCWMtMC42NjksMC0xLjI0My0wLjIzOC0xLjcyLTAuNzE1Yy0wLjQ3Ni0wLjQ3OC0wLjcxNS0xLjA1MS0wLjcxNS0xLjcydi0xNS44M2MwLTMuMDIyLTEuMDcxLTUuNjA1LTMuMjExLTcuNzQ2CgkJYy0yLjE0Mi0yLjE0MS00LjcyMy0zLjIxMS03Ljc0OC0zLjIxMWMtMy4wMjIsMC01LjYwNSwxLjA3LTcuNzQ2LDMuMjExcy0zLjIxMSw0LjcyMy0zLjIxMSw3Ljc0NnYxNS44MwoJCWMwLDAuNjY5LTAuMjM4LDEuMjQyLTAuNzE0LDEuNzJjLTAuNDc3LDAuNDc3LTEuMDUxLDAuNzE1LTEuNzIxLDAuNzE1Yy0wLjY2OSwwLTEuMjQ0LTAuMjM4LTEuNzItMC43MTUKCQljLTAuNDc3LTAuNDc4LTAuNzE1LTEuMDUxLTAuNzE1LTEuNzJWMTMuMjZ6Ii8+Cgk8cGF0aCBmaWxsPSIjRkZGRkZGIiBkPSJNNjAuNTEzLDMuNTJjMCwwLjgzMi0wLjI5OCwxLjU0Ny0wLjg5NywyLjE0NWMtMC41OTksMC42LTEuMzE0LDAuODk4LTIuMTQ2LDAuODk4CgkJYy0wLjgzMywwLTEuNTQ4LTAuMjk5LTIuMTQ2LTAuODk4Yy0wLjU5OS0wLjU5OC0wLjg5OC0xLjMxMy0wLjg5OC0yLjE0NWMwLTAuODMzLDAuMjk5LTEuNTQ4LDAuODk4LTIuMTQ2CgkJYzAuNTk4LTAuNiwxLjMxMy0wLjg5OCwyLjE0Ni0wLjg5OGMwLjgzMiwwLDEuNTQ3LDAuMjk5LDIuMTQ2LDAuODk4QzYwLjIxNCwxLjk3Miw2MC41MTMsMi42ODgsNjAuNTEzLDMuNTJ6IE01NS4wMzUsMTMuMjYKCQljMC0wLjY2OSwwLjIzOC0xLjI0MywwLjcxNC0xLjcyczEuMDUxLTAuNzE2LDEuNzItMC43MTZjMC42NywwLDEuMjQzLDAuMjM5LDEuNzE5LDAuNzE2YzAuNDc3LDAuNDc3LDAuNzE2LDEuMDUsMC43MTYsMS43MnYyOS4yMjIKCQljMCwwLjY2OS0wLjIzOSwxLjI0Mi0wLjcxNiwxLjcyYy0wLjQ3NiwwLjQ3Ny0xLjA0OSwwLjcxNS0xLjcxOSwwLjcxNWMtMC42NjksMC0xLjI0NC0wLjIzOC0xLjcyLTAuNzE1CgkJYy0wLjQ3Ny0wLjQ3OC0wLjcxNC0xLjA1MS0wLjcxNC0xLjcyVjEzLjI2eiIvPgoJPHBhdGggZmlsbD0iI0ZGRkZGRiIgZD0iTTcyLjA4MSw0Mi40ODFjMCwwLjY2OS0wLjIzOSwxLjI0Mi0wLjcxNSwxLjcyYy0wLjQ3NywwLjQ3Ny0xLjA1LDAuNzE1LTEuNzIsMC43MTUKCQljLTAuNjcsMC0xLjI0NC0wLjIzOC0xLjcyLTAuNzE1Yy0wLjQ3OC0wLjQ3OC0wLjcxNS0xLjA1MS0wLjcxNS0xLjcyVjEzLjI2YzAtMC42NjksMC4yMzgtMS4yNDMsMC43MTUtMS43MgoJCWMwLjQ3Ni0wLjQ3NywxLjA0OS0wLjcxNiwxLjcyLTAuNzE2YzAuNjY5LDAsMS4yNDMsMC4yMzksMS43MiwwLjcxNmMwLjQ3NiwwLjQ3NywwLjcxNSwxLjA1LDAuNzE1LDEuNzJ2MC42NAoJCWMyLjQxNC0yLjA1LDUuMjU2LTMuMDc1LDguNTIyLTMuMDc1YzMuNjk0LDAsNi44NTEsMS4zMDksOS40NjcsMy45MjZjMC41NDgsMC41NDksMS4wNDUsMS4xMjcsMS40OTEsMS43MzYKCQljMC40NDYtMC42MDksMC45NDMtMS4xODgsMS40OTItMS43MzZjMi42MTctMi42MTgsNS43NzMtMy45MjYsOS40NjUtMy45MjZjMy42OTQsMCw2Ljg1LDEuMzA5LDkuNDY3LDMuOTI2CgkJYzIuNjE4LDIuNjE5LDMuOTI5LDUuNzc0LDMuOTI5LDkuNDY2djE4LjI2NWMwLDAuNjY5LTAuMjQsMS4yNDItMC43MTYsMS43MmMtMC40NzksMC40NzctMS4wNTEsMC43MTUtMS43MiwwLjcxNQoJCWMtMC42NywwLTEuMjQ0LTAuMjM4LTEuNzIxLTAuNzE1Yy0wLjQ3Ny0wLjQ3OC0wLjcxNS0xLjA1MS0wLjcxNS0xLjcyVjI0LjIxN2MwLTIuMzUzLTAuODMzLTQuMzYyLTIuNDk2LTYuMDI2CgkJYy0xLjY2My0xLjY2NC0zLjY3Mi0yLjQ5Ni02LjAyOC0yLjQ5NmMtMi4zNTQsMC00LjM2MywwLjgzMi02LjAyNSwyLjQ5NmMtMS42NjUsMS42NjQtMi40OTYsMy42NzMtMi40OTYsNi4wMjZ2MTguMjY1CgkJYzAsMC42NjktMC4yMzksMS4yNDItMC43MTUsMS43MmMtMC40NzcsMC40NzctMS4wNSwwLjcxNS0xLjcyMSwwLjcxNWMtMC42NjksMC0xLjI0Mi0wLjIzOC0xLjcyLTAuNzE1CgkJYy0wLjQ3OC0wLjQ3OC0wLjcxNi0xLjA1MS0wLjcxNi0xLjcyVjI0LjIxN2MwLTIuMzUzLTAuODMxLTQuMzYyLTIuNDk1LTYuMDI2Yy0xLjY2NS0xLjY2NC0zLjY3My0yLjQ5Ni02LjAyNy0yLjQ5NgoJCXMtNC4zNjIsMC44MzItNi4wMjcsMi40OTZjLTEuNjYzLDEuNjY0LTIuNDk1LDMuNjczLTIuNDk1LDYuMDI2VjQyLjQ4MXoiLz4KCTxnPgoJCTxnPgoJCQk8cGF0aCBmaWxsPSIjRkZGRkZGIiBkPSJNNC4zNjksNTQuMjY5aDEuNDQ2VjYzSDQuMzY5VjU0LjI2OXoiLz4KCQkJPHBhdGggZmlsbD0iI0ZGRkZGRiIgZD0iTTE0LjA1Niw1NC4yNTdsNS44MTMsNS4yMzN2LTUuMjMzaDEuNDU5djguNzMydi0wLjAxMlY2M2wtNS44MjUtNS4yMzN2NS4yMjNoLTEuNDQ3VjU0LjI1N3oiLz4KCQkJPHBhdGggZmlsbD0iI0ZGRkZGRiIgZD0iTTI5LjU2OSw1NC4yNjloNy4yODR2MS40NjFoLTIuOTA2VjYzaC0xLjQ1OXYtNy4yNzFoLTIuOTE5VjU0LjI2OXoiLz4KCQkJPHBhdGggZmlsbD0iI0ZGRkZGRiIgZD0iTTUwLjkwOCw1NC4yNjl2MS40NjFoLTQuMzY3djIuMTg4aDQuMzY3djEuNDQ3aC00LjM2N3YyLjE3Nmg0LjM2N1Y2M2gtNS44MTN2LTguNzMxSDUwLjkwOHoiLz4KCQkJPHBhdGggZmlsbD0iI0ZGRkZGRiIgZD0iTTY0Ljc0Nyw2M2wtMS42ODYtMi45MDRoLTIuNDY2VjYzaC0xLjQ0N3YtOC43MzFoNC4zNjdjMC43OTUsMCwxLjQ3OSwwLjI4NywyLjA1LDAuODU2CgkJCQljMC41NywwLjU2OSwwLjg1NSwxLjI1NCwwLjg1NSwyLjA1MWMwLDAuNjA0LTAuMTcxLDEuMTU0LTAuNTE2LDEuNjQ5Yy0wLjMzNSwwLjQ4NS0wLjc2NCwwLjgzNS0xLjI4NCwxLjA0Mkw2Ni40MTksNjNINjQuNzQ3egoJCQkJIE02My41MTQsNTUuNzI5aC0yLjkydjIuODkzbDIuOTIsMC4wMTNjMC4zOTQsMCwwLjczMy0wLjE0MiwxLjAxOC0wLjQyN2MwLjI4NS0wLjI4NiwwLjQyOC0wLjYyOSwwLjQyOC0xLjAzMgoJCQkJYzAtMC4zOTUtMC4xNDMtMC43MzMtMC40MjgtMS4wMkM2NC4yNDgsNTUuODcyLDYzLjkwOCw1NS43MjksNjMuNTE0LDU1LjcyOXoiLz4KCQkJPHBhdGggZmlsbD0iI0ZGRkZGRiIgZD0iTTgxLjAzOSw2MS41NDFoLTQuMDEzTDc2LjI4NCw2M0g3NC42Nmw0LjM2Ny04LjczMUw4My4zOTMsNjNoLTEuNjI1TDgxLjAzOSw2MS41NDF6IE03Ny43NDMsNjAuMDk2CgkJCQloMi41NjdsLTEuMjgzLTIuNTY3TDc3Ljc0Myw2MC4wOTZ6Ii8+CgkJCTxwYXRoIGZpbGw9IiNGRkZGRkYiIGQ9Ik05NC4zMjUsNTQuMjY5YzAuNjA0LDAsMS4xNjgsMC4xMTQsMS42OTIsMC4zNGMwLjUyMywwLjIyNywwLjk4OCwwLjU0MywxLjM5MSwwLjk0NWwtMS4wMzEsMS4wMwoJCQkJYy0wLjU3Mi0wLjU2OS0xLjI1NC0wLjg1NC0yLjA1Mi0wLjg1NGMtMC40MDMsMC0wLjc3OCwwLjA3Ni0xLjEzMiwwLjIyNmMtMC4zNTMsMC4xNTEtMC42NjEsMC4zNTgtMC45MjUsMC42MjMKCQkJCWMtMC4yNjUsMC4yNjUtMC40NzQsMC41NzItMC42MjksMC45MjRjLTAuMTU1LDAuMzU0LTAuMjMzLDAuNzMxLTAuMjMzLDEuMTMzYzAsMC40MDMsMC4wNzgsMC43ODEsMC4yMzMsMS4xMzQKCQkJCWMwLjE1NSwwLjM1MSwwLjM2MiwwLjY2LDAuNjIyLDAuOTI1YzAuMjYxLDAuMjYzLDAuNTY4LDAuNDcxLDAuOTI2LDAuNjIyYzAuMzU2LDAuMTQ5LDAuNzM0LDAuMjI2LDEuMTM4LDAuMjI2CgkJCQljMC43OSwwLDEuNDcyLTAuMjgxLDIuMDUyLTAuODQybDEuMDMxLDEuMDE5Yy0wLjQwMiwwLjQwMi0wLjg2NywwLjcxNi0xLjM5MSwwLjk0MkM5NS40OTMsNjIuODg4LDk0LjkzLDYzLDk0LjMyNSw2MwoJCQkJYy0wLjYwNCwwLTEuMTctMC4xMTQtMS42OTgtMC4zNDVjLTAuNTI3LTAuMjMxLTAuOTkxLTAuNTQzLTEuMzg5LTAuOTM4Yy0wLjQtMC4zOTUtMC43MTQtMC44NTYtMC45NDQtMS4zODUKCQkJCWMtMC4yMzEtMC41MjctMC4zNDctMS4wOTQtMC4zNDctMS42OThjMC0wLjU4NywwLjExNS0xLjE0NiwwLjM0Ny0xLjY4YzAuMjMtMC41MzIsMC41NDQtMC45OTgsMC45NDQtMS4zOTYKCQkJCWMwLjM5Ny0wLjM5NiwwLjg2MS0wLjcxMywxLjM4OS0wLjk0M0M5My4xNTUsNTQuMzg0LDkzLjcyMiw1NC4yNjksOTQuMzI1LDU0LjI2OXoiLz4KCQkJPHBhdGggZmlsbD0iI0ZGRkZGRiIgZD0iTTEwNS42NDksNTQuMjY5aDcuMjg1djEuNDYxaC0yLjkwOFY2M2gtMS40NnYtNy4yNzFoLTIuOTE3VjU0LjI2OXoiLz4KCQkJPHBhdGggZmlsbD0iI0ZGRkZGRiIgZD0iTTEyMS4xNzQsNTQuMjY5aDEuNDQ3VjYzaC0xLjQ0N1Y1NC4yNjl6Ii8+CgkJCTxwYXRoIGZpbGw9IiNGRkZGRkYiIGQ9Ik0xMzIuNDg1LDU0LjI2OWwyLjc0Miw1LjQ3NGwyLjc0My01LjQ3NGgxLjYyMkwxMzUuMjI4LDYzbC00LjM2Ni04LjczMUgxMzIuNDg1eiIvPgoJCQk8cGF0aCBmaWxsPSIjRkZGRkZGIiBkPSJNMTUzLjY0Niw1NC4yNjl2MS40NjFoLTQuMzY1djIuMTg4aDQuMzY1djEuNDQ3aC00LjM2NXYyLjE3Nmg0LjM2NVY2M2gtNS44MTJ2LTguNzMxSDE1My42NDZ6Ii8+CgkJPC9nPgoJPC9nPgoJPGNpcmNsZSBmaWxsPSIjRkZGRkZGIiBjeD0iMTQ3LjY4MyIgY3k9IjEyLjkwNyIgcj0iMi41MzkiLz4KCTxjaXJjbGUgZmlsbD0iI0ZGRkZGRiIgY3g9IjE1OC4zMjgiIGN5PSIyMS45MDIiIHI9IjEuMjk5Ii8+Cgk8Y2lyY2xlIGZpbGw9IiNGRkZGRkYiIGN4PSIxNTkuMDY0IiBjeT0iMzQuOTU1IiByPSIwLjcyNCIvPgoJPGNpcmNsZSBmaWxsPSIjRkZGRkZGIiBjeD0iMTYzLjAzIiBjeT0iMTkuNDYxIiByPSIwLjcyNCIvPgoJPGNpcmNsZSBmaWxsPSIjRkZGRkZGIiBjeD0iMTU1LjE3OSIgY3k9IjIzLjY3NCIgcj0iMi4xMTkiLz4KCTxjaXJjbGUgZmlsbD0iI0ZGRkZGRiIgY3g9IjE1Mi41NDciIGN5PSIxOS40NjMiIHI9IjIuMTE5Ii8+Cgk8Y2lyY2xlIGZpbGw9IiNGRkZGRkYiIGN4PSIxNTAuMjIzIiBjeT0iMTEuNjYzIiByPSIxLjA0MyIvPgoJPGNpcmNsZSBmaWxsPSIjRkZGRkZGIiBjeD0iMTUyLjYxIiBjeT0iMTAuODI0IiByPSIwLjU4OSIvPgoJPGNpcmNsZSBmaWxsPSIjRkZGRkZGIiBjeD0iMTU3Ljc1MiIgY3k9IjE4LjA4MSIgcj0iMC41ODkiLz4KCTxjaXJjbGUgZmlsbD0iI0ZGRkZGRiIgY3g9IjE1NC4zNTgiIGN5PSIxOC4wODEiIHI9IjAuNTg5Ii8+Cgk8Y2lyY2xlIGZpbGw9IiNGRkZGRkYiIGN4PSIxNTcuMTk5IiBjeT0iMzEuMTM1IiByPSIwLjU4OCIvPgoJPGNpcmNsZSBmaWxsPSIjRkZGRkZGIiBjeD0iMTU4LjkzMyIgY3k9IjI3LjQxMyIgcj0iMS4wNDYiLz4KCTxjaXJjbGUgZmlsbD0iI0ZGRkZGRiIgY3g9IjE1Mi41NDYiIGN5PSIxNi4zNTUiIHI9IjAuMjU2Ii8+Cgk8Y2lyY2xlIGZpbGw9IiNGRkZGRkYiIGN4PSIxNTQuMzU3IiBjeT0iMTYuMSIgcj0iMC4yNTYiLz4KCTxjaXJjbGUgZmlsbD0iI0ZGRkZGRiIgY3g9IjE2My4yODciIGN5PSIxNC4wMDYiIHI9IjAuMjU2Ii8+Cgk8Y2lyY2xlIGZpbGw9IiNGRkZGRkYiIGN4PSIxNTAuMDAzIiBjeT0iMzUuNjc5IiByPSIxLjA0NSIvPgoJPHBhdGggZmlsbD0iI0ZGRkZGRiIgZD0iTTE1Mi4yODksMjkuMzU0Yy0wLjM2MiwwLTAuNjU0LDAuMjkzLTAuNjU0LDAuNjU2YzAsMC4zNjIsMC4yOTIsMC42NTYsMC42NTQsMC42NTYKCQljMC4zNjQsMCwwLjY1Ny0wLjI5NCwwLjY1Ny0wLjY1NkMxNTIuOTQ2LDI5LjY0NywxNTIuNjUzLDI5LjM1NCwxNTIuMjg5LDI5LjM1NHoiLz4KCTxjaXJjbGUgZmlsbD0iI0ZGRkZGRiIgY3g9IjE1NC45NjQiIGN5PSIyOC44MTIiIHI9IjAuNjU2Ii8+Cgk8Y2lyY2xlIGZpbGw9IiNGRkZGRkYiIGN4PSIxNTcuMDI5IiBjeT0iMjUuOTY2IiByPSIwLjE2OSIvPgoJPHBhdGggZmlsbD0iI0ZGRkZGRiIgZD0iTTE1Mi4yODksMjkuMzU0Yy0wLjM2MiwwLTAuNjU0LDAuMjkzLTAuNjU0LDAuNjU2YzAsMC4zNjIsMC4yOTIsMC42NTYsMC42NTQsMC42NTYKCQljMC4zNjQsMCwwLjY1Ny0wLjI5NCwwLjY1Ny0wLjY1NkMxNTIuOTQ2LDI5LjY0NywxNTIuNjUzLDI5LjM1NCwxNTIuMjg5LDI5LjM1NHoiLz4KCTxjaXJjbGUgZmlsbD0iI0ZGRkZGRiIgY3g9IjE1MC4wMDMiIGN5PSIzNS42NzkiIHI9IjEuMDQ1Ii8+Cgk8cGF0aCBmaWxsPSIjRkZGRkZGIiBkPSJNMTUzLjUsMzMuNTc0YzAtMC43NjIsMC42MTUtMS4zNzksMS4zNzQtMS4zODNWMjcuODdjMC0wLjQxLTAuMDE2LTAuODEzLTAuMDQxLTEuMjEzCgkJYy0wLjI3Ny0wLjEwOC0wLjQ3NS0wLjM3Ny0wLjQ3NS0wLjY5MmMwLTAuMjYyLDAuMTM3LTAuNDkzLDAuMzQzLTAuNjI0Yy0wLjM5MS0yLjgzNi0xLjQ1NC01LjM5Mi0zLjE5My03LjY2OAoJCWMtMC4zMDQsMC43MDEtMC45OTksMS4xOTItMS44MTMsMS4xOTJjLTEuMDksMC0xLjk3NS0wLjg4NS0xLjk3NS0xLjk3N2MwLTAuODYsMC41NTUtMS41ODYsMS4zMjMtMS44NTYKCQljLTMuMTU4LTIuODAyLTYuODk1LTQuMjA4LTExLjIxNC00LjIwOGMtNC43MDksMC04LjcyNywxLjY2NS0xMi4wNTQsNC45OTNjLTMuMzI5LDMuMzI4LTQuOTk0LDcuMzQ2LTQuOTk0LDEyLjA1MwoJCWMwLDQuNzA5LDEuNjY1LDguNzI3LDQuOTk0LDEyLjA1NWMzLjMyNywzLjMyNyw3LjM0NSw0Ljk5MSwxMi4wNTQsNC45OTFjNC43MDcsMCw4Ljc2Ni0xLjcwNCwxMi4xNzQtNS4xMTN2Mi42NzkKCQljMCwwLjY2OSwwLjIzOCwxLjI0MiwwLjcxNiwxLjcyYzAuNDc3LDAuNDc3LDEuMDUxLDAuNzE1LDEuNzIsMC43MTVjMC42NywwLDEuMjQzLTAuMjM4LDEuNzIxLTAuNzE1CgkJYzAuNDc2LTAuNDc4LDAuNzE1LTEuMDUxLDAuNzE1LTEuNzJ2LTcuNTI3QzE1NC4xMTUsMzQuOTQ5LDE1My41LDM0LjMzNCwxNTMuNSwzMy41NzR6IE0xMzcuODI5LDQwLjA0NgoJCWMtMy4zNywwLTYuMjQtMS4xODctOC42MTUtMy41NjJjLTIuMzc0LTIuMzc0LTMuNTYxLTUuMjQ2LTMuNTYxLTguNjE0YzAtMy4zNjcsMS4xODctNi4yMzksMy41NjEtOC42MTQKCQljMi4zNzUtMi4zNzUsNS4yNDUtMy41NjEsOC42MTUtMy41NjFjMy4zNjcsMCw2LjIzOSwxLjE4Nyw4LjYxMywzLjU2MWMyLjM3NSwyLjM3NSwzLjU2MSw1LjI0NywzLjU2MSw4LjYxNAoJCWMwLDMuMzY5LTEuMTg2LDYuMjQtMy41NjEsOC42MTRDMTQ0LjA2OCwzOC44NTksMTQxLjE5Niw0MC4wNDYsMTM3LjgyOSw0MC4wNDZ6IE0xNTAuMDAzLDM2LjcyNGMtMC41NzcsMC0xLjA0NS0wLjQ2OS0xLjA0NS0xLjA0NgoJCWMwLTAuNTc4LDAuNDY4LTEuMDQ0LDEuMDQ1LTEuMDQ0czEuMDQ2LDAuNDY2LDEuMDQ2LDEuMDQ0QzE1MS4wNDksMzYuMjU1LDE1MC41OCwzNi43MjQsMTUwLjAwMywzNi43MjR6IE0xNTIuMjg5LDMwLjY2NwoJCWMtMC4zNjIsMC0wLjY1NC0wLjI5NC0wLjY1NC0wLjY1NmMwLTAuMzYzLDAuMjkyLTAuNjU2LDAuNjU0LTAuNjU2YzAuMzY0LDAsMC42NTcsMC4yOTMsMC42NTcsMC42NTYKCQlDMTUyLjk0NiwzMC4zNzIsMTUyLjY1MywzMC42NjcsMTUyLjI4OSwzMC42Njd6Ii8+Cgk8Y2lyY2xlIGZpbGw9IiNGRkZGRkYiIGN4PSIxNTQuODgzIiBjeT0iMzEuNjQ2IiByPSIxLjM4MyIvPgoJPGNpcmNsZSBmaWxsPSIjRkZGRkZGIiBjeD0iMTU1LjUzNSIgY3k9IjM5LjAyNiIgcj0iMS4wNzEiLz4KCTxwb2x5Z29uIGZpbGw9IiNGRkZGRkYiIHBvaW50cz0iMTY3LjE3OCwxMy44MTEgMTY4LjIwNywxNC42ODYgMTY5LjIzNywxNS41NjEgMTY3Ljk2NSwxNi4wMTYgMTY2LjY5MSwxNi40NzIgMTY2LjkzNSwxNS4xNDEgCSIvPgoJPHBvbHlnb24gZmlsbD0iI0ZGRkZGRiIgcG9pbnRzPSIxNTQuNDU4LDMuODI4IDE1NS43MjgsNC45MDcgMTU2Ljk5OSw1Ljk4NiAxNTUuNDMsNi41NDcgMTUzLjg2LDcuMTA4IDE1NC4xNTgsNS40NjggCSIvPgoJPHBvbHlnb24gZmlsbD0iI0ZGRkZGRiIgcG9pbnRzPSIxNjUuODkzLDIzLjIgMTY2LjkyMSwyNC41NTMgMTY3Ljk1MSwyNS45MDMgMTY2Ljk4LDI2LjI0OSAxNjYuMDEyLDI2LjU5OCAxNjUuOTUxLDI0Ljg5NyAJIi8+CgkKCQk8cmVjdCB4PSIxNjIuNDc1IiB5PSI0Ljc4MiIgdHJhbnNmb3JtPSJtYXRyaXgoMC44MzIyIDAuNTU0NSAtMC41NTQ1IDAuODMyMiAzMS4zMDEgLTkwLjAyOTkpIiBmaWxsPSIjRkZGRkZGIiB3aWR0aD0iMy44MzEiIGhlaWdodD0iMy44MzMiLz4KCQoJCTxyZWN0IHg9IjE1NS44MDMiIHk9IjEwLjkzMyIgdHJhbnNmb3JtPSJtYXRyaXgoMC4zNDA2IDAuOTQwMiAtMC45NDAyIDAuMzQwNiAxMTQuOTEwMyAtMTM5LjQzNjQpIiBmaWxsPSIjRkZGRkZGIiB3aWR0aD0iMi4xMTEiIGhlaWdodD0iMi41MzMiLz4KCQoJCTxyZWN0IHg9IjE1OS4xMDYiIHk9IjMuOTYyIiB0cmFuc2Zvcm09Im1hdHJpeCgwLjk4MjMgMC4xODcxIC0wLjE4NzEgMC45ODIzIDMuNjQ3NiAtMjkuNzgzNCkiIGZpbGw9IiNGRkZGRkYiIHdpZHRoPSIwLjkzMSIgaGVpZ2h0PSIwLjkzMSIvPgoJPHBvbHlnb24gZmlsbD0iI0ZGRkZGRiIgcG9pbnRzPSIxNTYuOTM0LDMuMTk1IDE1Ni4yMiwyLjMyIDE1NS41MDYsMS40NDQgMTU2LjYyMiwxLjI2MyAxNTcuNzM2LDEuMDgzIDE1Ny4zMzYsMi4xMzkgCSIvPgoJCgkJPHJlY3QgeD0iMTYxLjY2NyIgeT0iMjkuNDY4IiB0cmFuc2Zvcm09Im1hdHJpeCgwLjgzMiAwLjU1NDggLTAuNTU0OCAwLjgzMiA0NC4wODQyIC04NS4wMTM0KSIgZmlsbD0iI0ZGRkZGRiIgd2lkdGg9IjEuNDg1IiBoZWlnaHQ9IjEuNjI2Ii8+CjwvZz4KPC9zdmc+Cg=="



# ─── Design system ────────────────────────────────────────────────────────────

C = {
    "bg":       "#F4F6FA",
    "surface":  "#FFFFFF",
    "navy":     "#080F1E",
    "navy2":    "#101C35",
    "blue":     "#2B5CE6",
    "blue_lt":  "#EEF3FD",
    "gold":     "#E8A020",
    "gold_lt":  "#FEF7EC",
    "red":      "#D63B3B",
    "red_lt":   "#FEF2F2",
    "amber":    "#D08B00",
    "amber_lt": "#FFFBEB",
    "green":    "#0A8A62",
    "green_lt": "#EDFAF5",
    "slate":    "#4B5675",
    "border":   "#E4E8F0",
    "muted":    "#8892A4",
    "text":     "#1A2236",
}

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Inter', -apple-system, system-ui, sans-serif;
  background: #F4F6FA;
  color: #1A2236;
  font-size: 13px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

.page {
  background: #fff;
  max-width: 1020px;
  margin: 0 auto 40px;
  box-shadow: 0 2px 4px rgba(0,0,0,.04), 0 12px 48px rgba(8,15,30,.10);
  border-radius: 16px;
  overflow: hidden;
}

/* ── Cover ── */
.cover {
  background: linear-gradient(140deg, #080F1E 0%, #0D1E3C 50%, #112040 100%);
  padding: 0;
  color: #fff;
  position: relative;
  overflow: hidden;
}
.cover-accent-bar {
  height: 4px;
  background: linear-gradient(90deg, #2B5CE6 0%, #7B5CF5 50%, #E8A020 100%);
}
.cover-inner { padding: 64px 64px 56px; position: relative; z-index: 2; }
.cover-dots {
  position: absolute; inset: 0; z-index: 1;
  background-image: radial-gradient(circle, rgba(43,92,230,.15) 1px, transparent 1px);
  background-size: 32px 32px;
}
.cover-eyebrow {
  font-size: 10px; font-weight: 700; letter-spacing: 4px;
  text-transform: uppercase; color: #E8A020; margin-bottom: 20px;
  display: flex; align-items: center; gap: 10px;
}
.cover-eyebrow::after { content: ''; flex: 1; max-width: 60px; height: 1px; background: #E8A020; opacity: .5; }
.cover-domain { font-size: 42px; font-weight: 900; letter-spacing: -1.5px; line-height: 1.1; margin-bottom: 8px; }
.cover-tagline { font-size: 15px; color: rgba(255,255,255,.5); margin-bottom: 56px; font-weight: 400; }

.cover-meta-row { display: flex; gap: 40px; flex-wrap: wrap; margin-bottom: 56px; }
.cover-meta-item .meta-label {
  font-size: 9px; font-weight: 700; letter-spacing: 3px;
  text-transform: uppercase; color: rgba(255,255,255,.35); margin-bottom: 4px;
}
.cover-meta-item .meta-value { font-size: 13px; font-weight: 600; color: rgba(255,255,255,.85); }

.cover-bottom { display: flex; align-items: flex-end; gap: 48px; flex-wrap: wrap; }
.cover-gauge-wrap { flex-shrink: 0; }
.cover-gauge-label {
  font-size: 9px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase;
  color: rgba(255,255,255,.4); text-align: center; margin-top: 8px;
}
.cover-chips { display: flex; gap: 16px; flex-wrap: wrap; }
.chip {
  background: rgba(255,255,255,.06);
  border: 1px solid rgba(255,255,255,.10);
  border-radius: 12px; padding: 18px 22px;
}
.chip-val { font-size: 32px; font-weight: 900; line-height: 1; }
.chip-lbl { font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; color: rgba(255,255,255,.45); margin-top: 4px; }
.chip-val.c-red    { color: #F87171; }
.chip-val.c-amber  { color: #FCD34D; }
.chip-val.c-green  { color: #34D399; }
.chip-val.c-gold   { color: #E8A020; }
.chip-val.c-blue   { color: #60A5FA; }

/* ── Section header ── */
.sec-header {
  border-bottom: 1px solid #E4E8F0;
  padding: 22px 48px;
  display: flex; align-items: center; gap: 14px;
  background: #FAFBFD;
}
.sec-num {
  width: 30px; height: 30px; border-radius: 8px;
  background: #080F1E; color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 800; flex-shrink: 0;
}
.sec-title { font-size: 17px; font-weight: 800; letter-spacing: -.3px; }
.sec-sub { font-size: 12px; color: #8892A4; margin-left: auto; }

.sec-body { padding: 36px 48px; }

/* ── Score cards ── */
.score-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-bottom: 32px; }
.score-card {
  border-radius: 12px; padding: 18px 14px; text-align: center;
  border: 1px solid #E4E8F0; position: relative; overflow: hidden;
}
.score-card::after {
  content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 3px;
}
.score-card.c-red::after   { background: #D63B3B; }
.score-card.c-amber::after { background: #D08B00; }
.score-card.c-green::after { background: #0A8A62; }
.sc-page { font-size: 9px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #8892A4; margin-bottom: 6px; }
.sc-num  { font-size: 36px; font-weight: 900; line-height: 1; letter-spacing: -1px; }
.sc-lbl  { font-size: 10px; font-weight: 700; margin-top: 3px; }
.sc-num.c-red   { color: #D63B3B; }
.sc-num.c-amber { color: #D08B00; }
.sc-num.c-green { color: #0A8A62; }
.sc-lbl.c-red   { color: #D63B3B; }
.sc-lbl.c-amber { color: #D08B00; }
.sc-lbl.c-green { color: #0A8A62; }

/* ── KPI row ── */
.kpi-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 14px; margin-bottom: 28px; }
.kpi-box {
  background: #FAFBFD; border: 1px solid #E4E8F0; border-radius: 12px; padding: 18px 16px;
}
.kpi-num  { font-size: 26px; font-weight: 900; letter-spacing: -.5px; color: #1A2236; }
.kpi-lbl  { font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; color: #8892A4; margin-top: 3px; }
.kpi-delta { font-size: 12px; font-weight: 700; margin-top: 5px; }
.kpi-delta.up   { color: #0A8A62; }
.kpi-delta.down { color: #D63B3B; }
.kpi-delta.neut { color: #8892A4; }

/* ── Issue cards ── */
.issue-list { display: flex; flex-direction: column; gap: 10px; }
.issue-card {
  border-radius: 8px; padding: 12px 14px;
  border-left: 3px solid; display: flex; gap: 10px; align-items: flex-start;
}
.issue-card.critical { background: #FEF2F2; border-color: #D63B3B; }
.issue-card.warning  { background: #FFFBEB; border-color: #D08B00; }
.issue-card.success  { background: #EDFAF5; border-color: #0A8A62; }
.i-badge {
  font-size: 9px; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase;
  padding: 2px 7px; border-radius: 4px; white-space: nowrap; flex-shrink: 0; margin-top: 1px;
}
.issue-card.critical .i-badge { background: #D63B3B; color: #fff; }
.issue-card.warning  .i-badge { background: #D08B00; color: #fff; }
.issue-card.success  .i-badge { background: #0A8A62; color: #fff; }
.i-text { font-size: 12px; color: #2D3748; line-height: 1.5; }

/* ── Recommendation cards ── */
.rec-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.rec-card {
  border: 1px solid #E4E8F0; border-radius: 12px; padding: 20px;
  display: flex; flex-direction: column; gap: 10px;
}
.rec-header { display: flex; align-items: flex-start; gap: 10px; }
.rec-dot { width: 9px; height: 9px; border-radius: 50%; flex-shrink: 0; margin-top: 4px; }
.rec-title { font-weight: 800; font-size: 13px; line-height: 1.4; color: #1A2236; }
.rec-tags { display: flex; gap: 6px; flex-wrap: wrap; }
.tag {
  font-size: 9px; font-weight: 700; letter-spacing: 1px;
  text-transform: uppercase; padding: 2px 8px; border-radius: 4px;
  background: #F0F2F7; color: #4B5675;
}
.rec-issue { font-size: 12px; color: #4B5675; line-height: 1.5; }
.rec-fix {
  font-size: 12px; color: #1E40AF; background: #EEF3FD;
  padding: 10px 12px; border-radius: 8px; line-height: 1.5;
}
.rec-fix strong { display: block; font-size: 9px; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; color: #2B5CE6; margin-bottom: 4px; }
.rec-bottom { display: flex; justify-content: space-between; align-items: center; padding-top: 4px; border-top: 1px solid #F0F2F7; }
.rec-impact { font-size: 11px; font-weight: 800; color: #0A8A62; }
.rec-effort { font-size: 11px; color: #8892A4; }
.rec-evidence { font-size: 10px; color: #8892A4; font-style: italic; }

/* ── Screenshot ── */
.shot-wrap { display: flex; gap: 12px; margin-bottom: 14px; }
.shot-frame {
  border: 1.5px solid #E4E8F0; border-radius: 10px; overflow: hidden;
  background: #F4F6FA; position: relative;
}
.shot-frame img { width: 100%; display: block; }
.shot-ph {
  display: flex; align-items: center; justify-content: center;
  background: linear-gradient(135deg, #EEF3FD 0%, #E0E9FB 100%);
}
.shot-label {
  position: absolute; top: 8px; left: 8px;
  background: rgba(8,15,30,.7); color: #fff;
  font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;
  padding: 3px 8px; border-radius: 4px; backdrop-filter: blur(4px);
}
.callout-list { border: 1px solid #E4E8F0; border-radius: 10px; overflow: hidden; }
.callout-row { display: grid; grid-template-columns: 32px 1fr; border-bottom: 1px solid #F0F2F7; }
.callout-row:last-child { border-bottom: none; }
.callout-n {
  background: #080F1E; color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-size: 10px; font-weight: 800;
}
.callout-t { padding: 8px 12px; font-size: 11px; color: #2D3748; line-height: 1.4; }

/* ── Page section ── */
.page-section { padding-top: 32px; margin-top: 32px; border-top: 1px solid #F0F2F7; }
.page-section:first-child { padding-top: 0; margin-top: 0; border-top: none; }
.ps-header { display: flex; align-items: center; gap: 10px; margin-bottom: 20px; }
.ps-badge {
  font-size: 9px; font-weight: 800; letter-spacing: 2px; text-transform: uppercase;
  padding: 4px 12px; border-radius: 6px;
}
.b-home     { background: #DBEAFE; color: #1D4ED8; }
.b-plp      { background: #EDE9FE; color: #6D28D9; }
.b-pdp      { background: #FCE7F3; color: #BE185D; }
.b-cart     { background: #FFEDD5; color: #C2410C; }
.b-checkout { background: #D1FAE5; color: #065F46; }
.ps-url  { font-size: 12px; color: #8892A4; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.ps-score { margin-left: auto; font-size: 24px; font-weight: 900; letter-spacing: -.5px; flex-shrink: 0; }

/* ── Roadmap ── */
.roadmap { display: grid; grid-template-columns: 1fr 1fr 1fr; border: 1px solid #E4E8F0; border-radius: 12px; overflow: hidden; }
.rm-col { padding: 22px; }
.rm-col:not(:last-child) { border-right: 1px solid #E4E8F0; }
.rm-title {
  font-size: 10px; font-weight: 800; text-transform: uppercase; letter-spacing: 2px;
  margin-bottom: 14px; padding-bottom: 10px; border-bottom: 2px solid;
}
.rm-30 { color: #0A8A62; border-color: #0A8A62; }
.rm-60 { color: #D08B00; border-color: #D08B00; }
.rm-90 { color: #2B5CE6; border-color: #2B5CE6; }
.rm-item {
  font-size: 11px; color: #2D3748; padding: 7px 0;
  border-bottom: 1px solid #F4F6FA; display: flex; gap: 6px; align-items: flex-start;
}
.rm-item:last-child { border-bottom: none; }
.rm-item::before { content: '→'; color: #C0C8D8; flex-shrink: 0; margin-top: 1px; }

/* ── AB test plan ── */
.ab-table { width: 100%; border-collapse: collapse; font-size: 12px; }
.ab-table th {
  background: #080F1E; color: rgba(255,255,255,.7);
  font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px;
  padding: 10px 14px; text-align: left;
}
.ab-table th:first-child { border-radius: 8px 0 0 8px; }
.ab-table th:last-child  { border-radius: 0 8px 8px 0; }
.ab-table td { padding: 14px; border-bottom: 1px solid #F0F2F7; vertical-align: top; }
.ab-table tr:last-child td { border-bottom: none; }
.ab-num { font-weight: 900; font-size: 16px; color: #2B5CE6; }
.ab-impact { font-weight: 800; color: #0A8A62; }
.ab-weeks  { font-weight: 700; color: #D08B00; }
.ab-effort-pill {
  font-size: 9px; font-weight: 800; text-transform: uppercase; letter-spacing: 1px;
  padding: 2px 8px; border-radius: 4px;
}
.ab-effort-pill.low    { background: #D1FAE5; color: #065F46; }
.ab-effort-pill.medium { background: #FEF3C7; color: #92400E; }
.ab-effort-pill.high   { background: #FEE2E2; color: #991B1B; }
.ab-card {
  border: 1px solid #E4E8F0; border-radius: 12px; overflow: hidden; margin-bottom: 16px;
}
.ab-card-header {
  background: #080F1E; color: #fff; padding: 14px 20px;
  display: flex; align-items: center; gap: 14px;
}
.ab-card-num { font-size: 22px; font-weight: 900; color: #E8A020; }
.ab-card-title { font-size: 14px; font-weight: 800; }
.ab-card-body { display: grid; grid-template-columns: 1fr 1fr; gap: 0; }
.ab-field { padding: 14px 20px; border-bottom: 1px solid #F0F2F7; border-right: 1px solid #F0F2F7; }
.ab-field:nth-child(even) { border-right: none; }
.ab-field:nth-last-child(-n+2) { border-bottom: none; }
.ab-field-label { font-size: 9px; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; color: #8892A4; margin-bottom: 4px; }
.ab-field-value { font-size: 12px; color: #2D3748; line-height: 1.5; }
.ab-hyp { background: #EEF3FD; border-radius: 8px; padding: 12px 14px; font-size: 12px; color: #1E40AF; font-style: italic; line-height: 1.6; }

/* ── Paid media ── */
.paid-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.paid-section { border: 1px solid #E4E8F0; border-radius: 12px; overflow: hidden; }
.paid-header {
  padding: 14px 20px; display: flex; align-items: center; gap: 10px;
  border-bottom: 1px solid #E4E8F0;
}
.paid-header.meta   { background: #EEF3FD; }
.paid-header.google { background: #EDFAF5; }
.paid-logo { font-size: 16px; font-weight: 900; }
.paid-logo.meta   { color: #1877F2; }
.paid-logo.google { color: #0A8A62; }
.paid-sub { font-size: 11px; color: #8892A4; }
.paid-body { padding: 16px 20px; }
.paid-kpi-mini { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 14px; }
.pkm { background: #FAFBFD; border-radius: 8px; padding: 12px; }
.pkm-val { font-size: 18px; font-weight: 900; color: #1A2236; }
.pkm-lbl { font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; color: #8892A4; margin-top: 2px; }
.pkm-val.gold  { color: #D08B00; }
.pkm-val.green { color: #0A8A62; }
.pkm-val.red   { color: #D63B3B; }
.pkm-val.blue  { color: #2B5CE6; }

/* ── Funnel SVG wrapper ── */
.funnel-wrap { overflow-x: auto; }

/* ── Diagnostic table ── */
.diag-table { width: 100%; border-collapse: collapse; font-size: 12px; margin-top: 20px; }
.diag-table th {
  background: #F4F6FA; padding: 9px 14px; text-align: left;
  font-size: 9px; font-weight: 800; text-transform: uppercase; letter-spacing: 2px;
  color: #4B5675; border-bottom: 2px solid #E4E8F0;
}
.diag-table td { padding: 12px 14px; border-bottom: 1px solid #F4F6FA; vertical-align: top; }
.diag-table tr:last-child td { border-bottom: none; }
.diag-signal  { font-weight: 700; color: #D63B3B; }
.diag-dx      { color: #4B5675; }
.diag-action  { font-weight: 600; color: #2B5CE6; }

/* ── TN section ── */
.tn-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 24px; }
.tn-box { background: #FAFBFD; border: 1px solid #E4E8F0; border-radius: 12px; padding: 18px 16px; }
.tn-num  { font-size: 24px; font-weight: 900; color: #1A2236; letter-spacing: -.5px; }
.tn-lbl  { font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; color: #8892A4; margin-top: 3px; }
.tn-delta { font-size: 11px; font-weight: 700; margin-top: 4px; }
.tn-delta.up   { color: #0A8A62; }
.tn-delta.down { color: #D63B3B; }
.tn-loss {
  background: linear-gradient(135deg, #FEF2F2, #FFEAEA);
  border: 1px solid #FECACA; border-radius: 12px;
  padding: 20px 24px; margin-bottom: 24px;
  display: flex; align-items: center; gap: 20px;
}
.tn-loss-val { font-size: 40px; font-weight: 900; color: #D63B3B; letter-spacing: -1px; }
.tn-loss-label { font-size: 13px; font-weight: 700; color: #D63B3B; }
.tn-loss-sub { font-size: 12px; color: #9B2020; margin-top: 2px; }

/* ── Chart areas ── */
.chart-box {
  background: #FAFBFD; border: 1px solid #E4E8F0;
  border-radius: 12px; padding: 20px;
}
.chart-title {
  font-size: 10px; font-weight: 800; text-transform: uppercase;
  letter-spacing: 2px; color: #4B5675; margin-bottom: 14px;
}
.chart-row { display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 24px; align-items: flex-start; }

/* ── Framework table ── */
.fw-table { width: 100%; border-collapse: collapse; font-size: 12px; }
.fw-table th {
  background: #F4F6FA; padding: 9px 12px; text-align: left;
  font-size: 9px; text-transform: uppercase; letter-spacing: 2px;
  font-weight: 800; color: #4B5675; border-bottom: 2px solid #E4E8F0;
}
.fw-table td { padding: 10px 12px; border-bottom: 1px solid #F4F6FA; }
.fw-table tr:last-child td { border-bottom: none; }
.pill {
  display: inline-block; padding: 2px 10px; border-radius: 20px;
  font-size: 10px; font-weight: 800;
}
.pill.c-red   { background: #FEE2E2; color: #991B1B; }
.pill.c-amber { background: #FEF3C7; color: #92400E; }
.pill.c-green { background: #D1FAE5; color: #065F46; }

/* ── Priority matrix ── */
.matrix-legend { display: flex; gap: 16px; flex-wrap: wrap; margin-top: 12px; }
.ml-item { display: flex; align-items: center; gap: 6px; font-size: 11px; color: #4B5675; }
.ml-dot  { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }

/* ── Critical block ── */
.critical-block {
  background: #FEF2F2; border: 1px solid #FECACA;
  border-radius: 12px; padding: 20px;
}
.crit-row {
  display: flex; gap: 14px; padding: 11px 0;
  border-bottom: 1px solid #FECACA; align-items: flex-start;
}
.crit-row:last-child { border-bottom: none; }
.crit-num {
  width: 26px; height: 26px; background: #D63B3B; color: #fff;
  border-radius: 6px; display: flex; align-items: center; justify-content: center;
  font-size: 11px; font-weight: 900; flex-shrink: 0;
}
.crit-page { font-size: 9px; font-weight: 800; text-transform: uppercase; letter-spacing: 1.5px; color: #D63B3B; margin-bottom: 2px; }
.crit-text { font-size: 12px; color: #1A2236; line-height: 1.4; }

/* ── Footer ── */
.report-footer {
  background: #080F1E; color: rgba(255,255,255,.4);
  padding: 18px 48px; font-size: 11px;
  display: flex; justify-content: space-between; align-items: center;
}
.report-footer strong { color: rgba(255,255,255,.7); }

/* ── Divider ── */
.divider { border: none; border-top: 1px solid #F0F2F7; margin: 28px 0; }

@media print {
  body { background: white; }
  .page { box-shadow: none; margin: 0; border-radius: 0; page-break-after: always; max-width: none; }
  @page { margin: 0; }
}
"""


# ─── Helpers ──────────────────────────────────────────────────────────────────

def score_color_cls(score):
    if score >= 72: return "c-green"
    if score >= 48: return "c-amber"
    return "c-red"

def score_label(score):
    if score >= 85: return "Elite"
    if score >= 72: return "Strong"
    if score >= 55: return "Average"
    if score >= 40: return "Weak"
    return "Critical"

def pill_cls(val, max_val):
    p = (val / max_val) * 100
    if p >= 66: return "c-green"
    if p >= 33: return "c-amber"
    return "c-red"


# ─── Data loaders ─────────────────────────────────────────────────────────────

def load_data(d="."):
    p = Path(d)
    analyses, discovery, ga4, tn, paid, ab_plan, plugins, screenshots = {}, {}, {}, {}, {}, {}, {}, {}

    for f in p.glob("cro_analysis_*.json"):
        analyses[f.stem.replace("cro_analysis_", "")] = json.loads(f.read_text())

    for fname, target in [
        ("cro_discovery.json", discovery),
        ("cro_ga4_data.json",  ga4),
        ("ga4_data.json",      ga4),
        ("cro_tiendanube.json", tn),
        ("cro_paid_media.json", paid),
        ("cro_ab_plan.json",   ab_plan),
        ("cro_plugins.json",   plugins),
    ]:
        fp = p / fname
        if fp.exists():
            target.update(json.loads(fp.read_text()))

    for img in p.glob("screenshot_*.png"):
        key = img.stem.replace("screenshot_", "")
        screenshots[key] = "data:image/png;base64," + base64.b64encode(img.read_bytes()).decode()

    return analyses, discovery, ga4, tn, paid, ab_plan, plugins, screenshots


def calculate_site_score(scores):
    weights = {"checkout": .40, "pdp": .30, "home": .20, "plp": .10}
    wt = ws = 0
    for page, w in weights.items():
        if page in scores:
            ws += scores[page] * w; wt += w
    return round(ws / wt) if wt else 0


# ─── SVG components ───────────────────────────────────────────────────────────

def svg_gauge(score, size=160, dark_bg=False):
    cx = cy = size / 2
    r  = size * 0.36
    sw = size * 0.09
    c  = 2 * math.pi * r
    color_map = {score >= 72: "#0A8A62", score >= 48: "#D08B00", True: "#D63B3B"}
    color = next(v for k, v in color_map.items() if k)
    filled = c * (score / 100)
    fs = size * 0.21
    ls = size * 0.095
    # On dark backgrounds: white text + semi-transparent track
    num_color  = "#FFFFFF"       if dark_bg else "#1A2236"
    lbl_color  = "rgba(255,255,255,.55)" if dark_bg else "#8892A4"
    track_col  = "rgba(255,255,255,.12)" if dark_bg else "#F0F2F7"
    return f"""<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{track_col}" stroke-width="{sw}"/>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="{sw}"
    stroke-dasharray="{filled:.1f} {c:.1f}" stroke-dashoffset="{c/4:.1f}" stroke-linecap="round"/>
  <text x="{cx}" y="{cy + fs*0.38}" text-anchor="middle"
    font-size="{fs}" font-weight="900" fill="{num_color}" font-family="Inter,system-ui">{score}</text>
  <text x="{cx}" y="{cy + fs*0.38 + ls + 5}" text-anchor="middle"
    font-size="{ls}" fill="{lbl_color}" font-family="Inter,system-ui">{score_label(score)}</text>
</svg>"""


def svg_bars(items, title="", max_val=25, height=200):
    bh = 20; gap = 12; lw = 120; bmax = 240; total_h = max(height, len(items)*(bh+gap)+48)
    total_w = lw + bmax + 72
    bars = ""
    for i, (label, val, color) in enumerate(items):
        y = 36 + i*(bh+gap)
        bw = (val/max_val)*bmax if max_val else 0
        bars += f"""
  <text x="{lw-8}" y="{y+bh*.72}" text-anchor="end" font-size="10" fill="#8892A4" font-family="Inter,system-ui">{label}</text>
  <rect x="{lw}" y="{y}" width="{bmax}" height="{bh}" rx="5" fill="#F0F2F7"/>
  <rect x="{lw}" y="{y}" width="{bw:.1f}" height="{bh}" rx="5" fill="{color}"/>
  <text x="{lw+bw+6}" y="{y+bh*.72}" font-size="10" font-weight="800" fill="{color}" font-family="Inter,system-ui">{val}/{max_val}</text>"""
    tl = f'<text x="{total_w/2}" y="16" text-anchor="middle" font-size="10" font-weight="800" fill="#4B5675" font-family="Inter,system-ui" letter-spacing="2">{title.upper()}</text>' if title else ""
    return f'<svg width="{total_w}" height="{total_h}" viewBox="0 0 {total_w} {total_h}">{tl}{bars}</svg>'


def svg_funnel(steps):
    if not steps: return ""
    w = 520; step_h = 64; h = len(steps) * step_h + 20
    max_bar = 400
    out = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
    for i, (label, value, pct) in enumerate(steps):
        bw = max(60, (pct/100)*max_bar)
        x  = (max_bar - bw)/2 + 60
        y  = i * step_h + 8
        bh = 42
        colors = ["#2B5CE6","#0A8A62","#0A8A62","#D08B00","#D63B3B"]
        if i == 0: color = "#2B5CE6"
        elif pct > 70: color = "#0A8A62"
        elif pct > 40: color = "#D08B00"
        else: color = "#D63B3B"
        drop = ""
        if i > 0 and steps[i-1][2] > 0:
            dp = round(100 - (pct/steps[i-1][2])*100)
            drop = f'<text x="{x+bw+10}" y="{y+bh*.65}" font-size="10" font-weight="800" fill="#D63B3B" font-family="Inter,system-ui">▼ {dp}%</text>'
        out += f"""
  <text x="{x-8:.1f}" y="{y+bh*.65}" text-anchor="end" font-size="10" fill="#8892A4" font-family="Inter,system-ui">{value:,}</text>
  <rect x="{x:.1f}" y="{y}" width="{bw:.1f}" height="{bh}" rx="8" fill="{color}" opacity=".9"/>
  <text x="{x+bw/2:.1f}" y="{y+bh*.65}" text-anchor="middle" font-size="11" font-weight="800" fill="white" font-family="Inter,system-ui">{label}</text>
  {drop}"""
    return out + "</svg>"


def svg_matrix(recs):
    """Numbered dots + leyenda separada para evitar solapamiento de labels."""
    w = 640; h = 400; pad = 70
    iw = w - pad*2; ih = h - pad - 44
    mx = pad + iw/2; my = pad + ih/2

    dots = ""
    for i, rec in enumerate(recs[:12], 1):
        impact = rec.get("impact_score", 5)
        effort = rec.get("effort_score", 5)
        p      = rec.get("priority", "medium")
        col    = {"critical": "#D63B3B", "high": "#D08B00", "medium": "#0A8A62"}.get(p, "#8892A4")
        cx = pad + (effort / 10) * iw
        cy = pad + (1 - impact / 10) * ih
        dots += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="14" fill="{col}" opacity=".92"/>'
        dots += f'<text x="{cx:.1f}" y="{cy+5:.1f}" text-anchor="middle" font-size="11" font-weight="900" fill="white" font-family="Inter,system-ui">{i}</text>'

    return f"""<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <!-- quadrants -->
  <rect x="{pad}" y="{pad}" width="{iw/2:.1f}" height="{ih/2:.1f}" rx="8" fill="#EDFAF5"/>
  <rect x="{mx:.1f}" y="{pad}" width="{iw/2:.1f}" height="{ih/2:.1f}" rx="8" fill="#FFFBEB"/>
  <rect x="{pad}" y="{my:.1f}" width="{iw/2:.1f}" height="{ih/2:.1f}" rx="8" fill="#EEF3FD"/>
  <rect x="{mx:.1f}" y="{my:.1f}" width="{iw/2:.1f}" height="{ih/2:.1f}" rx="8" fill="#FEF2F2"/>
  <!-- quadrant labels -->
  <text x="{pad+iw/4:.1f}" y="{pad+20}" text-anchor="middle" font-size="10" font-weight="800" fill="#0A8A62" font-family="Inter,system-ui">⚡ VICTORIAS RÁPIDAS</text>
  <text x="{pad+iw*3/4:.1f}" y="{pad+20}" text-anchor="middle" font-size="10" font-weight="800" fill="#D08B00" font-family="Inter,system-ui">🎯 ESTRATÉGICO</text>
  <text x="{pad+iw/4:.1f}" y="{my+20:.1f}" text-anchor="middle" font-size="10" font-weight="800" fill="#2B5CE6" font-family="Inter,system-ui">📋 BACKLOG</text>
  <text x="{pad+iw*3/4:.1f}" y="{my+20:.1f}" text-anchor="middle" font-size="10" font-weight="800" fill="#D63B3B" font-family="Inter,system-ui">✗ EVITAR</text>
  <!-- axes -->
  <line x1="{mx:.1f}" y1="{pad}" x2="{mx:.1f}" y2="{pad+ih:.1f}" stroke="#D4DAE8" stroke-width="1.5" stroke-dasharray="4,4"/>
  <line x1="{pad}" y1="{my:.1f}" x2="{pad+iw:.1f}" y2="{my:.1f}" stroke="#D4DAE8" stroke-width="1.5" stroke-dasharray="4,4"/>
  <!-- axis labels -->
  <text x="{pad}" y="{h-8}" font-size="10" fill="#8892A4" font-family="Inter,system-ui">Bajo esfuerzo →</text>
  <text x="{pad+iw}" y="{h-8}" text-anchor="end" font-size="10" fill="#8892A4" font-family="Inter,system-ui">← Alto esfuerzo</text>
  <text transform="rotate(-90)" x="{-(pad+ih/2):.1f}" y="16" text-anchor="middle" font-size="10" fill="#8892A4" font-family="Inter,system-ui">← Bajo impacto · Alto impacto →</text>
  <!-- dots -->
  {dots}
</svg>"""


def svg_matrix_legend(recs):
    """Leyenda numerada para acompañar la matriz."""
    if not recs:
        return ""
    items = ""
    for i, rec in enumerate(recs[:12], 1):
        p   = rec.get("priority", "medium")
        col = {"critical": "#D63B3B", "high": "#D08B00", "medium": "#0A8A62"}.get(p, "#8892A4")
        title = rec.get("title", "")[:55]
        page  = rec.get("page", "")
        items += f"""<div style="display:flex;align-items:flex-start;gap:10px;padding:7px 0;border-bottom:1px solid #F4F6FA">
  <div style="width:22px;height:22px;border-radius:50%;background:{col};color:#fff;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:900;flex-shrink:0">{i}</div>
  <div style="flex:1;min-width:0">
    <div style="font-size:11px;font-weight:700;color:#1A2236;line-height:1.3">{title}</div>
    {'<div style="font-size:9px;color:#8892A4;margin-top:1px">'+page+'</div>' if page else ''}
  </div>
</div>"""
    return f'<div style="margin-top:16px">{items}</div>'


# ─── HTML component builders ──────────────────────────────────────────────────

def shot_block(screenshots, key, callouts=None, mobile_key=None):
    mk = mobile_key or f"{key}_mobile"
    dk = f"{key}_desktop"
    d_src = screenshots.get(dk, "")
    m_src = screenshots.get(mk, "")

    def frame(src, label, style="flex:1"):
        if src:
            img = f'<img src="{src}" alt="{label}"/>'
        else:
            img = f'<div class="shot-ph" style="height:260px"><div style="text-align:center;color:#6B8BCC"><div style="font-size:32px;margin-bottom:8px">🖥</div><div style="font-size:10px;font-weight:700;letter-spacing:1px">{label}</div></div></div>'
        return f'<div class="shot-frame" style="{style}"><div class="shot-label">{label}</div>{img}</div>'

    html = f'<div class="shot-wrap">{frame(d_src,"Desktop")}{frame(m_src,"Mobile","width:150px;flex-shrink:0")}</div>'
    if callouts:
        rows = "".join(f'<div class="callout-row"><div class="callout-n">{i+1}</div><div class="callout-t">{c}</div></div>' for i,c in enumerate(callouts))
        html += f'<div class="callout-list">{rows}</div>'
    return html


def issue_card_html(text, level="warning"):
    badges = {"critical": "Crítico", "warning": "Alto", "success": "Fortaleza"}
    return f'<div class="issue-card {level}"><span class="i-badge">{badges.get(level,"Alto")}</span><div class="i-text">{text}</div></div>'


def rec_card_html(rec):
    p = rec.get("priority","medium")
    dot = {"critical":"#D63B3B","high":"#D08B00","medium":"#0A8A62"}.get(p,"#8892A4")
    page_tag = f'<span class="tag">{rec.get("page","")}</span>' if rec.get("page") else ""
    fw_tag   = f'<span class="tag">{rec.get("framework","")}</span>' if rec.get("framework") else ""
    ev = f'<div class="rec-evidence">📊 {rec["ga4_evidence"]}</div>' if rec.get("ga4_evidence") else ""
    return f"""<div class="rec-card">
  <div class="rec-header"><div class="rec-dot" style="background:{dot}"></div><div class="rec-title">{rec.get("title","")}</div></div>
  <div class="rec-tags">{page_tag}{fw_tag}</div>
  <div class="rec-issue">{rec.get("issue","")}</div>
  <div class="rec-fix"><strong>Solución</strong>{rec.get("fix","")}</div>
  {ev}
  <div class="rec-bottom">
    <div class="rec-impact">↑ {rec.get("impact","")}</div>
    <div class="rec-effort">⏱ {rec.get("effort","")}</div>
  </div>
</div>"""


def kpi_box_html(num, label, delta=None, delta_positive=True):
    if delta is not None:
        sign = "↑" if delta_positive else "↓"
        cls  = "up" if delta_positive else "down"
        d_html = f'<div class="kpi-delta {cls}">{sign} {abs(delta):.1f}% vs prev</div>'
    else:
        d_html = ""
    return f'<div class="kpi-box"><div class="kpi-num">{num}</div><div class="kpi-lbl">{label}</div>{d_html}</div>'


def footer(domain, date, label=""):
    sep = f" · {label}" if label else ""
    return (
        f'<div class="report-footer">'
        f'<div><strong>{domain}</strong>{sep}</div>'
        f'<div style="display:flex;gap:18px;align-items:center">'
        f'<img src="{INIMA_LOGO_B64}" alt="INIMA Interactive" style="height:20px;opacity:.75"/>'
        f'<span style="color:rgba(255,255,255,.35)">{date}</span>'
        f'</div></div>'
    )


# ─── Page builders ────────────────────────────────────────────────────────────

def page_cover(domain, platform, date, site_score, analyses, recommendations):
    all_issues = [(pt.upper(), i) for pt, a in analyses.items() for i in a.get("issues", [])]
    critical   = [i for i in all_issues if "🔴" in i[1] or "critical" in i[1].lower()]
    quick_wins = [r for r in recommendations if r.get("effort_score", 10) <= 3]

    chips = [
        (str(len(analyses)),     "Páginas Auditadas", "c-blue"),
        (str(len(all_issues)),   "Problemas",         "c-amber"),
        (str(len(critical)),     "Críticos",          "c-red"),
        (str(len(quick_wins)),   "Victorias Rápidas", "c-green"),
    ]
    chips_html = "".join(
        f'<div class="chip"><div class="chip-val {c}">{v}</div><div class="chip-lbl">{l}</div></div>'
        for v,l,c in chips
    )
    meta = [
        ("Fecha",       date),
        ("Plataforma",  platform),
        ("Frameworks",  "4Ps · AIDA · Cialdini · Nielsen"),
        ("Datos",       "GA4 · Tiendanube · Meta · Google"),
    ]
    meta_html = "".join(
        f'<div class="cover-meta-item"><div class="meta-label">{l}</div><div class="meta-value">{v}</div></div>'
        for l,v in meta
    )
    # Semáforo: color de portada según score
    if site_score >= 72:
        traffic_gradient = "linear-gradient(90deg,#0A8A62 0%,#16A07A 50%,#34D399 100%)"
        eyebrow_color    = "#34D399"
        score_label_txt  = "VERDE — Buen desempeño"
    elif site_score >= 48:
        traffic_gradient = "linear-gradient(90deg,#D08B00 0%,#E8A020 50%,#FCD34D 100%)"
        eyebrow_color    = "#FCD34D"
        score_label_txt  = "AMARILLO — Oportunidades de mejora"
    else:
        traffic_gradient = "linear-gradient(90deg,#D63B3B 0%,#E85555 50%,#FF6B6B 100%)"
        eyebrow_color    = "#FF6B6B"
        score_label_txt  = "ROJO — Requiere acción inmediata"

    return f"""<div class="page">
  <div class="cover">
    <div class="cover-accent-bar" style="background:{traffic_gradient}"></div>
    <div class="cover-dots"></div>
    <div class="cover-inner">
      <div style="display:flex;justify-content:flex-end;margin-bottom:40px">
        <img src="{INIMA_LOGO_B64}" alt="INIMA Interactive" style="height:36px;opacity:.9"/>
      </div>
      <div class="cover-eyebrow" style="color:{eyebrow_color}">Reporte de Auditoría CRO</div>
      <div class="cover-domain">{domain}</div>
      <div class="cover-tagline">Optimización de Conversión Full-Funnel · {date}</div>
      <div class="cover-meta-row">{meta_html}</div>
      <div class="cover-bottom">
        <div class="cover-gauge-wrap">
          {svg_gauge(site_score, 200, dark_bg=True)}
          <div class="cover-gauge-label" style="color:{eyebrow_color};font-size:9px;letter-spacing:2px">{score_label_txt}</div>
        </div>
        <div class="cover-chips">{chips_html}</div>
      </div>
    </div>
  </div>
  {footer(domain, date, "Confidencial · Preparado por INIMA Interactive")}
</div>"""


def page_executive(domain, date, analyses, scores, recommendations, roadmap):
    site_score = calculate_site_score(scores)
    all_issues = [(pt.upper(), i) for pt, a in analyses.items() for i in a.get("issues", [])]
    critical   = [i for i in all_issues if "🔴" in i[1] or "critical" in i[1].lower()]

    # Score cards
    cards = ""
    for page in ["home","plp","pdp","cart","checkout"]:
        if page not in scores: continue
        sc = scores[page]; cls = score_color_cls(sc)
        cards += f"""<div class="score-card {cls}">
  <div class="sc-page">{page}</div>
  <div class="sc-num {cls}">{sc}</div>
  <div class="sc-lbl {cls}">{score_label(sc)}</div>
</div>"""

    # Critical block
    crit_rows = ""
    for i, (page, issue) in enumerate(critical[:6], 1):
        crit_rows += f"""<div class="crit-row">
  <div class="crit-num">{i}</div>
  <div><div class="crit-page">{page}</div><div class="crit-text">{issue.replace("🔴","").strip()}</div></div>
</div>"""

    # Roadmap
    rm = ""
    if roadmap:
        cols = [
            ("30 Días — Victorias Rápidas", "rm-30", roadmap.get("30_days",[])),
            ("60 Días — Estratégico",       "rm-60", roadmap.get("60_days",[])),
            ("90 Días — Crecimiento",       "rm-90", roadmap.get("90_days",[])),
        ]
        col_html = ""
        for title, cls, items in cols:
            rows = "".join(f'<div class="rm-item">{it}</div>' for it in items[:6])
            col_html += f'<div class="rm-col"><div class="rm-title {cls}">{title}</div>{rows}</div>'
        rm = f'<div style="margin-top:28px"><div style="font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:2px;color:#4B5675;margin-bottom:14px">Roadmap Recomendado</div><div class="roadmap">{col_html}</div></div>'

    return f"""<div class="page">
  <div class="sec-header"><div class="sec-num">1</div><div class="sec-title">Resumen Ejecutivo</div><div class="sec-sub">Últimos 30 días · {len(analyses)} páginas auditadas</div></div>
  <div class="sec-body">
    <div class="score-grid">{cards}</div>
    <div class="chart-row">
      <div class="chart-box" style="flex-shrink:0">
        <div class="chart-title">Score del Sitio</div>
        {svg_gauge(site_score, 150)}
        <div style="font-size:10px;color:#8892A4;margin-top:8px;text-align:center">Checkout 40% · PDP 30% · Inicio 20% · PLP 10%</div>
      </div>
      <div style="flex:1;min-width:260px">
        <div style="font-size:13px;font-weight:800;color:#D63B3B;margin-bottom:12px">{len(critical)} Problemas Críticos que Afectan Conversiones</div>
        <div class="critical-block">{crit_rows or "<div style='color:#8892A4;font-size:12px'>No critical issues identified</div>"}</div>
      </div>
    </div>
    {rm}
  </div>
  {footer(domain, date, "Resumen Ejecutivo")}
</div>"""


def page_pages(domain, date, analyses, scores, screenshots):
    badges = {"home":"b-home","plp":"b-plp","pdp":"b-pdp","cart":"b-cart","checkout":"b-checkout"}
    labels = {"home":"HOME","plp":"CATEGORY / PLP","pdp":"PRODUCT / PDP","cart":"CART","checkout":"CHECKOUT"}

    body = ""
    for pt in ["home","plp","pdp","cart","checkout"]:
        if pt not in analyses: continue
        a  = analyses[pt]; sc = scores.get(pt, 0); cls = score_color_cls(sc)
        issues_h   = "".join(issue_card_html(i, "critical" if "🔴" in i else "warning") for i in a.get("issues",[])[:5])
        strengths_h = "".join(issue_card_html(s, "success") for s in a.get("strengths",[])[:3])
        aida = a.get("aida", {})
        aida_items = [
            ("Attention", aida.get("attention",0), "#2B5CE6"),
            ("Interest",  aida.get("interest",0),  "#7B5CF5"),
            ("Desire",    aida.get("desire",0),     "#D08B00"),
            ("Action",    aida.get("action",0),     "#0A8A62"),
        ]
        score_color_map = {'c-green':'#0A8A62','c-amber':'#D08B00','c-red':'#D63B3B'}
        sc_hex = score_color_map.get(cls, '#8892A4')
        body += f"""<div class="page-section">
  <div class="ps-header">
    <span class="ps-badge {badges.get(pt,'b-home')}">{labels.get(pt,pt.upper())}</span>
    <span class="ps-url">{a.get("url","")}</span>
    <span class="ps-score" style="color:{sc_hex}">{sc}/100</span>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:18px">
    <div>{shot_block(screenshots, pt, a.get("callouts",[]))}</div>
    <div>
      <div class="chart-title">Análisis AIDA</div>
      {svg_bars(aida_items, max_val=25)}
    </div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
    <div>
      <div style="font-size:9px;font-weight:800;text-transform:uppercase;letter-spacing:2px;color:#D63B3B;margin-bottom:10px">Problemas Encontrados</div>
      <div class="issue-list">{issues_h or "<div style='color:#8892A4;font-size:12px'>No critical issues found</div>"}</div>
    </div>
    <div>
      <div style="font-size:9px;font-weight:800;text-transform:uppercase;letter-spacing:2px;color:#0A8A62;margin-bottom:10px">Fortalezas</div>
      <div class="issue-list">{strengths_h or "<div style='color:#8892A4;font-size:12px'>No strengths noted</div>"}</div>
    </div>
  </div>
</div>"""

    return f"""<div class="page">
  <div class="sec-header"><div class="sec-num">2</div><div class="sec-title">Análisis por Página</div></div>
  <div class="sec-body">{body}</div>
  {footer(domain, date, "Análisis por Página")}
</div>"""


def page_frameworks(domain, date, analyses):
    cialdini, nielsen = {}, {}
    for a in analyses.values():
        for k,v in a.get("cialdini",{}).items(): cialdini[k] = max(cialdini.get(k,0),v)
        for k,v in a.get("nielsen",{}).items():  nielsen[k]  = max(nielsen.get(k,0),v)

    c_items = [
        ("Reciprocity",  cialdini.get("reciprocity",0),  "#2B5CE6"),
        ("Commitment",   cialdini.get("commitment",0),   "#7B5CF5"),
        ("Social Proof", cialdini.get("social_proof",0), "#0A8A62"),
        ("Authority",    cialdini.get("authority",0),    "#D08B00"),
        ("Liking",       cialdini.get("liking",0),       "#E8A020"),
        ("Scarcity",     cialdini.get("scarcity",0),     "#D63B3B"),
        ("Urgency",      cialdini.get("urgency",0),      "#9333EA"),
    ]

    n_principles = [
        ("Visibility of system status","h1"),("Real-world match","h2"),
        ("User control & freedom","h3"),("Consistency & standards","h4"),
        ("Error prevention","h5"),("Recognition over recall","h6"),
        ("Flexibility & efficiency","h7"),("Minimalist design","h8"),
        ("Error recovery","h9"),("Help & documentation","h10"),
    ]
    n_rows = ""
    for label, key in n_principles:
        val = nielsen.get(key, 0)
        cls = pill_cls(val, 3)
        n_rows += f'<tr><td>{label}</td><td><span class="pill {cls}">{val}/3</span></td><td style="color:#8892A4;font-size:11px"></td></tr>'

    return f"""<div class="page">
  <div class="sec-header"><div class="sec-num">3</div><div class="sec-title">Auditoría de Persuasión y UX</div></div>
  <div class="sec-body">
    <div class="chart-row">
      <div class="chart-box" style="flex:1">
        <div class="chart-title">Cialdini — 7 Principios de Persuasión</div>
        {svg_bars(c_items, max_val=3)}
      </div>
    </div>
    <div style="margin-top:24px">
      <div class="chart-title" style="margin-bottom:14px">Nielsen — 10 Heurísticas de UX</div>
      <table class="fw-table">
        <thead><tr><th>Heurística</th><th>Score</th><th>Notas</th></tr></thead>
        <tbody>{n_rows}</tbody>
      </table>
    </div>
  </div>
  {footer(domain, date, "Auditoría de Frameworks")}
</div>"""


def page_data_dashboard(domain, date, ga4, tn):
    if not ga4 and not tn:
        return ""

    sections = ""

    # GA4
    if ga4:
        kpis = ga4.get("kpis", {})
        kpi_boxes = ""
        kpi_map = [
            ("sessions",    "Sessions",          "num"),
            ("transactions","Transactions",       "num"),
            ("cvr",         "Conv. Rate",         "pct"),
            ("bounce_rate", "Bounce Rate",        "pct_inv"),
            ("atc_rate",    "ATC Rate",           "pct"),
        ]
        for key, label, fmt in kpi_map:
            if key not in kpis: continue
            d = kpis[key]
            val = d.get("current", 0)
            delta = d.get("delta_pct", None)
            if fmt == "pct":     fval = f"{val:.1f}%"
            elif fmt == "pct_inv": fval = f"{val:.1f}%"
            else:                 fval = f"{val:,}"
            pos = delta > 0 if delta is not None else True
            if fmt == "pct_inv": pos = not pos  # lower bounce = better
            kpi_boxes += kpi_box_html(fval, label, delta, pos)

        funnel = ga4.get("funnel", {})
        funnel_steps = []
        if funnel:
            step_map = [
                ("session_start","Sessions"),("view_item","View Item"),
                ("add_to_cart","Add to Cart"),("begin_checkout","Checkout"),("purchase","Purchase"),
            ]
            top = None
            for key, label in step_map:
                if key in funnel:
                    val = funnel[key]; pct = (val/top*100) if top else 100
                    if top is None: top = val
                    funnel_steps.append((label, val, pct))

        device = ga4.get("cvr_by_device", {})
        device_rows = ""
        benchmarks = {"mobile": "1.2–2.0%", "desktop": "2.5–4.5%", "tablet": "1.5–2.5%"}
        for dev, cvr in device.items():
            diff = cvr - device.get("desktop", cvr)
            cls = "c-red" if diff < -1.5 else ("c-amber" if diff < -.5 else "c-green")
            device_rows += f'<tr><td style="font-weight:600;text-transform:capitalize">{dev}</td><td><span class="pill {cls}">{cvr:.1f}%</span></td><td style="color:#8892A4">{benchmarks.get(dev,"—")}</td></tr>'

        sections += f"""<div style="margin-bottom:32px">
  <div style="font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:2px;color:#2B5CE6;margin-bottom:16px;display:flex;align-items:center;gap:8px"><span style="font-size:16px">📊</span> Google Analytics 4</div>
  <div class="kpi-row">{kpi_boxes}</div>
  <div class="chart-row">
    {'<div class="chart-box"><div class="chart-title">Embudo de Conversión</div><div class="funnel-wrap">' + svg_funnel(funnel_steps) + '</div></div>' if funnel_steps else ''}
    {'<div class="chart-box" style="flex:1"><div class="chart-title">CVR por Dispositivo vs. Benchmark</div><table class="fw-table"><thead><tr><th>Dispositivo</th><th>CVR</th><th>Benchmark</th></tr></thead><tbody>' + device_rows + '</tbody></table></div>' if device_rows else ''}
  </div>
</div>"""

    # Tiendanube
    if tn:
        kpis = tn.get("kpis", {})
        tn_boxes = ""
        tn_map = [
            ("sessions",        "Pedidos Vendidos", None),
            ("transactions",    "Facturación",      None),
            ("cvr",             "Ticket Promedio",  None),
            ("bounce_rate",     "Tasa Abandono",    None),
        ]
        orders = tn.get("orders_sold", 0)
        revenue = tn.get("revenue_total", 0)
        ticket  = tn.get("avg_ticket", 0)
        abandonment_rate = tn.get("abandonment_rate", 0)
        abandonment_value = tn.get("abandonment_value", 0)

        for val, label, delta in [
            (f"{orders:,}", "Pedidos / 30d", tn.get("orders_delta")),
            (f"${revenue:,.0f}", "Facturación", tn.get("revenue_delta")),
            (f"${ticket:,.0f}", "Ticket Promedio", tn.get("ticket_delta")),
            (f"{abandonment_rate:.1f}%", "Tasa Abandono", None),
        ]:
            if val and val != "$0" and val != "0":
                pos = (delta or 0) > 0
                tn_boxes += kpi_box_html(val, label, delta, pos)

        loss_html = ""
        if abandonment_value:
            loss_html = f"""<div class="tn-loss">
  <div><div class="tn-loss-val">${abandonment_value:,.0f}</div></div>
  <div><div class="tn-loss-label">Revenue perdido en carritos abandonados / mes</div>
  <div class="tn-loss-sub">Tasa de abandono: {abandonment_rate:.1f}% · Recuperar el 20% = ${abandonment_value*.2:,.0f} extra/mes sin nuevo tráfico</div></div>
</div>"""

        top_products = tn.get("top_products", [])
        prod_rows = ""
        for p in top_products[:5]:
            prod_rows += f'<tr><td style="font-weight:600">{p.get("name","")}</td><td style="text-align:right">{p.get("quantity",0)}</td><td style="text-align:right;font-weight:700;color:#0A8A62">${p.get("revenue",0):,.0f}</td></tr>'

        sections += f"""<hr class="divider"/>
<div>
  <div style="font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:2px;color:#E8A020;margin-bottom:16px;display:flex;align-items:center;gap:8px"><span style="font-size:16px">🛍</span> Tiendanube — Datos de Ventas</div>
  {loss_html}
  <div class="kpi-row">{tn_boxes}</div>
  {'<div class="chart-box" style="margin-top:8px"><div class="chart-title">Top Productos por Revenue</div><table class="fw-table"><thead><tr><th>Producto</th><th style="text-align:right">Unidades</th><th style="text-align:right">Revenue</th></tr></thead><tbody>' + prod_rows + '</tbody></table></div>' if prod_rows else ''}
</div>"""

    return f"""<div class="page">
  <div class="sec-header"><div class="sec-num">4</div><div class="sec-title">Dashboard de Datos</div><div class="sec-sub">GA4 + Tiendanube · Últimos 30 días</div></div>
  <div class="sec-body">{sections}</div>
  {footer(domain, date, "Dashboard de Datos")}
</div>"""


def page_paid_media(domain, date, paid):
    if not paid:
        return ""

    meta   = paid.get("meta", {})
    google = paid.get("google", {})

    def pkm(val, label, color=""):
        return f'<div class="pkm"><div class="pkm-val {color}">{val}</div><div class="pkm-lbl">{label}</div></div>'

    meta_html = ""
    if meta:
        meta_html = f"""<div class="paid-section">
  <div class="paid-header meta">
    <div class="paid-logo meta">Meta Ads</div>
    <div class="paid-sub">Facebook + Instagram · Last 30d</div>
  </div>
  <div class="paid-body">
    <div class="paid-kpi-mini">
      {pkm(f"${meta.get('spend',0):,.0f}", "Inversión", "")}
      {pkm(f"{meta.get('roas',0):.1f}x", "ROAS", "gold" if meta.get('roas',0) >= 2 else "red")}
      {pkm(f"${meta.get('cpa',0):,.0f}", "CPA", "")}
      {pkm(f"{meta.get('cvr',0):.1f}%", "CVR Post-Click", "green" if meta.get('cvr',0) >= 1.5 else "red")}
    </div>
  </div>
</div>"""

    google_html = ""
    if google:
        lp_score = google.get("landing_page_quality", 0)
        lp_color = "green" if lp_score >= 7 else ("blue" if lp_score >= 5 else "red")
        google_html = f"""<div class="paid-section">
  <div class="paid-header google">
    <div class="paid-logo google">Google Ads</div>
    <div class="paid-sub">Search + Shopping · Last 30d</div>
  </div>
  <div class="paid-body">
    <div class="paid-kpi-mini">
      {pkm(f"${google.get('spend',0):,.0f}", "Inversión", "")}
      {pkm(f"{google.get('roas',0):.1f}x", "ROAS", "gold" if google.get('roas',0) >= 3 else "red")}
      {pkm(f"${google.get('cpa',0):,.0f}", "CPA", "")}
      {pkm(f"{lp_score}/10", "Landing Quality", lp_color)}
    </div>
  </div>
</div>"""

    diag = paid.get("diagnosis", [])
    diag_rows = ""
    for d in diag:
        diag_rows += f'<tr><td class="diag-signal">{d.get("signal","")}</td><td class="diag-dx">{d.get("diagnosis","")}</td><td class="diag-action">{d.get("action","")}</td></tr>'

    diag_html = ""
    if diag_rows:
        diag_html = f"""<div style="margin-top:24px">
  <div class="chart-title">Diagnóstico: Ad vs. Landing Page</div>
  <table class="diag-table">
    <thead><tr><th>Señal detectada</th><th>Diagnóstico</th><th>Acción recomendada</th></tr></thead>
    <tbody>{diag_rows}</tbody>
  </table>
</div>"""

    return f"""<div class="page">
  <div class="sec-header"><div class="sec-num">5</div><div class="sec-title">Performance de Medios Pagados</div><div class="sec-sub">Meta Ads + Google Ads</div></div>
  <div class="sec-body">
    <div class="paid-grid">{meta_html}{google_html}</div>
    {diag_html}
  </div>
  {footer(domain, date, "Medios Pagados")}
</div>"""


def page_recommendations(domain, date, recommendations):
    matrix  = svg_matrix(recommendations)
    legend  = svg_matrix_legend(recommendations)
    cards   = "".join(rec_card_html(r) for r in recommendations[:12])
    return f"""<div class="page">
  <div class="sec-header"><div class="sec-num">6</div><div class="sec-title">Matriz de Prioridad y Recomendaciones</div></div>
  <div class="sec-body">
    <div style="margin-bottom:24px">
      <div class="chart-box">
        <div class="chart-title">Matriz Impacto × Esfuerzo</div>
        {matrix}
        <div style="display:flex;gap:20px;margin-top:12px;flex-wrap:wrap">
          <div class="ml-item"><div class="ml-dot" style="background:#0A8A62"></div><span style="font-size:11px;color:#4B5675">Victoria Rápida</span></div>
          <div class="ml-item"><div class="ml-dot" style="background:#D08B00"></div><span style="font-size:11px;color:#4B5675">Estratégico</span></div>
          <div class="ml-item"><div class="ml-dot" style="background:#D63B3B"></div><span style="font-size:11px;color:#4B5675">Crítico</span></div>
        </div>
      </div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-bottom:28px;align-items:start">
      <div>
        <div style="font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:2px;color:#4B5675;margin-bottom:8px">Referencias de la Matriz</div>
        {legend}
      </div>
      <div style="font-size:12px;color:#4B5675;line-height:1.9">
        <div style="margin-bottom:10px"><strong style="color:#0A8A62">⚡ Victorias Rápidas</strong><br>Alto impacto, bajo esfuerzo. Implementar esta semana.</div>
        <div style="margin-bottom:10px"><strong style="color:#D08B00">🎯 Estratégico</strong><br>Priorizar para el próximo sprint. Test A/B recomendado.</div>
        <div style="margin-bottom:10px"><strong style="color:#2B5CE6">📋 Backlog</strong><br>Agregar al roadmap después de las victorias rápidas.</div>
        <div><strong style="color:#D63B3B">✗ Evitar</strong><br>Alto esfuerzo, bajo retorno. No vale la pena ahora.</div>
      </div>
    </div>
    <div class="rec-grid">{cards}</div>
  </div>
  {footer(domain, date, "Recomendaciones")}
</div>"""


def page_ab_plan(domain, date, ab_plan):
    tests = ab_plan.get("tests", [])
    if not tests:
        return ""

    # Summary table
    summary_rows = ""
    for t in tests:
        effort_lvl = "low" if t.get("effort_hours",0) <= 4 else ("medium" if t.get("effort_hours",0) <= 16 else "high")
        summary_rows += f"""<tr>
  <td><div class="ab-num">#{t.get("id","")}</div></td>
  <td style="font-weight:700">{t.get("name","")}</td>
  <td style="color:#4B5675">{t.get("page","")}</td>
  <td style="font-weight:600;color:#4B5675">{t.get("primary_metric","")}</td>
  <td class="ab-weeks">{t.get("weeks",2)}sem</td>
  <td><span class="ab-effort-pill {effort_lvl}">{t.get("effort_hours","?")}</span></td>
  <td class="ab-impact">{t.get("expected_impact","")}</td>
</tr>"""

    # Detail cards
    detail_cards = ""
    for t in tests:
        fields = [
            ("Página",            t.get("page","")),
            ("Métrica primaria",  t.get("primary_metric","")),
            ("Control (A)",       t.get("control","")),
            ("Variante (B)",      t.get("variant","")),
            ("Muestra necesaria", t.get("sample_size","")),
            ("Duración mínima",   f"{t.get('weeks',2)} semanas"),
            ("Segmento",          t.get("segment","Todos")),
            ("Herramienta",       t.get("tool","")),
        ]
        fields_html = "".join(
            f'<div class="ab-field"><div class="ab-field-label">{l}</div><div class="ab-field-value">{v}</div></div>'
            for l,v in fields if v
        )
        hyp = f'<div style="padding:14px 20px;border-top:1px solid #F0F2F7"><div class="ab-hyp">{t.get("hypothesis","")}</div></div>' if t.get("hypothesis") else ""
        evidence = f'<div style="padding:8px 20px 14px;font-size:10px;color:#8892A4;font-style:italic">📊 {t["evidence"]}</div>' if t.get("evidence") else ""
        detail_cards += f"""<div class="ab-card">
  <div class="ab-card-header">
    <div class="ab-card-num">#{t.get("id","")}</div>
    <div>
      <div class="ab-card-title">{t.get("name","")}</div>
      <div style="font-size:11px;color:rgba(255,255,255,.5);margin-top:2px">{t.get("expected_impact","")}</div>
    </div>
  </div>
  {hyp}
  <div class="ab-card-body">{fields_html}</div>
  {evidence}
</div>"""

    return f"""<div class="page">
  <div class="sec-header"><div class="sec-num">7</div><div class="sec-title">Plan de Tests A/B</div><div class="sec-sub">{len(tests)} tests priorizados por Impacto × Esfuerzo</div></div>
  <div class="sec-body">
    <div style="margin-bottom:28px;overflow-x:auto">
      <table class="ab-table">
        <thead><tr><th>#</th><th>Test</th><th>Página</th><th>Métrica</th><th>Duración</th><th>Esfuerzo (h)</th><th>Impacto esperado</th></tr></thead>
        <tbody>{summary_rows}</tbody>
      </table>
    </div>
    <hr class="divider"/>
    <div style="font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:2px;color:#4B5675;margin-bottom:16px">Especificaciones de Tests</div>
    {detail_cards}
    <div style="margin-top:20px;background:#F4F6FA;border-radius:10px;padding:16px 20px">
      <div style="font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:2px;color:#4B5675;margin-bottom:10px">Reglas de Testing — No Negociables</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:11px;color:#4B5675">
        <div>→ Una variable por test</div><div>→ Mínimo 2 semanas completas</div>
        <div>→ Significancia estadística del 95%</div><div>→ No revisar resultados antes de tiempo</div>
        <div>→ Documentar todos los resultados</div><div>→ Testear mobile por separado si gap CVR &gt;15pp</div>
      </div>
    </div>
  </div>
  {footer(domain, date, "Plan de Tests A/B")}
</div>"""


def page_plugins(domain, date, plugins):
    items = plugins.get("plugins", [])
    if not items:
        return ""

    impact_colors = {
        "crítico": ("#FEF2F2", "#D63B3B", "#D63B3B"),
        "alto":    ("#FFFBEB", "#D08B00", "#D08B00"),
        "medio-alto": ("#EEF3FD", "#2B5CE6", "#2B5CE6"),
        "medio":   ("#EDFAF5", "#0A8A62", "#0A8A62"),
    }

    cards = ""
    for pl in items:
        bg, border, text = impact_colors.get(pl.get("impact","medio"), ("#F4F6FA","#8892A4","#8892A4"))
        price_color = "#0A8A62" if "GRATIS" in pl.get("price","") else "#D08B00"
        cards += f"""<div style="border:1px solid #E4E8F0;border-radius:12px;overflow:hidden;display:flex;flex-direction:column">
  <div style="background:{bg};border-bottom:1px solid {border}22;padding:14px 18px;display:flex;align-items:center;gap:12px">
    <div style="width:28px;height:28px;border-radius:8px;background:{border};color:#fff;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:900;flex-shrink:0">{pl['rank']}</div>
    <div style="flex:1">
      <div style="font-size:13px;font-weight:800;color:#1A2236">{pl['name']}</div>
      <div style="font-size:10px;color:#8892A4;margin-top:1px">{pl['category']} · {pl['provider']}</div>
    </div>
    <div style="text-align:right;flex-shrink:0">
      <div style="font-size:12px;font-weight:800;color:{price_color}">{pl['price']}</div>
      <div style="font-size:10px;color:{text};font-weight:700;margin-top:1px">{pl['cvr_uplift']} CVR</div>
    </div>
  </div>
  <div style="padding:14px 18px;flex:1">
    <div style="font-size:11px;color:#4B5675;line-height:1.6;margin-bottom:10px">{pl['description']}</div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center">
      <span style="font-size:9px;font-weight:800;text-transform:uppercase;letter-spacing:1.5px;background:#F0F2F7;color:#4B5675;padding:3px 8px;border-radius:4px">📍 {pl['where']}</span>
      <span style="font-size:9px;font-weight:800;text-transform:uppercase;letter-spacing:1.5px;background:#F0F2F7;color:#4B5675;padding:3px 8px;border-radius:4px">⏱ {pl['setup_hours']}h setup</span>
    </div>
  </div>
</div>"""

    return f"""<div class="page">
  <div class="sec-header"><div class="sec-num">8</div><div class="sec-title">Plugins y Herramientas Recomendadas</div><div class="sec-sub">Tiendanube · Ordenadas por impacto en CVR</div></div>
  <div class="sec-body">
    <div style="background:linear-gradient(135deg,#080F1E,#0D1E3C);border-radius:12px;padding:20px 24px;margin-bottom:24px;display:flex;align-items:center;gap:20px">
      <div style="font-size:36px">🛠</div>
      <div>
        <div style="font-size:14px;font-weight:800;color:#fff;margin-bottom:4px">Stack de herramientas para llevar dreambig-store.com.ar al siguiente nivel</div>
        <div style="font-size:12px;color:rgba(255,255,255,.55)">La mayoría son gratuitas o de bajo costo. Impacto en CVR compuesto si se instalan juntas: estimado +40–60% en conversión total.</div>
      </div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
      {cards}
    </div>
    <div style="margin-top:20px;background:#F4F6FA;border-radius:10px;padding:16px 20px">
      <div style="font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:2px;color:#4B5675;margin-bottom:10px">Orden de instalación recomendado</div>
      <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px;text-align:center">
        <div style="background:#FEF2F2;border-radius:8px;padding:10px;font-size:10px;font-weight:700;color:#D63B3B">1° Opiniones<br><span style="font-weight:400;color:#8892A4">Social proof</span></div>
        <div style="background:#FEF2F2;border-radius:8px;padding:10px;font-size:10px;font-weight:700;color:#D63B3B">2° WhatsApp<br><span style="font-weight:400;color:#8892A4">Consultas</span></div>
        <div style="background:#FEF2F2;border-radius:8px;padding:10px;font-size:10px;font-weight:700;color:#D63B3B">3° Email Recovery<br><span style="font-weight:400;color:#8892A4">$1.8M ARS/mes</span></div>
        <div style="background:#FFFBEB;border-radius:8px;padding:10px;font-size:10px;font-weight:700;color:#D08B00">4° Guía talles<br><span style="font-weight:400;color:#8892A4">Reduce abandono</span></div>
        <div style="background:#FFFBEB;border-radius:8px;padding:10px;font-size:10px;font-weight:700;color:#D08B00">5° Chat live<br><span style="font-weight:400;color:#8892A4">Conversión real-time</span></div>
      </div>
    </div>
  </div>
  {footer(domain, date, "Plugins y Herramientas")}
</div>"""


# ─── Main assembler ───────────────────────────────────────────────────────────

def build_report(analyses, discovery, ga4, tn, paid, ab_plan, plugins, screenshots, scores, recs, roadmap):
    domain   = discovery.get("domain", "E-commerce Audit")
    platform = ", ".join(discovery.get("platform", ["Tiendanube"]))
    date     = datetime.now().strftime("%B %d, %Y")
    site_score = calculate_site_score(scores)

    pages = [
        page_cover(domain, platform, date, site_score, analyses, recs),
        page_executive(domain, date, analyses, scores, recs, roadmap),
        page_pages(domain, date, analyses, scores, screenshots),
        page_frameworks(domain, date, analyses),
        page_data_dashboard(domain, date, ga4, tn),
        page_paid_media(domain, date, paid),
        page_recommendations(domain, date, recs),
        page_ab_plan(domain, date, ab_plan),
        page_plugins(domain, date, plugins),
    ]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>CRO Audit — {domain}</title>
  <style>{CSS}</style>
</head>
<body>
  {"".join(p for p in pages if p)}
</body>
</html>"""


# ─── Entry point ──────────────────────────────────────────────────────────────

def main():
    analysis_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    output_file  = "cro_report.html"
    generate_pdf = False

    for i, arg in enumerate(sys.argv):
        if arg == "--output" and i+1 < len(sys.argv): output_file = sys.argv[i+1]
        if arg == "--pdf": generate_pdf = True

    analyses, discovery, ga4, tn, paid, ab_plan, plugins, screenshots = load_data(analysis_dir)

    if not analyses:
        print("⚠️  No analysis JSON files found. Run html_analyzer.py first.")
        sys.exit(1)

    scores = {page: a.get("score", 60) for page, a in analyses.items()}
    recs   = []
    for pt, a in analyses.items():
        for r in a.get("recommendations", []):
            r.setdefault("page", pt.upper())
            recs.append(r)

    roadmap = {
        "30_days": [r.get("title","") for r in recs if r.get("effort_score",10) <= 3][:6],
        "60_days": [r.get("title","") for r in recs if 3 < r.get("effort_score",10) <= 6][:6],
        "90_days": [r.get("title","") for r in recs if r.get("effort_score",10) > 6][:6],
    }

    html = build_report(analyses, discovery, ga4, tn, paid, ab_plan, plugins, screenshots, scores, recs, roadmap)

    if not output_file.endswith(".html"): output_file = output_file.replace(".md", ".html")
    Path(output_file).write_text(html, encoding="utf-8")
    print(f"✅ HTML report: {output_file}")

    if generate_pdf:
        pdf_file = output_file.replace(".html", ".pdf")
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch()
                pg = browser.new_page()
                pg.goto(f"file://{Path(output_file).resolve()}")
                pg.wait_for_timeout(2000)
                pg.pdf(path=pdf_file, format="A4", print_background=True,
                       margin={"top":"0","right":"0","bottom":"0","left":"0"})
                browser.close()
            print(f"✅ PDF: {pdf_file}")
        except ImportError:
            print("ℹ️  pip install playwright && playwright install chromium")


if __name__ == "__main__":
    main()
