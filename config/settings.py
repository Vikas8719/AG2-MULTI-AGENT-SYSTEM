"""
AG2 Multi-Agent System Configuration Management
Centralized settings using Pydantic for validation and type safety
"""

from typing import Optional, Literal
from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path


class AG2Settings(BaseSettings):
    """AG2 and AI Model Configuration"""
    
    # LLM Provider Selection
    llm_provider: Literal["openai", "huggingface", "anthropic"] = Field("openai", description="LLM Provider")
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = Field(None, description="OpenAI API Key")
    openai_org_id: Optional[str] = Field(None, description="OpenAI Organization ID")
    
    # Hugging Face Configuration
    huggingface_api_key: Optional[str] = Field(None, description="Hugging Face API Key")
    huggingface_model: str = Field("mistralai/Mixtral-8x7B-Instruct-v0.1", description="Hugging Face Model")
    huggingface_endpoint: Optional[str] = Field(None, description="Custom HF Inference Endpoint")
    
    # Anthropic Configuration
    anthropic_api_key: Optional[str] = None
    anthropic_model: str = "claude-3-opus-20240229"
    
    # Model Parameters (Applied to all providers)
    ag2_model: Optional[str] = Field(None, description="AG2 Model Name (auto-selected based on provider)")
    ag2_temperature: float = Field(0.7, ge=0.0, le=2.0)
    ag2_max_tokens: int = Field(4000, ge=100, le=8000)

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)
    
    @validator("llm_provider")
    def validate_provider(cls, v):
        """Validate LLM provider selection"""
        valid_providers = ["openai", "huggingface", "anthropic"]
        if v not in valid_providers:
            raise ValueError(f"LLM provider must be one of {valid_providers}")
        return v


class GitHubSettings(BaseSettings):
    """GitHub Integration Configuration"""
    
    github_token: Optional[str] = Field(None, description="GitHub Personal Access Token")
    github_username: Optional[str] = Field(None, description="GitHub Username")
    github_repo_prefix: str = Field("ag2-generated", description="Repository Prefix")
    github_default_branch: str = Field("main", description="Default Branch")
    github_org: Optional[str] = Field(None, description="GitHub Organization")

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)


class CloudSettings(BaseSettings):
    """Cloud Provider Configuration"""
    
    cloud_provider: Literal["aws", "gcp", "azure"] = Field("aws")
    
    # AWS
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: str = "us-east-1"
    aws_account_id: Optional[str] = None
    aws_ecr_registry: Optional[str] = None
    
    # GCP
    gcp_project_id: Optional[str] = None
    gcp_region: str = "us-central1"
    gcp_zone: str = "us-central1-a"
    google_application_credentials: Optional[str] = None
    gcp_container_registry: Optional[str] = None
    
    # Azure
    azure_subscription_id: Optional[str] = None
    azure_resource_group: Optional[str] = None
    azure_location: str = "eastus"
    azure_tenant_id: Optional[str] = None
    azure_client_id: Optional[str] = None
    azure_client_secret: Optional[str] = None
    azure_container_registry: Optional[str] = None

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)
    
    @validator("cloud_provider")
    def validate_cloud_provider(cls, v):
        """Validate cloud provider selection"""
        valid_providers = ["aws", "gcp", "azure"]
        if v not in valid_providers:
            raise ValueError(f"Cloud provider must be one of {valid_providers}")
        return v


class KubernetesSettings(BaseSettings):
    """Kubernetes Configuration"""
    
    kubeconfig_path: str = Field("~/.kube/config")
    k8s_namespace: str = Field("ag2-system")
    k8s_cluster_name: str = Field("production-cluster")
    k8s_context: Optional[str] = None

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)


class DockerSettings(BaseSettings):
    """Docker Configuration"""
    
    docker_registry: str = Field("docker.io")
    docker_username: Optional[str] = Field(None, description="Docker Registry Username")
    docker_password: Optional[str] = Field(None, description="Docker Registry Password")
    docker_email: Optional[str] = None

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)


class ArgoCDSettings(BaseSettings):
    """ArgoCD Configuration"""
    
    argocd_server: Optional[str] = None
    argocd_token: Optional[str] = None
    argocd_namespace: str = "argocd"
    argocd_project: str = "default"

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)


class DeploymentSettings(BaseSettings):
    """Deployment Configuration"""
    
    deployment_strategy: Literal["rolling", "blue-green", "canary"] = "rolling"
    deployment_replicas: int = Field(3, ge=1, le=100)
    deployment_auto_scale: bool = True
    deployment_min_replicas: int = Field(2, ge=1)
    deployment_max_replicas: int = Field(10, ge=1)
    deployment_cpu_threshold: int = Field(70, ge=1, le=100)

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)


class LoggingSettings(BaseSettings):
    """Logging Configuration"""
    
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    log_file: str = "logs/app.log"
    log_format: Literal["json", "text"] = "json"
    log_max_size: int = Field(100, description="Max log file size in MB")
    log_backup_count: int = Field(10, description="Number of backup log files")
    agent_log_dir: str = "logs/agents"

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)


class DatabaseSettings(BaseSettings):
    """Database Configuration"""
    
    database_type: Literal["sqlite", "postgresql", "mysql", "mongodb"] = "sqlite"
    database_url: str = "sqlite:///./ag2_system.db"
    
    # PostgreSQL
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "ag2_user"
    postgres_password: Optional[str] = None
    postgres_db: str = "ag2_db"
    
    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: Optional[str] = None
    redis_db: int = 0

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)


class SecuritySettings(BaseSettings):
    """Security Configuration"""
    
    secret_key: Optional[str] = Field(None, min_length=32)
    encryption_key: Optional[str] = Field(None, min_length=32)
    jwt_secret: Optional[str] = Field(None, min_length=32)
    jwt_algorithm: str = "HS256"
    jwt_expiration: int = 3600

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)


class ApplicationSettings(BaseSettings):
    """Application Configuration"""
    
    app_name: str = "AG2 Multi-Agent System"
    app_version: str = "1.0.0"
    app_env: Literal["development", "staging", "production"] = "development"
    debug: bool = True
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    streamlit_port: int = 8501

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)


class FeatureFlags(BaseSettings):
    """Feature Flags Configuration"""
    
    enable_human_approval: bool = True
    enable_auto_deployment: bool = False
    enable_slack_notifications: bool = False
    enable_email_notifications: bool = False
    enable_metrics: bool = True
    enable_tracing: bool = True

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)


class MonitoringSettings(BaseSettings):
    """Monitoring and Observability Configuration"""
    
    prometheus_port: int = 9090
    grafana_url: Optional[str] = "http://localhost:3000"
    jaeger_endpoint: Optional[str] = "http://localhost:14268/api/traces"
    sentry_dsn: Optional[str] = None

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)


class NotificationSettings(BaseSettings):
    """Notification Configuration"""
    
    slack_webhook_url: Optional[str] = None
    slack_channel: str = "#deployments"
    email_smtp_host: str = "smtp.gmail.com"
    email_smtp_port: int = 587
    email_from: Optional[str] = None
    email_password: Optional[str] = None
    email_to: Optional[str] = None

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)


class MLflowSettings(BaseSettings):
    """MLflow Configuration for ML Projects"""
    
    mlflow_tracking_uri: str = "http://localhost:5000"
    mlflow_experiment_name: str = "ag2-experiments"
    mlflow_artifact_location: Optional[str] = None

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)


class TerraformSettings(BaseSettings):
    """Terraform Configuration"""
    
    terraform_backend: Literal["s3", "gcs", "azurerm", "local"] = "s3"
    terraform_state_bucket: Optional[str] = None
    terraform_state_key: str = "ag2/terraform.tfstate"
    terraform_lock_table: Optional[str] = None

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)


class CICDSettings(BaseSettings):
    """CI/CD Configuration"""
    
    ci_platform: Literal["github-actions", "gitlab-ci", "jenkins"] = "github-actions"
    ci_trigger_on_push: bool = True
    ci_run_tests: bool = True
    ci_run_security_scan: bool = True
    ci_deploy_to_staging: bool = True
    ci_deploy_to_prod: bool = False

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)


class ProjectDefaultsSettings(BaseSettings):
    """Project Generation Defaults"""
    
    default_language: str = "python"
    default_framework: str = "fastapi"
    default_database: str = "postgresql"
    default_cache: str = "redis"
    default_message_queue: str = "rabbitmq"

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)


class RateLimitSettings(BaseSettings):
    """Rate Limiting Configuration"""
    
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 60
    rate_limit_per_hour: int = 1000

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)


class TimeoutSettings(BaseSettings):
    """Timeout Configuration (in seconds)"""
    
    agent_timeout: int = 300
    http_timeout: int = 30
    deployment_timeout: int = 600

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)


class ResourceLimitSettings(BaseSettings):
    """Resource Limits Configuration"""
    
    max_file_size: int = Field(100, description="Max file size in MB")
    max_project_size: int = Field(1000, description="Max project size in MB")
    max_concurrent_agents: int = 5
    max_concurrent_projects: int = 10

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)


class DevelopmentSettings(BaseSettings):
    """Development and Testing Configuration"""
    
    testing_mode: bool = False
    mock_deployments: bool = False
    dry_run: bool = False
    verbose: bool = True

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)


class Settings:
    """
    Unified Settings Class
    Aggregates all configuration sections
    """
    
    def __init__(self):
        """Initialize all settings sections"""
        self.ag2 = AG2Settings()
        self.github = GitHubSettings()
        self.cloud = CloudSettings()
        self.kubernetes = KubernetesSettings()
        self.docker = DockerSettings()
        self.argocd = ArgoCDSettings()
        self.deployment = DeploymentSettings()
        self.logging = LoggingSettings()
        self.database = DatabaseSettings()
        self.security = SecuritySettings()
        self.application = ApplicationSettings()
        self.features = FeatureFlags()
        self.monitoring = MonitoringSettings()
        self.notifications = NotificationSettings()
        self.mlflow = MLflowSettings()
        self.terraform = TerraformSettings()
        self.cicd = CICDSettings()
        self.project_defaults = ProjectDefaultsSettings()
        self.rate_limit = RateLimitSettings()
        self.timeouts = TimeoutSettings()
        self.resource_limits = ResourceLimitSettings()
        self.development = DevelopmentSettings()
    
    def validate_required_settings(self) -> tuple[bool, list[str]]:
        """
        Validate that all required settings are configured
        
        Returns:
            tuple: (is_valid, list_of_missing_settings)
        """
        missing = []
        
        # Check AG2 settings
        if not self.ag2.openai_api_key or self.ag2.openai_api_key == "sk-your-openai-api-key-here":
            missing.append("OPENAI_API_KEY")
        
        # Check GitHub settings
        if not self.github.github_token or "your" in self.github.github_token.lower():
            missing.append("GITHUB_TOKEN")
        
        if not self.github.github_username or "your" in self.github.github_username.lower():
            missing.append("GITHUB_USERNAME")
        
        # Check Docker settings
        if not self.docker.docker_username or "your" in self.docker.docker_username.lower():
            missing.append("DOCKER_USERNAME")
        
        if not self.docker.docker_password or "your" in self.docker.docker_password.lower():
            missing.append("DOCKER_PASSWORD")
        
        # Check cloud provider specific settings
        if self.cloud.cloud_provider == "aws":
            if not self.cloud.aws_access_key_id:
                missing.append("AWS_ACCESS_KEY_ID")
            if not self.cloud.aws_secret_access_key:
                missing.append("AWS_SECRET_ACCESS_KEY")
        
        elif self.cloud.cloud_provider == "gcp":
            if not self.cloud.gcp_project_id:
                missing.append("GCP_PROJECT_ID")
            if not self.cloud.google_application_credentials:
                missing.append("GOOGLE_APPLICATION_CREDENTIALS")
        
        elif self.cloud.cloud_provider == "azure":
            if not self.cloud.azure_subscription_id:
                missing.append("AZURE_SUBSCRIPTION_ID")
            if not self.cloud.azure_client_id:
                missing.append("AZURE_CLIENT_ID")
        
        return len(missing) == 0, missing
    
    def get_cloud_config(self) -> dict:
        """Get cloud provider specific configuration"""
        provider = self.cloud.cloud_provider
        
        if provider == "aws":
            return {
                "provider": "aws",
                "access_key": self.cloud.aws_access_key_id,
                "secret_key": self.cloud.aws_secret_access_key,
                "region": self.cloud.aws_region,
                "account_id": self.cloud.aws_account_id,
                "registry": self.cloud.aws_ecr_registry
            }
        elif provider == "gcp":
            return {
                "provider": "gcp",
                "project_id": self.cloud.gcp_project_id,
                "region": self.cloud.gcp_region,
                "zone": self.cloud.gcp_zone,
                "credentials": self.cloud.google_application_credentials,
                "registry": self.cloud.gcp_container_registry
            }
        else:  # azure
            return {
                "provider": "azure",
                "subscription_id": self.cloud.azure_subscription_id,
                "resource_group": self.cloud.azure_resource_group,
                "location": self.cloud.azure_location,
                "tenant_id": self.cloud.azure_tenant_id,
                "client_id": self.cloud.azure_client_id,
                "client_secret": self.cloud.azure_client_secret,
                "registry": self.cloud.azure_container_registry
            }
    
    def create_log_directories(self):
        """Create required log directories"""
        log_dir = Path(self.logging.log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)
        
        agent_log_dir = Path(self.logging.agent_log_dir)
        agent_log_dir.mkdir(parents=True, exist_ok=True)
    
    def create_project_directory(self):
        """Create projects directory"""
        projects_dir = Path("projects")
        projects_dir.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()


# Initialize directories on import
try:
    settings.create_log_directories()
    settings.create_project_directory()
except Exception as e:
    print(f"Warning: Could not create directories: {e}")


__all__ = ["settings", "Settings"]
