"""
Test suite for Codicent CLI application.
"""

import unittest
import sys
import os
import logging
from unittest.mock import patch, MagicMock, mock_open
from io import StringIO

# Add the current directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import app


class TestCodicentCLI(unittest.TestCase):
    """Test cases for the Codicent CLI application."""

    def setUp(self):
        """Set up test fixtures."""
        self.original_argv = sys.argv.copy()
        self.original_environ = os.environ.copy()

    def tearDown(self):
        """Clean up after tests."""
        sys.argv = self.original_argv
        os.environ.clear()
        os.environ.update(self.original_environ)

    def test_show_help(self):
        """Test help message display."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            app.show_help()
            output = fake_out.getvalue()
            self.assertIn("Codicent CLI", output)
            self.assertIn("USAGE:", output)
            self.assertIn("OPTIONS:", output)
            self.assertIn("EXAMPLES:", output)

    def test_show_version(self):
        """Test version display."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            app.show_version()
            output = fake_out.getvalue()
            self.assertIn("Codicent CLI v0.4.6", output)

    def test_validate_input_valid(self):
        """Test input validation with valid input."""
        is_valid, error = app.validate_input("What is Python?")
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_validate_input_empty(self):
        """Test input validation with empty input."""
        is_valid, error = app.validate_input("")
        self.assertFalse(is_valid)
        self.assertEqual(error, "Empty question provided")

        is_valid, error = app.validate_input("   ")
        self.assertFalse(is_valid)
        self.assertEqual(error, "Empty question provided")

    def test_validate_input_too_long(self):
        """Test input validation with overly long input."""
        long_question = "x" * 10001
        is_valid, error = app.validate_input(long_question)
        self.assertFalse(is_valid)
        self.assertEqual(error, "Question too long (max 10,000 characters)")

    @patch('sys.argv', ['codicent', '--help'])
    def test_main_help_flag(self):
        """Test main function with help flag."""
        with patch('app.show_help') as mock_help:
            result = app.main()
            mock_help.assert_called_once()
            self.assertEqual(result, 0)

    @patch('sys.argv', ['codicent', '-h'])
    def test_main_help_flag_short(self):
        """Test main function with short help flag."""
        with patch('app.show_help') as mock_help:
            result = app.main()
            mock_help.assert_called_once()
            self.assertEqual(result, 0)

    @patch('sys.argv', ['codicent', '--version'])
    def test_main_version_flag(self):
        """Test main function with version flag."""
        with patch('app.show_version') as mock_version:
            result = app.main()
            mock_version.assert_called_once()
            self.assertEqual(result, 0)

    @patch('sys.argv', ['codicent', '-v'])
    def test_main_version_flag_short(self):
        """Test main function with short version flag."""
        with patch('app.show_version') as mock_version:
            result = app.main()
            mock_version.assert_called_once()
            self.assertEqual(result, 0)

    def test_main_missing_token(self):
        """Test main function without CODICENT_TOKEN."""
        sys.argv = ['codicent', 'test question']
        if 'CODICENT_TOKEN' in os.environ:
            del os.environ['CODICENT_TOKEN']
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = app.main()
            output = fake_out.getvalue()
            self.assertEqual(result, 1)
            self.assertIn("CODICENT_TOKEN environment variable is not set", output)

    @patch('app.Codicent')
    def test_main_api_client_init_failure(self, mock_codicent_class):
        """Test main function when API client initialization fails."""
        sys.argv = ['codicent', 'test question']
        os.environ['CODICENT_TOKEN'] = 'test_token'
        
        mock_codicent_class.side_effect = Exception("API initialization failed")
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = app.main()
            output = fake_out.getvalue()
            self.assertEqual(result, 1)
            self.assertIn("Failed to initialize Codicent API client", output)

    @patch('app.Codicent')
    def test_main_one_shot_mode_success(self, mock_codicent_class):
        """Test successful one-shot mode execution."""
        sys.argv = ['codicent', 'test', 'question']
        os.environ['CODICENT_TOKEN'] = 'test_token'
        
        mock_codicent = MagicMock()
        mock_codicent_class.return_value = mock_codicent
        mock_codicent.post_chat_reply.return_value = {
            'id': 'test_id',
            'content': 'Test response'
        }
        
        with patch('sys.stdout', new=StringIO()):
            result = app.main()
            self.assertEqual(result, 0)
            mock_codicent.post_chat_reply.assert_called_once_with('test question', None)

    @patch('app.Codicent')
    def test_main_at_message(self, mock_codicent_class):
        """Test @ message handling."""
        sys.argv = ['codicent', '@mention', 'test', 'message']
        os.environ['CODICENT_TOKEN'] = 'test_token'
        
        mock_codicent = MagicMock()
        mock_codicent_class.return_value = mock_codicent
        mock_codicent.post_message.return_value = {'status': 'success'}
        
        with patch('sys.stdout', new=StringIO()):
            result = app.main()
            self.assertEqual(result, 0)
            mock_codicent.post_message.assert_called_once_with('@mention test message', type="info")

    @patch('sys.stdin')
    @patch('app.Codicent')
    def test_main_stdin_input(self, mock_codicent_class, mock_stdin):
        """Test stdin input handling."""
        sys.argv = ['codicent']
        os.environ['CODICENT_TOKEN'] = 'test_token'
        
        mock_stdin.isatty.return_value = False
        mock_stdin.read.return_value = 'stdin question'
        
        mock_codicent = MagicMock()
        mock_codicent_class.return_value = mock_codicent
        mock_codicent.post_chat_reply.return_value = {
            'id': 'test_id',
            'content': 'Test response'
        }
        
        with patch('sys.stdout', new=StringIO()), \
             patch('builtins.input', side_effect=KeyboardInterrupt()):  # Prevent interactive mode
            result = app.main()
            self.assertEqual(result, 0)
            mock_codicent.post_chat_reply.assert_called_once_with('stdin question', None)

    @patch('app.Codicent')
    def test_api_connection_error(self, mock_codicent_class):
        """Test handling of API connection errors."""
        sys.argv = ['codicent', 'test question']
        os.environ['CODICENT_TOKEN'] = 'test_token'
        
        mock_codicent = MagicMock()
        mock_codicent_class.return_value = mock_codicent
        mock_codicent.post_chat_reply.side_effect = ConnectionError("Network error")
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = app.main()
            output = fake_out.getvalue()
            self.assertEqual(result, 1)
            self.assertIn("Network error", output)

    @patch('app.Codicent')
    def test_api_general_error(self, mock_codicent_class):
        """Test handling of general API errors."""
        sys.argv = ['codicent', 'test question']
        os.environ['CODICENT_TOKEN'] = 'test_token'
        
        mock_codicent = MagicMock()
        mock_codicent_class.return_value = mock_codicent
        mock_codicent.post_chat_reply.side_effect = Exception("API error")
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = app.main()
            output = fake_out.getvalue()
            self.assertEqual(result, 1)
            self.assertIn("API error", output)

    @patch('logging.getLogger')
    @patch('app.Codicent')
    def test_verbose_logging(self, mock_codicent_class, mock_get_logger):
        """Test verbose logging flag."""
        sys.argv = ['codicent', '--verbose', 'test question']
        os.environ['CODICENT_TOKEN'] = 'test_token'
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        mock_codicent = MagicMock()
        mock_codicent_class.return_value = mock_codicent
        mock_codicent.post_chat_reply.return_value = {
            'id': 'test_id',
            'content': 'Test response'
        }
        
        with patch('sys.stdout', new=StringIO()):
            app.main()
            # Verify logging level was changed to INFO
            mock_logger.setLevel.assert_called_with(logging.INFO)

    @patch('logging.getLogger')
    @patch('app.Codicent')
    def test_quiet_logging(self, mock_codicent_class, mock_get_logger):
        """Test quiet logging flag."""
        sys.argv = ['codicent', '--quiet', 'test question']
        os.environ['CODICENT_TOKEN'] = 'test_token'
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        mock_codicent = MagicMock()
        mock_codicent_class.return_value = mock_codicent
        mock_codicent.post_chat_reply.return_value = {
            'id': 'test_id',
            'content': 'Test response'
        }
        
        with patch('sys.stdout', new=StringIO()):
            app.main()
            # Verify logging level was changed to ERROR
            mock_logger.setLevel.assert_called_with(logging.ERROR)


class TestInteractiveMode(unittest.TestCase):
    """Test cases specifically for interactive mode."""

    def setUp(self):
        """Set up test fixtures."""
        self.original_argv = sys.argv.copy()
        self.original_environ = os.environ.copy()

    def tearDown(self):
        """Clean up after tests."""
        sys.argv = self.original_argv
        os.environ.clear()
        os.environ.update(self.original_environ)

    @patch('builtins.input')
    @patch('app.Codicent')
    def test_interactive_mode_basic(self, mock_codicent_class, mock_input):
        """Test basic interactive mode functionality."""
        sys.argv = ['codicent', '-t']
        os.environ['CODICENT_TOKEN'] = 'test_token'
        
        # Simulate user input followed by KeyboardInterrupt to exit
        mock_input.side_effect = ['test question', KeyboardInterrupt()]
        
        mock_codicent = MagicMock()
        mock_codicent_class.return_value = mock_codicent
        mock_codicent.post_chat_reply.return_value = {
            'id': 'test_id',
            'content': 'Test response'
        }
        
        with patch('sys.stdout', new=StringIO()):
            result = app.main()
            self.assertEqual(result, 0)
            mock_codicent.post_chat_reply.assert_called_once_with('test question', None)

    @patch('builtins.input')
    @patch('app.Codicent')
    def test_interactive_mode_empty_input(self, mock_codicent_class, mock_input):
        """Test interactive mode with empty input."""
        sys.argv = ['codicent', '--interactive']
        os.environ['CODICENT_TOKEN'] = 'test_token'
        
        # Simulate empty input followed by KeyboardInterrupt
        mock_input.side_effect = ['', '   ', KeyboardInterrupt()]
        
        mock_codicent = MagicMock()
        mock_codicent_class.return_value = mock_codicent
        
        with patch('sys.stdout', new=StringIO()):
            result = app.main()
            self.assertEqual(result, 0)
            # Should not call API for empty inputs
            mock_codicent.post_chat_reply.assert_not_called()


if __name__ == '__main__':
    # Run the tests
    unittest.main()
