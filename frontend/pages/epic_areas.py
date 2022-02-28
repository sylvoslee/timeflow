import asyncio
from cProfile import label
import json
from idom import html, run, use_state, component, event, vdom
import requests
from sanic import Sanic, response
from black import click
from datetime import datetime

from components.input import Input, SelectorDropdownKeyValue, Selector
from components.layout import Row, Column, Container
from components.lists import ListSimple
from components.table import SimpleTable
from config import base_url


@component
def page():
    pass


@component
def create_epic_area_form():
    pass


@component
def list_epic_areas(submitted_name):
    pass


@component
def delete_epic(set_delete_name):
    pass
