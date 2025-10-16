from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch, Mock
from datetime import datetime
import json

class ProfileAPITests(APITestCase):
    """
    Test cases for the /me endpoint
    """
    
    def setUp(self):
        """Set up test data"""
        self.url = reverse('profile')  # Make sure your URL name is 'profile'
    
    def test_endpoint_returns_200_status(self):
        """Test that the endpoint returns 200 OK"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_response_has_correct_structure(self):
        """Test that response has all required fields"""
        response = self.client.get(self.url)
        data = response.json()
        
        # Check top-level fields
        self.assertIn('status', data)
        self.assertIn('user', data)
        self.assertIn('timestamp', data)
        self.assertIn('fact', data)
        
        # Check user sub-fields
        self.assertIn('email', data['user'])
        self.assertIn('name', data['user'])
        self.assertIn('stack', data['user'])
    
    def test_status_field_is_success(self):
        """Test that status field is always 'success'"""
        response = self.client.get(self.url)
        data = response.json()
        self.assertEqual(data['status'], 'success')
    
    def test_timestamp_format(self):
        """Test that timestamp is in ISO 8601 format"""
        response = self.client.get(self.url)
        data = response.json()
        
        # Check if it's a string
        self.assertIsInstance(data['timestamp'], str)
        
        # Try to parse as ISO format datetime
        try:
            parsed_time = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
            self.assertIsInstance(parsed_time, datetime)
        except ValueError:
            self.fail("Timestamp is not in valid ISO 8601 format")
    
    def test_user_data_types(self):
        """Test that user fields are strings"""
        response = self.client.get(self.url)
        data = response.json()
        
        self.assertIsInstance(data['user']['email'], str)
        self.assertIsInstance(data['user']['name'], str)
        self.assertIsInstance(data['user']['stack'], str)
    
    def test_fact_field_is_string(self):
        """Test that fact field is a string"""
        response = self.client.get(self.url)
        data = response.json()
        self.assertIsInstance(data['fact'], str)
    
    def test_content_type_is_json(self):
        """Test that content type is application/json"""
        response = self.client.get(self.url)
        self.assertEqual(response['Content-Type'], 'application/json')
    
    @patch('profileapi.views.requests.get')
    def test_cat_fact_api_success(self, mock_get):
        """Test when cat fact API returns successful response"""
        # Mock successful API response
        mock_response = Mock()
        mock_response.json.return_value = {'fact': 'Cats are amazing creatures!'}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        response = self.client.get(self.url)
        data = response.json()
        
        self.assertEqual(data['fact'], 'Cats are amazing creatures!')
        mock_get.assert_called_once_with('https://catfact.ninja/fact', timeout=5)
    
    @patch('profileapi.views.requests.get')
    def test_cat_fact_api_failure(self, mock_get):
        """Test when cat fact API fails"""
        # Mock API failure
        mock_get.side_effect = Exception("API unavailable")
        
        response = self.client.get(self.url)
        data = response.json()
        
        # Should still return 200 with fallback fact
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('fact', data)
        self.assertIsInstance(data['fact'], str)
    
    @patch('profileapi.views.requests.get')
    def test_cat_fact_api_timeout(self, mock_get):
        """Test when cat fact API times out"""
        from requests.exceptions import Timeout
        mock_get.side_effect = Timeout("Request timed out")
        
        response = self.client.get(self.url)
        data = response.json()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('fact', data)
    
    def test_timestamp_updates_on_each_request(self):
        """Test that timestamp changes between requests"""
        response1 = self.client.get(self.url)
        data1 = response1.json()
        
        response2 = self.client.get(self.url)
        data2 = response2.json()
        
        # Timestamps should be different (or at least can be checked)
        self.assertIsInstance(data1['timestamp'], str)
        self.assertIsInstance(data2['timestamp'], str)
        # Note: We can't guarantee they'll be different if requests are very fast,
        # but we can verify they're both valid timestamps
    
    def test_user_data_content(self):
        """Test that user data contains expected content"""
        response = self.client.get(self.url)
        data = response.json()
        
        # Check that fields are not empty
        self.assertTrue(len(data['user']['email']) > 0)
        self.assertTrue(len(data['user']['name']) > 0)
        self.assertTrue(len(data['user']['stack']) > 0)
        
        # Check email format (basic check)
        self.assertIn('@', data['user']['email'])


class ProfileAPIEdgeCases(APITestCase):
    """Test edge cases and error scenarios"""
    
    def setUp(self):
        self.url = reverse('profile')
    
    @patch('profileapi.views.requests.get')
    def test_cat_fact_api_returns_invalid_json(self, mock_get):
        """Test when cat fact API returns invalid JSON"""
        mock_response = Mock()
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "doc", 0)
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        response = self.client.get(self.url)
        data = response.json()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('fact', data)
    
    @patch('profileapi.views.requests.get')
    def test_cat_fact_api_returns_empty_fact(self, mock_get):
        """Test when cat fact API returns empty fact"""
        mock_response = Mock()
        mock_response.json.return_value = {'fact': ''}  # Empty fact
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        response = self.client.get(self.url)
        data = response.json()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('fact', data)