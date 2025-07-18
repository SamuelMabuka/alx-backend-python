#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient.
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct data."""
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, test_payload)
    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct repos_url."""
        payload = {"repos_url": "https://api.github.com/orgs/google/repos"}

        with patch.object(GithubOrgClient, 'org', new_callable=property) as mock_org:
            mock_org.return_value = payload

            client = GithubOrgClient("google")
            result = client._public_repos_url

            self.assertEqual(result, payload["repos_url"])
from unittest.mock import patch, MagicMock

class TestGithubOrgClient(unittest.TestCase):
    # ... other tests ...

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected list of repo names."""
        mock_repos_payload = [
            {'name': 'repo1'},
            {'name': 'repo2'},
            {'name': 'repo3'},
        ]
        mock_get_json.return_value = mock_repos_payload

        with patch.object(GithubOrgClient, '_public_repos_url', new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/testorg/repos"

            client = GithubOrgClient("testorg")
            repos = client.public_repos()

            self.assertEqual(repos, ["repo1", "repo2", "repo3"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/testorg/repos")

