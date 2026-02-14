"""
Advanced Logging Configuration for AG2 Multi-Agent System
Supports JSON and text formats, file rotation, and agent-specific logging
"""

import logging
import logging.handlers
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
from pythonjsonlogger import jsonlogger


class ColoredFormatter(logging.Formatter):
    """Custom formatter with color support for console output"""
    
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        """Format log record with colors"""
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.RESET}"
        return super().format(record)


class AgentLogFilter(logging.Filter):
    """Filter to add agent context to log records"""
    
    def __init__(self, agent_name: str):
        super().__init__()
        self.agent_name = agent_name
    
    def filter(self, record):
        """Add agent name to record"""
        record.agent_name = self.agent_name
        return True


class StreamlitLogHandler(logging.Handler):
    """Custom handler to send logs to Streamlit UI"""
    
    def __init__(self, callback=None):
        super().__init__()
        self.callback = callback
        self.logs = []
    
    def emit(self, record):
        """Emit log record to callback or store in buffer"""
        try:
            log_entry = self.format(record)
            self.logs.append({
                'timestamp': datetime.now().isoformat(),
                'level': record.levelname,
                'message': log_entry,
                'agent': getattr(record, 'agent_name', 'system')
            })
            
            if self.callback:
                self.callback(log_entry)
        except Exception:
            self.handleError(record)
    
    def get_logs(self, limit: Optional[int] = None):
        """Get stored logs"""
        if limit:
            return self.logs[-limit:]
        return self.logs
    
    def clear_logs(self):
        """Clear stored logs"""
        self.logs = []


class LoggingConfig:
    """
    Centralized Logging Configuration Manager
    """
    
    def __init__(self, config):
        """
        Initialize logging configuration
        
        Args:
            config: Settings object with logging configuration
        """
        self.config = config
        self.log_level = getattr(logging, config.logging.log_level)
        self.log_file = config.logging.log_file
        self.log_format = config.logging.log_format
        self.agent_log_dir = Path(config.logging.agent_log_dir)
        self.max_bytes = config.logging.log_max_size * 1024 * 1024  # Convert MB to bytes
        self.backup_count = config.logging.log_backup_count
        
        # Ensure directories exist
        Path(self.log_file).parent.mkdir(parents=True, exist_ok=True)
        self.agent_log_dir.mkdir(parents=True, exist_ok=True)
        
        # Store handlers for later access
        self.streamlit_handler = None
    
    def setup_root_logger(self):
        """Setup root logger with file and console handlers"""
        root_logger = logging.getLogger()
        root_logger.setLevel(self.log_level)
        
        # Remove existing handlers
        root_logger.handlers.clear()
        
        # Add console handler
        console_handler = self._create_console_handler()
        root_logger.addHandler(console_handler)
        
        # Add file handler
        file_handler = self._create_file_handler(self.log_file)
        root_logger.addHandler(file_handler)
        
        return root_logger
    
    def _create_console_handler(self) -> logging.Handler:
        """Create colored console handler"""
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(self.log_level)
        
        if self.log_format == "json":
            formatter = jsonlogger.JsonFormatter(
                '%(timestamp)s %(level)s %(name)s %(message)s',
                rename_fields={'levelname': 'level', 'asctime': 'timestamp'}
            )
        else:
            formatter = ColoredFormatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        
        handler.setFormatter(formatter)
        return handler
    
    def _create_file_handler(self, log_file: str) -> logging.Handler:
        """Create rotating file handler"""
        handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=self.max_bytes,
            backupCount=self.backup_count,
            encoding='utf-8'
        )
        handler.setLevel(self.log_level)
        
        if self.log_format == "json":
            formatter = jsonlogger.JsonFormatter(
                '%(timestamp)s %(level)s %(name)s %(message)s %(pathname)s %(lineno)d',
                rename_fields={'levelname': 'level', 'asctime': 'timestamp'}
            )
        else:
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(pathname)s:%(lineno)d]',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        
        handler.setFormatter(formatter)
        return handler
    
    def setup_agent_logger(self, agent_name: str) -> logging.Logger:
        """
        Setup logger for specific agent
        
        Args:
            agent_name: Name of the agent
            
        Returns:
            Configured logger instance
        """
        logger = logging.getLogger(f"agent.{agent_name}")
        logger.setLevel(self.log_level)
        
        # Prevent propagation to avoid duplicate logs
        logger.propagate = False
        
        # Add agent-specific file handler
        agent_log_file = self.agent_log_dir / f"{agent_name}.log"
        file_handler = self._create_file_handler(str(agent_log_file))
        
        # Add agent filter
        agent_filter = AgentLogFilter(agent_name)
        file_handler.addFilter(agent_filter)
        
        logger.addHandler(file_handler)
        
        # Add console handler
        console_handler = self._create_console_handler()
        console_handler.addFilter(agent_filter)
        logger.addHandler(console_handler)
        
        return logger
    
    def setup_streamlit_handler(self, callback=None) -> StreamlitLogHandler:
        """
        Setup Streamlit-specific log handler
        
        Args:
            callback: Optional callback function for real-time log updates
            
        Returns:
            StreamlitLogHandler instance
        """
        self.streamlit_handler = StreamlitLogHandler(callback)
        self.streamlit_handler.setLevel(self.log_level)
        
        if self.log_format == "json":
            formatter = jsonlogger.JsonFormatter(
                '%(timestamp)s %(level)s %(agent_name)s %(message)s',
                rename_fields={'levelname': 'level', 'asctime': 'timestamp'}
            )
        else:
            formatter = logging.Formatter(
                '%(asctime)s - [%(agent_name)s] - %(levelname)s - %(message)s',
                datefmt='%H:%M:%S'
            )
        
        self.streamlit_handler.setFormatter(formatter)
        
        # Add to root logger
        root_logger = logging.getLogger()
        root_logger.addHandler(self.streamlit_handler)
        
        return self.streamlit_handler
    
    def get_streamlit_logs(self, limit: Optional[int] = None) -> list:
        """Get logs from Streamlit handler"""
        if self.streamlit_handler:
            return self.streamlit_handler.get_logs(limit)
        return []
    
    def clear_streamlit_logs(self):
        """Clear Streamlit handler logs"""
        if self.streamlit_handler:
            self.streamlit_handler.clear_logs()
    
    def setup_module_logger(self, module_name: str) -> logging.Logger:
        """
        Setup logger for a specific module
        
        Args:
            module_name: Name of the module
            
        Returns:
            Configured logger instance
        """
        logger = logging.getLogger(module_name)
        logger.setLevel(self.log_level)
        return logger
    
    def log_system_info(self):
        """Log system and configuration information"""
        logger = logging.getLogger("system")
        logger.info("="*80)
        logger.info("AG2 Multi-Agent System Starting")
        logger.info("="*80)
        logger.info(f"Application: {self.config.application.app_name}")
        logger.info(f"Version: {self.config.application.app_version}")
        logger.info(f"Environment: {self.config.application.app_env}")
        logger.info(f"Log Level: {self.config.logging.log_level}")
        logger.info(f"Log Format: {self.config.logging.log_format}")
        logger.info(f"Cloud Provider: {self.config.cloud.cloud_provider}")
        logger.info(f"AG2 Model: {self.config.ag2.ag2_model}")
        logger.info("="*80)
    
    def log_agent_execution(self, agent_name: str, action: str, status: str, details: dict = None):
        """
        Log agent execution details
        
        Args:
            agent_name: Name of the agent
            action: Action being performed
            status: Status (started, completed, failed)
            details: Additional details dictionary
        """
        logger = logging.getLogger(f"agent.{agent_name}")
        
        log_data = {
            'agent': agent_name,
            'action': action,
            'status': status,
            'timestamp': datetime.now().isoformat()
        }
        
        if details:
            log_data.update(details)
        
        if status == "started":
            logger.info(f"Started: {action}")
        elif status == "completed":
            logger.info(f"Completed: {action}")
        elif status == "failed":
            logger.error(f"Failed: {action}")
        
        if self.log_format == "json":
            logger.info(json.dumps(log_data))


def setup_logging(config):
    """
    Convenience function to setup logging
    
    Args:
        config: Settings object
        
    Returns:
        LoggingConfig instance
    """
    logging_config = LoggingConfig(config)
    logging_config.setup_root_logger()
    logging_config.log_system_info()
    return logging_config


# Convenience function for getting logger
def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


__all__ = [
    'LoggingConfig',
    'setup_logging',
    'get_logger',
    'StreamlitLogHandler',
    'ColoredFormatter',
    'AgentLogFilter'
]
