"""
Agent 1: Analyzer & Planner
Analyzes input data/tasks and creates comprehensive project plans
"""

from typing import Dict, Any, Optional, List
import json
import pandas as pd
from pathlib import Path
from .base_agent import BaseAgent


class AnalyzerAgent(BaseAgent):
    """
    Agent responsible for analyzing requirements and creating execution plans
    """
    
    def __init__(self, config: Any):
        """Initialize Analyzer Agent"""
        
        system_message = """You are an expert Software Architect and Project Planner.
        
Your responsibilities:
1. Analyze CSV data or text-based task descriptions
2. Identify project requirements and constraints
3. Create detailed execution plans
4. Generate complete project folder structures
5. Define appropriate technology stacks
6. Break down tasks into manageable components
7. Identify infrastructure requirements

When analyzing:
- Extract key requirements and goals
- Identify data patterns and relationships (for CSV)
- Determine project type (web app, API, ML model, etc.)
- Assess complexity and scope
- Consider scalability and best practices

Output Format (JSON):
{
    "project_type": "...",
    "requirements": [...],
    "tech_stack": {
        "language": "...",
        "framework": "...",
        "database": "...",
        "other_tools": [...]
    },
    "folder_structure": {
        "root": "project_name",
        "directories": [...],
        "key_files": [...]
    },
    "task_breakdown": [
        {
            "task": "...",
            "priority": "high/medium/low",
            "estimated_effort": "...",
            "dependencies": [...]
        }
    ],
    "infrastructure": {
        "compute": "...",
        "storage": "...",
        "networking": "...",
        "services": [...]
    },
    "dependencies": [...]
}

Be thorough, precise, and production-focused."""
        
        super().__init__(
            name="AnalyzerAgent",
            role="Requirement Analysis and Project Planning",
            system_message=system_message,
            config=config
        )
    
    def validate_input(self, input_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate input data"""
        
        if not input_data:
            return False, "Input data is empty"
        
        input_type = input_data.get('type')
        if input_type not in ['csv', 'text']:
            return False, f"Invalid input type: {input_type}. Must be 'csv' or 'text'"
        
        if input_type == 'csv':
            if 'csv_path' not in input_data:
                return False, "CSV path not provided"
            
            csv_path = Path(input_data['csv_path'])
            if not csv_path.exists():
                return False, f"CSV file not found: {csv_path}"
        
        elif input_type == 'text':
            if 'task_description' not in input_data:
                return False, "Task description not provided"
            
            if len(input_data['task_description'].strip()) < 10:
                return False, "Task description too short (minimum 10 characters)"
        
        return True, None
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute analysis and planning"""
        
        self.logger.info("Starting requirement analysis and planning...")
        
        input_type = input_data['type']
        
        if input_type == 'csv':
            analysis = self._analyze_csv(input_data)
        else:
            analysis = self._analyze_text(input_data)
        
        # Create project plan
        project_plan = self._create_project_plan(analysis, input_data)
        
        # Generate folder structure
        folder_structure = self._generate_folder_structure(project_plan)
        
        # Define tech stack
        tech_stack = self._define_tech_stack(project_plan)
        
        # Break down tasks
        task_breakdown = self._break_down_tasks(project_plan)
        
        # Identify infrastructure needs
        infrastructure = self._identify_infrastructure(project_plan, input_data)
        
        result = {
            'analysis': analysis,
            'project_plan': project_plan,
            'folder_structure': folder_structure,
            'tech_stack': tech_stack,
            'task_breakdown': task_breakdown,
            'infrastructure': infrastructure
        }
        
        self.logger.info("Analysis and planning completed successfully")
        self.log_metric('tasks_identified', len(task_breakdown))
        
        return result
    
    def _analyze_csv(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze CSV file"""
        
        csv_path = input_data['csv_path']
        self.logger.info(f"Analyzing CSV file: {csv_path}")
        
        try:
            df = pd.read_csv(csv_path)
            
            analysis = {
                'data_shape': {
                    'rows': len(df),
                    'columns': len(df.columns)
                },
                'columns': df.columns.tolist(),
                'data_types': df.dtypes.astype(str).to_dict(),
                'missing_values': df.isnull().sum().to_dict(),
                'sample_data': df.head(5).to_dict('records'),
                'statistics': {}
            }
            
            # Get statistics for numeric columns
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                analysis['statistics'] = df[numeric_cols].describe().to_dict()
            
            # Infer project type from CSV content
            analysis['inferred_project_type'] = self._infer_project_type_from_csv(df)
            
            self.logger.info(f"CSV analysis complete: {len(df)} rows, {len(df.columns)} columns")
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing CSV: {str(e)}")
            raise
    
    def _analyze_text(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze text task description"""
        
        task_description = input_data['task_description']
        self.logger.info("Analyzing text task description...")
        
        # Extract key information from text
        analysis = {
            'task_description': task_description,
            'word_count': len(task_description.split()),
            'key_terms': self._extract_key_terms(task_description),
            'inferred_project_type': self._infer_project_type_from_text(task_description),
            'complexity': self._assess_complexity(task_description)
        }
        
        return analysis
    
    def _infer_project_type_from_csv(self, df: pd.DataFrame) -> str:
        """Infer project type from CSV data"""
        
        # Simple heuristics for project type inference
        column_names = ' '.join(df.columns).lower()
        
        if any(term in column_names for term in ['price', 'sales', 'revenue', 'predict']):
            return 'ml_prediction'
        elif any(term in column_names for term in ['user', 'customer', 'email', 'name']):
            return 'web_application'
        elif any(term in column_names for term in ['time', 'date', 'timestamp', 'series']):
            return 'time_series_analysis'
        else:
            return 'data_processing'
    
    def _infer_project_type_from_text(self, text: str) -> str:
        """Infer project type from text description"""
        
        text_lower = text.lower()
        
        # ML/AI Projects
        if any(term in text_lower for term in ['machine learning', 'ml', 'predict', 'model', 'train']):
            return 'ml_application'
        
        # Web Applications
        elif any(term in text_lower for term in ['website', 'web app', 'frontend', 'backend', 'api']):
            if 'api' in text_lower and 'frontend' not in text_lower:
                return 'rest_api'
            return 'web_application'
        
        # Data Processing
        elif any(term in text_lower for term in ['data', 'etl', 'pipeline', 'process']):
            return 'data_pipeline'
        
        # Microservices
        elif any(term in text_lower for term in ['microservice', 'service']):
            return 'microservices'
        
        # Default
        else:
            return 'general_application'
    
    def _extract_key_terms(self, text: str) -> List[str]:
        """Extract key technical terms from text"""
        
        keywords = [
            'api', 'rest', 'graphql', 'database', 'sql', 'nosql',
            'frontend', 'backend', 'fullstack', 'web', 'mobile',
            'ml', 'ai', 'prediction', 'classification', 'regression',
            'docker', 'kubernetes', 'aws', 'gcp', 'azure',
            'authentication', 'authorization', 'security',
            'microservices', 'serverless', 'lambda'
        ]
        
        text_lower = text.lower()
        found_terms = [term for term in keywords if term in text_lower]
        
        return found_terms
    
    def _assess_complexity(self, text: str) -> str:
        """Assess project complexity"""
        
        word_count = len(text.split())
        key_terms = self._extract_key_terms(text)
        
        if word_count < 50 and len(key_terms) < 3:
            return 'low'
        elif word_count < 150 and len(key_terms) < 6:
            return 'medium'
        else:
            return 'high'
    
    def _create_project_plan(self, analysis: Dict[str, Any], input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive project plan"""
        
        project_type = analysis.get('inferred_project_type', 'general_application')
        
        plan = {
            'project_name': input_data.get('project_name', f'project_{project_type}'),
            'project_type': project_type,
            'description': self._generate_project_description(analysis, project_type),
            'goals': self._define_project_goals(analysis, project_type),
            'requirements': self._extract_requirements(analysis, input_data),
            'constraints': input_data.get('constraints', []),
            'timeline': self._estimate_timeline(analysis)
        }
        
        return plan
    
    def _generate_project_description(self, analysis: Dict[str, Any], project_type: str) -> str:
        """Generate project description"""
        
        descriptions = {
            'ml_application': 'Machine Learning application for predictive analytics',
            'web_application': 'Full-stack web application with modern architecture',
            'rest_api': 'RESTful API service with comprehensive endpoints',
            'data_pipeline': 'Data processing pipeline with ETL capabilities',
            'microservices': 'Microservices architecture with distributed components',
            'general_application': 'General-purpose application'
        }
        
        return descriptions.get(project_type, 'Custom application')
    
    def _define_project_goals(self, analysis: Dict[str, Any], project_type: str) -> List[str]:
        """Define project goals"""
        
        common_goals = [
            'Implement clean, maintainable code',
            'Follow industry best practices',
            'Ensure proper error handling',
            'Add comprehensive logging',
            'Include documentation'
        ]
        
        type_specific_goals = {
            'ml_application': [
                'Build accurate prediction model',
                'Implement model versioning',
                'Add model monitoring'
            ],
            'web_application': [
                'Create responsive UI',
                'Implement user authentication',
                'Optimize performance'
            ],
            'rest_api': [
                'Design RESTful endpoints',
                'Add API documentation',
                'Implement rate limiting'
            ]
        }
        
        goals = common_goals + type_specific_goals.get(project_type, [])
        return goals
    
    def _extract_requirements(self, analysis: Dict[str, Any], input_data: Dict[str, Any]) -> List[str]:
        """Extract functional and non-functional requirements"""
        
        requirements = []
        
        # Functional requirements from analysis
        if 'task_description' in analysis:
            requirements.append(f"Implement: {analysis['task_description']}")
        
        # Add technical requirements
        requirements.extend([
            'Implement proper error handling',
            'Add logging and monitoring',
            'Include unit tests',
            'Add configuration management',
            'Implement security best practices'
        ])
        
        return requirements
    
    def _estimate_timeline(self, analysis: Dict[str, Any]) -> Dict[str, str]:
        """Estimate project timeline"""
        
        complexity = analysis.get('complexity', 'medium')
        
        timelines = {
            'low': {'planning': '1 day', 'development': '3-5 days', 'testing': '1-2 days', 'deployment': '1 day'},
            'medium': {'planning': '2 days', 'development': '1-2 weeks', 'testing': '3-5 days', 'deployment': '2 days'},
            'high': {'planning': '1 week', 'development': '3-4 weeks', 'testing': '1 week', 'deployment': '3-5 days'}
        }
        
        return timelines.get(complexity, timelines['medium'])
    
    def _generate_folder_structure(self, project_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Generate project folder structure"""
        
        project_type = project_plan['project_type']
        project_name = project_plan['project_name']
        
        # Base structure for all projects
        base_structure = {
            'root': project_name,
            'directories': [
                'src',
                'tests',
                'config',
                'docs',
                'scripts',
                '.github/workflows'
            ],
            'files': [
                'README.md',
                'requirements.txt',
                '.gitignore',
                '.env.example',
                'Dockerfile',
                'docker-compose.yml'
            ]
        }
        
        # Type-specific additions
        type_structures = {
            'web_application': {
                'directories': ['src/frontend', 'src/backend', 'src/shared', 'static', 'templates'],
                'files': ['src/frontend/index.html', 'src/backend/app.py']
            },
            'rest_api': {
                'directories': ['src/api', 'src/models', 'src/services', 'src/middleware'],
                'files': ['src/api/main.py', 'src/api/routes.py']
            },
            'ml_application': {
                'directories': ['src/models', 'src/data', 'src/training', 'src/inference', 'notebooks'],
                'files': ['src/training/train.py', 'src/inference/predict.py']
            },
            'data_pipeline': {
                'directories': ['src/extractors', 'src/transformers', 'src/loaders', 'src/validators'],
                'files': ['src/pipeline.py']
            }
        }
        
        # Merge structures
        specific_structure = type_structures.get(project_type, {})
        base_structure['directories'].extend(specific_structure.get('directories', []))
        base_structure['files'].extend(specific_structure.get('files', []))
        
        return base_structure
    
    def _define_tech_stack(self, project_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Define technology stack based on project type"""
        
        project_type = project_plan['project_type']
        
        tech_stacks = {
            'web_application': {
                'language': 'Python',
                'framework': 'FastAPI + React',
                'database': 'PostgreSQL',
                'cache': 'Redis',
                'other_tools': ['Nginx', 'Gunicorn', 'SQLAlchemy']
            },
            'rest_api': {
                'language': 'Python',
                'framework': 'FastAPI',
                'database': 'PostgreSQL',
                'cache': 'Redis',
                'other_tools': ['Pydantic', 'SQLAlchemy', 'Alembic']
            },
            'ml_application': {
                'language': 'Python',
                'framework': 'FastAPI',
                'database': 'PostgreSQL',
                'ml_tools': ['scikit-learn', 'pandas', 'numpy', 'MLflow'],
                'other_tools': ['Jupyter', 'Matplotlib']
            },
            'data_pipeline': {
                'language': 'Python',
                'framework': 'Apache Airflow',
                'database': 'PostgreSQL',
                'other_tools': ['pandas', 'Apache Spark', 'Kafka']
            }
        }
        
        return tech_stacks.get(project_type, tech_stacks['rest_api'])
    
    def _break_down_tasks(self, project_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Break down project into tasks"""
        
        tasks = [
            {
                'id': 'task_1',
                'name': 'Setup project structure',
                'priority': 'high',
                'estimated_effort': '2 hours',
                'dependencies': [],
                'agent': 'CodeGenerator'
            },
            {
                'id': 'task_2',
                'name': 'Implement core functionality',
                'priority': 'high',
                'estimated_effort': '1-2 days',
                'dependencies': ['task_1'],
                'agent': 'CodeGenerator'
            },
            {
                'id': 'task_3',
                'name': 'Add error handling and logging',
                'priority': 'high',
                'estimated_effort': '4 hours',
                'dependencies': ['task_2'],
                'agent': 'CodeGenerator'
            },
            {
                'id': 'task_4',
                'name': 'Code review and refactoring',
                'priority': 'high',
                'estimated_effort': '4-6 hours',
                'dependencies': ['task_3'],
                'agent': 'CodeReviewer'
            },
            {
                'id': 'task_5',
                'name': 'Setup deployment infrastructure',
                'priority': 'high',
                'estimated_effort': '1 day',
                'dependencies': ['task_4'],
                'agent': 'DevOpsEngineer'
            },
            {
                'id': 'task_6',
                'name': 'Final validation and deployment',
                'priority': 'critical',
                'estimated_effort': '4 hours',
                'dependencies': ['task_5'],
                'agent': 'Validator'
            }
        ]
        
        return tasks
    
    def _identify_infrastructure(self, project_plan: Dict[str, Any], input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Identify infrastructure requirements"""
        
        cloud_provider = input_data.get('cloud_provider', self.config.cloud.cloud_provider)
        project_type = project_plan['project_type']
        
        infrastructure = {
            'cloud_provider': cloud_provider,
            'compute': self._get_compute_requirements(project_type),
            'storage': self._get_storage_requirements(project_type),
            'networking': self._get_networking_requirements(project_type),
            'services': self._get_cloud_services(cloud_provider, project_type)
        }
        
        return infrastructure
    
    def _get_compute_requirements(self, project_type: str) -> Dict[str, Any]:
        """Get compute requirements"""
        
        requirements = {
            'ml_application': {
                'type': 'GPU-enabled instances',
                'cpu': '4-8 vCPUs',
                'memory': '16-32 GB',
                'gpu': 'Optional for training'
            },
            'web_application': {
                'type': 'General purpose instances',
                'cpu': '2-4 vCPUs',
                'memory': '8-16 GB'
            },
            'rest_api': {
                'type': 'General purpose instances',
                'cpu': '2 vCPUs',
                'memory': '4-8 GB'
            }
        }
        
        return requirements.get(project_type, requirements['rest_api'])
    
    def _get_storage_requirements(self, project_type: str) -> Dict[str, Any]:
        """Get storage requirements"""
        
        return {
            'persistent_volume': '20-50 GB',
            'object_storage': 'For assets and backups',
            'database_storage': '10-20 GB'
        }
    
    def _get_networking_requirements(self, project_type: str) -> Dict[str, Any]:
        """Get networking requirements"""
        
        return {
            'load_balancer': 'Required',
            'cdn': 'Optional',
            'vpc': 'Isolated network',
            'security_groups': 'Firewall rules'
        }
    
    def _get_cloud_services(self, cloud_provider: str, project_type: str) -> List[str]:
        """Get required cloud services"""
        
        services = {
            'aws': {
                'common': ['ECS/EKS', 'RDS', 'S3', 'CloudWatch', 'IAM'],
                'ml_application': ['SageMaker', 'ECR'],
                'web_application': ['CloudFront', 'Route53']
            },
            'gcp': {
                'common': ['GKE', 'Cloud SQL', 'Cloud Storage', 'Cloud Monitoring'],
                'ml_application': ['Vertex AI', 'Container Registry'],
                'web_application': ['Cloud CDN', 'Cloud DNS']
            },
            'azure': {
                'common': ['AKS', 'Azure Database', 'Blob Storage', 'Monitor'],
                'ml_application': ['Azure ML', 'Container Registry'],
                'web_application': ['CDN', 'DNS']
            }
        }
        
        provider_services = services.get(cloud_provider, services['aws'])
        return provider_services['common'] + provider_services.get(project_type, [])
    
    def generate_output(self, processed_data: Any) -> Dict[str, Any]:
        """Generate formatted output"""
        
        return {
            'status': 'completed',
            'analysis_complete': True,
            'project_ready_for_coding': True,
            'data': processed_data
        }


__all__ = ['AnalyzerAgent']
