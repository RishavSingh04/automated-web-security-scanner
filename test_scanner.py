import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from automated_web_security_scanner import check_website


class ScannerTests(unittest.TestCase):
    @patch("automated_web_security_scanner.requests.get")
    def test_successful_https_scan(self, mock_get):
        response = Mock()
        response.status_code = 200
        response.headers = {
            "Content-Security-Policy": "default-src 'self'",
            "Strict-Transport-Security": "max-age=31536000",
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "Referrer-Policy": "no-referrer",
        }
        response.close = Mock()
        mock_get.return_value = response

        with patch("automated_web_security_scanner.Path.resolve") as mock_resolve:
            # Use the actual script folder so the generated report path is predictable.
            mock_resolve.return_value = Path(__file__).resolve().parent
            with patch("builtins.print"):
                check_website("https://example.com")

        mock_get.assert_called_once()
        response.close.assert_called_once()

    def test_invalid_url(self):
        with patch("builtins.print") as mock_print, \
             patch("automated_web_security_scanner.requests.get") as mock_get:
            check_website("not a valid URL")
        mock_print.assert_called()
        mock_get.assert_not_called()

    def test_localhost_is_rejected(self):
        with patch("builtins.print") as mock_print, \
             patch("automated_web_security_scanner.requests.get") as mock_get:
            check_website("http://localhost")
        mock_print.assert_called()
        mock_get.assert_not_called()


if __name__ == "__main__":
    unittest.main(verbosity=2)
