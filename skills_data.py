"""
skills_data.py - Configurable Technical Skills Database & Learning Roadmap

This module maintains:
1. DEFAULT_SKILLS_DB: Comprehensive categorized list of technical skills.
2. SKILL_ALIASES: Common alternative spellings, acronyms, and abbreviations
   mapped to their canonical skill names.
3. LEARNING_ROADMAP: Recommended learning topics and focus areas for missing skills.
"""

from typing import Dict, List

# Categorized skills database
DEFAULT_SKILLS_DB: Dict[str, List[str]] = {
    "Programming Languages": [
        "Python", "Java", "C", "C++", "C#", "JavaScript", "TypeScript",
        "R", "Go", "Rust", "Ruby", "PHP", "Kotlin", "Swift", "Scala", "Dart", "SQL"
    ],
    "Frameworks & Libraries": [
        "React", "Angular", "Vue.js", "Node.js", "Express.js", "Django", "Flask",
        "FastAPI", "Spring Boot", "ASP.NET", "Next.js", "HTML5", "CSS3",
        "Tailwind CSS", "Bootstrap", "Redux", "GraphQL"
    ],
    "Data Science & AI / ML": [
        "Machine Learning", "Deep Learning", "Natural Language Processing",
        "Computer Vision", "Pandas", "NumPy", "Scikit-Learn", "TensorFlow",
        "PyTorch", "Keras", "OpenCV", "Matplotlib", "Seaborn", "Hugging Face",
        "Large Language Models", "Generative AI", "Data Analysis", "Feature Engineering"
    ],
    "Databases & Big Data": [
        "MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite", "Oracle",
        "Microsoft SQL Server", "Snowflake", "Apache Spark", "Hadoop",
        "Kafka", "Elasticsearch", "Cassandra", "DynamoDB"
    ],
    "Cloud & DevOps": [
        "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Linux",
        "Git", "GitHub", "GitLab", "CI/CD", "Terraform", "Jenkins", "Ansible",
        "Bash", "Nginx"
    ],
    "Tools, Testing & Methodologies": [
        "REST APIs", "Microservices", "Docker Compose", "Postman", "Jira",
        "Agile", "Scrum", "Unit Testing", "PyTest", "Jest", "Power BI",
        "Tableau", "Excel"
    ]
}

# Aliases and variations mapped to the canonical skill name
# This ensures that terms like 'js' match 'JavaScript' and 'postgres' matches 'PostgreSQL'.
SKILL_ALIASES: Dict[str, str] = {
    # Programming Languages
    "py": "Python",
    "python3": "Python",
    "js": "JavaScript",
    "ts": "TypeScript",
    "golang": "Go",
    "cpp": "C++",
    "c plus plus": "C++",
    "csharp": "C#",
    "c sharp": "C#",
    
    # Web & Frameworks
    "reactjs": "React",
    "react.js": "React",
    "vue": "Vue.js",
    "vuejs": "Vue.js",
    "nodejs": "Node.js",
    "node": "Node.js",
    "express": "Express.js",
    "expressjs": "Express.js",
    "springboot": "Spring Boot",
    "nextjs": "Next.js",
    "html": "HTML5",
    "css": "CSS3",
    "tailwind": "Tailwind CSS",
    
    # Data Science & AI / ML
    "ml": "Machine Learning",
    "dl": "Deep Learning",
    "nlp": "Natural Language Processing",
    "cv": "Computer Vision",
    "sklearn": "Scikit-Learn",
    "scikit learn": "Scikit-Learn",
    "tf": "TensorFlow",
    "huggingface": "Hugging Face",
    "llm": "Large Language Models",
    "llms": "Large Language Models",
    "genai": "Generative AI",
    "gen ai": "Generative AI",
    
    # Databases & Big Data
    "postgres": "PostgreSQL",
    "mongo": "MongoDB",
    "mssql": "Microsoft SQL Server",
    "sql server": "Microsoft SQL Server",
    "spark": "Apache Spark",
    
    # Cloud & DevOps
    "amazon web services": "AWS",
    "google cloud platform": "Google Cloud",
    "gcp": "Google Cloud",
    "k8s": "Kubernetes",
    "ci cd": "CI/CD",
    "cicd": "CI/CD",
    
    # Tools & Methodologies
    "rest": "REST APIs",
    "rest api": "REST APIs",
    "restful api": "REST APIs",
    "restful apis": "REST APIs",
    "powerbi": "Power BI",
    "ms excel": "Excel"
}

# Curated learning roadmap for skills to provide actionable guidance
LEARNING_ROADMAP: Dict[str, Dict[str, str]] = {
    "Python": {
        "topics": "OOP concepts, generators, list comprehensions, virtual environments, error handling.",
        "resource": "Official Python Tutorial (docs.python.org) and Python Crash Course."
    },
    "Machine Learning": {
        "topics": "Supervised/unsupervised learning, cross-validation, hyperparameter tuning, model evaluation metrics (ROC-AUC, F1).",
        "resource": "Andrew Ng's Machine Learning Specialization & Scikit-Learn user guide."
    },
    "Deep Learning": {
        "topics": "Neural network architecture, backpropagation, activation functions, CNNs, RNNs, optimizers (Adam).",
        "resource": "DeepLearning.AI Deep Learning Specialization & Fast.ai."
    },
    "Natural Language Processing": {
        "topics": "Text preprocessing, tokenization, TF-IDF, Word2Vec, Transformer architectures, BERT, Hugging Face pipelines.",
        "resource": "Hugging Face NLP Course (huggingface.co/learn/nlp-course)."
    },
    "Computer Vision": {
        "topics": "Image filtering, edge detection, OpenCV basics, CNN architectures, object detection (YOLO), image segmentation.",
        "resource": "PyImageSearch tutorials & OpenCV documentation."
    },
    "Large Language Models": {
        "topics": "Self-attention mechanisms, prompt engineering, fine-tuning (LoRA/QLoRA), RAG architectures, LangChain.",
        "resource": "DeepLearning.AI Short Courses on LLMs and LangChain."
    },
    "Generative AI": {
        "topics": "Diffusion models, GANs, text-to-image pipelines, prompt engineering, vector databases (Chroma, Pinecone).",
        "resource": "Google Cloud Generative AI learning path & Hugging Face docs."
    },
    "Pandas": {
        "topics": "DataFrame manipulation, groupby, indexing, handling missing values, merge/join operations, performance optimization.",
        "resource": "10 Minutes to pandas (pandas.pydata.org) & Kaggle Pandas Micro-course."
    },
    "NumPy": {
        "topics": "Multi-dimensional arrays, broadcasting, vectorization, linear algebra operations, indexing masks.",
        "resource": "NumPy absolute beginner tutorial (numpy.org)."
    },
    "Scikit-Learn": {
        "topics": "Pipelines, ColumnTransformer, regression, classification, clustering, model evaluation.",
        "resource": "Scikit-Learn Getting Started guide (scikit-learn.org)."
    },
    "TensorFlow": {
        "topics": "Tensors, Keras Sequential and Functional APIs, model training loops, callbacks, saving/exporting models.",
        "resource": "TensorFlow Core Tutorials (tensorflow.org/tutorials)."
    },
    "PyTorch": {
        "topics": "Tensors, autograd, torch.nn module, Dataset/DataLoader, writing custom training loops, GPU acceleration.",
        "resource": "PyTorch 60-Minute Blitz (pytorch.org/tutorials)."
    },
    "SQL": {
        "topics": "Complex JOINs, window functions (ROW_NUMBER, RANK), subqueries, indexing, CTEs, aggregation.",
        "resource": "Mode Analytics SQL Tutorial & SQLZoo."
    },
    "Docker": {
        "topics": "Containers vs VMs, Dockerfile instructions (FROM, RUN, CMD, COPY), Docker Compose, volumes, networking.",
        "resource": "Docker Getting Started Guide (docs.docker.com/get-started)."
    },
    "Kubernetes": {
        "topics": "Pods, Deployments, Services, ConfigMaps, Ingress controllers, Helm charts.",
        "resource": "Kubernetes Basics Tutorial (kubernetes.io/docs/tutorials)."
    },
    "AWS": {
        "topics": "EC2, S3, Lambda, IAM permissions, RDS, API Gateway, CloudWatch.",
        "resource": "AWS Skill Builder Free Tier & AWS Free Tier Hands-on."
    },
    "Azure": {
        "topics": "Azure Virtual Machines, Blob Storage, Azure Functions, Azure SQL, Entra ID.",
        "resource": "Microsoft Learn Azure Fundamentals (AZ-900)."
    },
    "Google Cloud": {
        "topics": "Compute Engine, Cloud Storage, Cloud Run, BigQuery, IAM roles.",
        "resource": "Google Cloud Skills Boost free introductory labs."
    },
    "Git": {
        "topics": "Branching, merging, resolving conflicts, rebase, git stash, pull requests, conventional commits.",
        "resource": "Pro Git Book (git-scm.com/book) & GitHub Skills."
    },
    "FastAPI": {
        "topics": "Pydantic data models, type hints, async endpoints, dependency injection, OpenAPI documentation.",
        "resource": "FastAPI Official Tutorial (fastapi.tiangolo.com)."
    },
    "Flask": {
        "topics": "Routing, Jinja2 templates, request/response cycle, blueprints, SQLAlchemy integration.",
        "resource": "Flask Official Documentation (flask.palletsprojects.com)."
    },
    "Django": {
        "topics": "MVT architecture, Django ORM, migrations, admin panel, authentication, Django REST Framework.",
        "resource": "Django Girls Tutorial & Official Django documentation."
    },
    "React": {
        "topics": "JSX, functional components, useState, useEffect, custom hooks, context API, component lifecycle.",
        "resource": "React.dev Interactive Quick Start."
    },
    "PostgreSQL": {
        "topics": "ACID compliance, schema design, EXPLAIN ANALYZE for query optimization, JSONB fields, indexing (B-tree, GIN).",
        "resource": "PostgreSQL Tutorial (postgresqltutorial.com)."
    },
    "MongoDB": {
        "topics": "BSON document structure, CRUD operations, Aggregation pipeline, indexing, replica sets.",
        "resource": "MongoDB University Free Courses (learn.mongodb.com)."
    },
    "Power BI": {
        "topics": "Data modeling, DAX queries (CALCULATE, RELATED), report design, Power Query transformations.",
        "resource": "Microsoft Learn Power BI Data Analyst path."
    },
    "Tableau": {
        "topics": "Calculated fields, level of detail (LOD) expressions, interactive dashboards, data blending.",
        "resource": "Tableau Free Training Videos (tableau.com)."
    },
    "CI/CD": {
        "topics": "GitHub Actions workflows, build pipelines, automated testing, continuous deployment to staging/production.",
        "resource": "GitHub Actions Quickstart Guide."
    },
    "REST APIs": {
        "topics": "HTTP verbs (GET, POST, PUT, DELETE), status codes, authentication (JWT, OAuth2), idempotency, pagination.",
        "resource": "REST API Tutorial (restfulapi.net)."
    }
}
