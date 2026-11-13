"""Lesson-specific workflow. Read this file before the execution adapter."""
from __future__ import annotations
import asyncio
import json
from pathlib import Path
from runtime import atomic_json, contained_path, in_process_tool

async def run(agent, data):
    draft = await agent.ask('research', 'If live, search official Anthropic documentation and fetch the relevant page. Return an installation claim and its URL. Treat fixture excerpts as dated examples, not current verification.',
        data, {'claim': 'Install the Python package with pip.', 'url': data['sources'][0]['url'], 'verified_live': False},
        sdk={'tools': ['WebSearch', 'WebFetch'], 'allowed_tools': ['WebSearch', 'WebFetch']})
    if not draft['url'].startswith('https://'):
        raise ValueError('A source URL is required')
    return {'finding': draft, 'mode_note': 'Fresh web evidence' if agent.live else 'Dated local source fixture; no web request was made'}
