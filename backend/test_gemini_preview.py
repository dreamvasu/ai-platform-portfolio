#!/usr/bin/env python
"""Test Gemini models using preview API"""
import vertexai
from vertexai.preview.generative_models import GenerativeModel

vertexai.init(project='ai-portfolio-1762033947', location='us-central1')

print("Testing Gemini models with PREVIEW API...")
models_to_test = [
    'gemini-1.5-flash-001',
    'gemini-1.5-pro-001',
    'gemini-1.0-pro-002',
    'gemini-pro',
    'gemini-1.5-flash',
    'gemini-1.5-pro',
]

for model_name in models_to_test:
    try:
        print(f"\nTrying {model_name}...")
        model = GenerativeModel(model_name)
        response = model.generate_content("Say 'hi' in one word")
        print(f"✅ {model_name} WORKS!")
        print(f"   Response: {response.text}")
        print(f"\n🎉 Use this model: {model_name}")
        break
    except Exception as e:
        error_msg = str(e)[:200]
        print(f"❌ {model_name}: {error_msg}")
