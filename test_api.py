#!/usr/bin/env python3
"""
Test script for NextWish Birthday Greeting API
Demonstrates how to use all API endpoints
"""

import requests
import json
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:5000"

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))
    print(f"{'='*60}\n")

def test_api_info():
    """Test 1: Get API information"""
    response = requests.get(f"{BASE_URL}/")
    print_response("API Information", response)
    return response.json()

def test_list_templates():
    """Test 2: List available templates"""
    response = requests.get(f"{BASE_URL}/api/templates")
    print_response("Available Templates", response)
    return response.json()

def test_generate_template1():
    """Test 3: Generate greeting with Template 1"""
    print("\n🎨 Generating Template 1: Classic Birthday Card")

    data = {
        'template_id': 'template1',
        'name': 'Sarah Johnson',
        'message': 'Wishing you an amazing birthday filled with joy and happiness!'
    }

    # Optional: Add user image if available
    # files = {'user_image': open('path/to/photo.jpg', 'rb')}
    # response = requests.post(f"{BASE_URL}/api/generate", data=data, files=files)

    response = requests.post(f"{BASE_URL}/api/generate", data=data)
    result = response.json()
    print_response("Template 1 Generated", response)

    if result.get('success'):
        print(f"✅ Greeting URL: {result['greeting_url']}")
        print(f"   Greeting ID: {result['greeting_id']}")
        return result['greeting_id']
    return None

def test_generate_template2():
    """Test 4: Generate greeting with Template 2"""
    print("\n🎨 Generating Template 2: 3D Photo Carousel")

    data = {
        'template_id': 'template2',
        'name': 'Mike Anderson'
    }

    # For testing without actual images
    response = requests.post(f"{BASE_URL}/api/generate", data=data)
    result = response.json()
    print_response("Template 2 Generated", response)

    if result.get('success'):
        print(f"✅ Greeting URL: {result['greeting_url']}")
        return result['greeting_id']
    return None

def test_generate_template3():
    """Test 5: Generate greeting with Template 3"""
    print("\n🎨 Generating Template 3: Interactive Gift Card")

    data = {
        'template_id': 'template3',
        'name': 'Emily Davis',
        'message': 'Hope your special day brings you all the happiness you deserve! 🎉'
    }

    response = requests.post(f"{BASE_URL}/api/generate", data=data)
    result = response.json()
    print_response("Template 3 Generated", response)

    if result.get('success'):
        print(f"✅ Greeting URL: {result['greeting_url']}")
        return result['greeting_id']
    return None

def test_get_greeting_info(greeting_id):
    """Test 6: Get information about a greeting"""
    if not greeting_id:
        print("\n⚠️  Skipping - No greeting_id provided")
        return

    print(f"\n📋 Getting info for greeting: {greeting_id}")
    response = requests.get(f"{BASE_URL}/api/greeting/{greeting_id}")
    print_response(f"Greeting Info ({greeting_id[:8]}...)", response)

def test_invalid_template():
    """Test 7: Error handling - Invalid template"""
    print("\n🔍 Testing error handling with invalid template")

    data = {
        'template_id': 'invalid_template',
        'name': 'Test User'
    }

    response = requests.post(f"{BASE_URL}/api/generate", data=data)
    print_response("Invalid Template Error", response)

def test_missing_name():
    """Test 8: Error handling - Missing required field"""
    print("\n🔍 Testing error handling with missing name")

    data = {
        'template_id': 'template1'
        # name is missing
    }

    response = requests.post(f"{BASE_URL}/api/generate", data=data)
    print_response("Missing Name Error", response)

def test_delete_greeting(greeting_id):
    """Test 9: Delete a greeting"""
    if not greeting_id:
        print("\n⚠️  Skipping delete - No greeting_id provided")
        return

    user_input = input(f"\n❓ Delete greeting {greeting_id[:8]}...? (y/N): ")
    if user_input.lower() != 'y':
        print("   Skipped deletion")
        return

    response = requests.delete(f"{BASE_URL}/api/greeting/{greeting_id}")
    print_response("Delete Greeting", response)

def run_all_tests():
    """Run complete test suite"""
    print("\n" + "="*60)
    print("  NextWish API Test Suite")
    print("="*60)

    try:
        # Basic tests
        test_api_info()
        test_list_templates()

        # Generate greetings with each template
        greeting_id_1 = test_generate_template1()
        greeting_id_2 = test_generate_template2()
        greeting_id_3 = test_generate_template3()

        # Get info about first generated greeting
        if greeting_id_1:
            test_get_greeting_info(greeting_id_1)

        # Error handling tests
        test_invalid_template()
        test_missing_name()

        # Cleanup (optional)
        if greeting_id_1:
            test_delete_greeting(greeting_id_1)

        # Summary
        print("\n" + "="*60)
        print("  Test Summary")
        print("="*60)
        print(f"✅ All tests completed!")

        if greeting_id_2:
            print(f"\n🔗 View Template 2: {BASE_URL}/greeting/{greeting_id_2}")
        if greeting_id_3:
            print(f"🔗 View Template 3: {BASE_URL}/greeting/{greeting_id_3}")
        print("\n")

    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API")
        print("   Make sure the Flask server is running:")
        print("   python app.py")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    run_all_tests()
